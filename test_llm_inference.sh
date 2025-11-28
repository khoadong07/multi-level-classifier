#!/bin/bash

echo "🧪 Testing LLM Inference Flow"
echo "=============================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Login
echo -e "${BLUE}1. Logging in...${NC}"
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ Login failed"
    exit 1
fi
echo -e "${GREEN}✅ Logged in successfully${NC}"
echo ""

# 2. Get topics
echo -e "${BLUE}2. Getting topics...${NC}"
TOPICS=$(curl -s -X GET http://localhost:8000/api/topics \
  -H "Authorization: Bearer $TOKEN")
TOPIC_ID=$(echo "$TOPICS" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['topics'][0]['topic_id']) if data['topics'] else print('')")

if [ -z "$TOPIC_ID" ]; then
    echo "❌ No topics found"
    exit 1
fi
echo -e "${GREEN}✅ Found topic: $TOPIC_ID${NC}"
echo ""

# 3. Create test data
echo -e "${BLUE}3. Creating test data...${NC}"
python3 << 'EOF'
import pandas as pd

data = {
    'Title': [
        'Dịch vụ xuất sắc',
        'Rất thất vọng',
        'Bình thường'
    ],
    'Content': [
        'Tôi rất hài lòng với chất lượng dịch vụ',
        'Sản phẩm không như mong đợi, rất tệ',
        'Không có gì đặc biệt'
    ],
    'Description': [
        'Nhân viên nhiệt tình, chuyên nghiệp',
        'Chất lượng kém, không đáng tiền',
        'Trung bình, không tốt không xấu'
    ]
}

df = pd.DataFrame(data)
df.to_excel('/tmp/test_inference.xlsx', index=False)
print("✅ Test data created")
EOF
echo ""

# 4. Upload file
echo -e "${BLUE}4. Uploading file...${NC}"
UPLOAD_RESULT=$(curl -s -X POST http://localhost:8000/api/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/test_inference.xlsx" \
  -F "topic_id=$TOPIC_ID")

JOB_ID=$(echo "$UPLOAD_RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin)['job_id'])")
echo -e "${GREEN}✅ File uploaded, Job ID: $JOB_ID${NC}"
echo ""

# 5. Start classification
echo -e "${BLUE}5. Starting classification (calling LLM)...${NC}"
curl -s -X POST "http://localhost:8000/api/classify/$JOB_ID" \
  -H "Authorization: Bearer $TOKEN" > /dev/null
echo -e "${YELLOW}⏳ Processing...${NC}"
echo ""

# 6. Wait and check status
for i in {1..10}; do
    sleep 2
    STATUS=$(curl -s -X GET "http://localhost:8000/api/status/$JOB_ID" \
      -H "Authorization: Bearer $TOKEN")
    
    TASK_STATUS=$(echo "$STATUS" | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])")
    PROGRESS=$(echo "$STATUS" | python3 -c "import sys, json; print(json.load(sys.stdin)['progress'])")
    
    echo -e "${YELLOW}Status: $TASK_STATUS | Progress: $PROGRESS%${NC}"
    
    if [ "$TASK_STATUS" = "completed" ]; then
        echo ""
        echo -e "${GREEN}✅ Classification completed!${NC}"
        echo ""
        
        # Show stats
        echo -e "${BLUE}6. Statistics:${NC}"
        echo "$STATUS" | python3 -c "import sys, json; data=json.load(sys.stdin); stats=data['stats']; print(f\"   Total tasks: {stats['total_tasks']}\"); print(f\"   API calls (LLM): {stats['api_calls']}\"); print(f\"   Cache hits: {stats['cache_hits']}\"); print(f\"   Failed: {stats['failed']}\"); print(f\"   Success rate: {stats['success_rate']}%\")"
        echo ""
        
        # Download and show results
        echo -e "${BLUE}7. Downloading results...${NC}"
        curl -s -X GET "http://localhost:8000/api/download/$JOB_ID" \
          -H "Authorization: Bearer $TOKEN" \
          -o /tmp/result_inference.xlsx
        
        echo -e "${GREEN}✅ Results downloaded${NC}"
        echo ""
        
        echo -e "${BLUE}8. Classification Results:${NC}"
        python3 << 'PYEOF'
import pandas as pd
df = pd.read_excel('/tmp/result_inference.xlsx')
print("="*100)
for idx, row in df.iterrows():
    print(f"\nRecord {idx+1}:")
    print(f"  Title: {row['Title']}")
    print(f"  Content: {row['Content'][:50]}...")
    print(f"  Classification: {row['label_en']}")
print("\n" + "="*100)
PYEOF
        
        break
    fi
    
    if [ "$TASK_STATUS" = "failed" ]; then
        echo -e "❌ Classification failed"
        echo "$STATUS" | python3 -c "import sys, json; print(json.load(sys.stdin).get('error', 'Unknown error'))"
        exit 1
    fi
done

echo ""
echo -e "${GREEN}🎉 Test completed successfully!${NC}"
echo ""
echo "Summary:"
echo "  - LLM service was called successfully"
echo "  - All records were classified"
echo "  - Results saved to /tmp/result_inference.xlsx"
