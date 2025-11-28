# 🏗️ Kiến trúc hệ thống SPX Classification v2.0

## 📋 Tổng quan

Hệ thống phân loại feedback SPX được thiết kế theo kiến trúc **xử lý tập trung** (Centralized Processing Architecture) với các nguyên tắc:

- **Separation of Concerns**: Tách biệt rõ ràng giữa UI, business logic, và data
- **Modularity**: Các module độc lập, dễ bảo trì và mở rộng
- **Scalability**: Hỗ trợ xử lý song song với ThreadPoolExecutor
- **Caching**: Cache thông minh để tối ưu hiệu suất và chi phí

## 🗂️ Cấu trúc thư mục

```
spx_classification/
│
├── app/                          # Application package
│   ├── __init__.py
│   ├── main.py                   # Streamlit UI layer
│   │
│   ├── core/                     # Core business logic
│   │   ├── __init__.py
│   │   ├── config.py             # Configuration management
│   │   ├── classifier.py         # LLM classification logic
│   │   ├── cache_manager.py      # Cache management
│   │   └── processor.py          # Central batch processor
│   │
│   ├── utils/                    # Utility functions
│   │   ├── __init__.py
│   │   ├── text_utils.py         # Text processing utilities
│   │   └── file_utils.py         # File I/O utilities
│   │
│   └── models/                   # Data models
│       ├── __init__.py
│       └── schemas.py            # Dataclass definitions
│
├── scripts/                      # Utility scripts
│   ├── check_config.py           # Configuration checker
│   ├── clear_cache.py            # Cache cleaner
│   └── test_system.py            # System tests
│
├── run.py                        # Application entry point
├── prompt_template.txt           # LLM prompt template
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose setup
├── .env.example                  # Environment template
├── Makefile                      # Build automation
├── README.md                     # English documentation
├── HUONG_DAN.md                  # Vietnamese guide
└── ARCHITECTURE.md               # This file
```

## 🔧 Các thành phần chính

### 1. Core Layer (`app/core/`)

#### Config (`config.py`)
- **Chức năng**: Quản lý cấu hình tập trung
- **Nguồn dữ liệu**: Environment variables (.env)
- **Responsibilities**:
  - Load và validate configuration
  - Provide configuration constants
  - Load prompt template

```python
class Config:
    CACHE_FILE = "classification_cache.json"
    MAX_WORKERS = 10
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # ...
```

#### Classifier (`classifier.py`)
- **Chức năng**: Xử lý phân loại văn bản bằng LLM
- **Dependencies**: OpenAI API client
- **Responsibilities**:
  - Build prompts từ template
  - Call LLM API với retry logic
  - Extract và validate JSON response

```python
class Classifier:
    def classify(feedback: str) -> Optional[str]:
        # Build prompt → Call API → Extract result
```

#### CacheManager (`cache_manager.py`)
- **Chức năng**: Quản lý cache với file persistence
- **Storage**: JSON file
- **Responsibilities**:
  - Load/save cache từ/vào file
  - Get/set cache entries
  - Clear cache

```python
class CacheManager:
    def get(key: str) -> Optional[str]
    def set(key: str, label: str)
    def save()
```

#### CentralProcessor (`processor.py`)
- **Chức năng**: Engine xử lý batch tập trung
- **Pattern**: Coordinator pattern
- **Responsibilities**:
  - Prepare tasks từ DataFrame
  - Orchestrate concurrent processing
  - Aggregate results và statistics
  - Apply results back to DataFrame

```python
class CentralProcessor:
    def prepare_tasks(df) -> List[ClassificationTask]
    def process_task(task) -> ClassificationResult
    def process_batch(tasks) -> (results, stats)
    def apply_results_to_dataframe(df, results) -> DataFrame
```

### 2. Models Layer (`app/models/`)

#### Schemas (`schemas.py`)
- **Chức năng**: Define data structures
- **Pattern**: Dataclass pattern
- **Models**:
  - `ClassificationTask`: Input task
  - `ClassificationResult`: Output result
  - `ProcessingStats`: Statistics tracking

```python
@dataclass
class ClassificationTask:
    index: int
    feedback: str
    feedback_key: str

@dataclass
class ClassificationResult:
    index: int
    label_en: Optional[str]
    label_1: Optional[str]
    # ...
    status: str
```

### 3. Utils Layer (`app/utils/`)

#### Text Utils (`text_utils.py`)
- **Chức năng**: Text processing utilities
- **Functions**:
  - `clean_text()`: Clean và normalize text
  - `merge_feedback()`: Merge multiple fields
  - `normalize_feedback_key()`: Create cache key
  - `split_label()`: Split hierarchical label

#### File Utils (`file_utils.py`)
- **Chức năng**: File I/O operations
- **Functions**:
  - `load_excel()`: Load Excel to DataFrame
  - `save_excel()`: Save DataFrame to Excel
  - `to_excel_bytes()`: Convert to bytes for download

### 4. UI Layer (`app/main.py`)

- **Framework**: Streamlit
- **Responsibilities**:
  - User interface
  - File upload/download
  - Progress tracking
  - Results visualization
- **Pattern**: MVC-like separation

## 🔄 Luồng xử lý dữ liệu

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│                      (Streamlit UI)                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   CENTRAL PROCESSOR                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 1. Prepare Tasks                                     │   │
│  │    - Read DataFrame                                  │   │
│  │    - Merge feedback fields                           │   │
│  │    - Generate cache keys                             │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 2. Process Batch (Concurrent)                        │   │
│  │    ┌─────────────────────────────────────────────┐   │   │
│  │    │ For each task (parallel):                   │   │   │
│  │    │   ├─ Check Cache ──────────────┐            │   │   │
│  │    │   │                             ▼            │   │   │
│  │    │   │                    ┌────────────────┐   │   │   │
│  │    │   │                    │ Cache Manager  │   │   │   │
│  │    │   │                    └────────────────┘   │   │   │
│  │    │   │                             │            │   │   │
│  │    │   │         Hit ◄───────────────┤            │   │   │
│  │    │   │                             │            │   │   │
│  │    │   │         Miss                ▼            │   │   │
│  │    │   │                    ┌────────────────┐   │   │   │
│  │    │   └─ Call Classifier ─►│  Classifier    │   │   │   │
│  │    │                        │  (LLM API)     │   │   │   │
│  │    │                        └────────────────┘   │   │   │
│  │    │                             │                │   │   │
│  │    │                             ▼                │   │   │
│  │    │                    Update Cache              │   │   │
│  │    └─────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 3. Aggregate Results                                 │   │
│  │    - Collect all results                             │   │
│  │    - Calculate statistics                            │   │
│  │    - Apply to DataFrame                              │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    OUTPUT & DOWNLOAD                         │
│                  (Excel with labels)                         │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Design Patterns

### 1. Dependency Injection
```python
processor = CentralProcessor(
    classifier=classifier,
    cache_manager=cache_manager,
    max_workers=10
)
```

### 2. Strategy Pattern
- Classifier có thể thay đổi implementation (OpenAI, Anthropic, etc.)
- Cache có thể thay đổi storage backend (JSON, Redis, etc.)

### 3. Coordinator Pattern
- CentralProcessor orchestrates các components
- Không có direct coupling giữa Classifier và CacheManager

### 4. Repository Pattern
- CacheManager abstract storage layer
- Dễ dàng thay đổi từ file sang database

## 🚀 Concurrent Processing

### ThreadPoolExecutor Architecture

```python
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {
        executor.submit(process_task, task): task 
        for task in tasks
    }
    
    for future in as_completed(futures):
        result = future.result()
        # Handle result
```

### Benefits:
- **Parallel execution**: Xử lý nhiều tasks đồng thời
- **Non-blocking**: UI không bị block
- **Scalable**: Dễ dàng điều chỉnh số workers

### Considerations:
- **Thread-safe**: Cache operations phải thread-safe
- **Rate limiting**: Cần handle API rate limits
- **Error handling**: Mỗi task có error handling riêng

## 💾 Caching Strategy

### Cache Key Generation
```python
feedback = "Tài xế giao hàng nhanh"
key = normalize_feedback_key(feedback)
# → "tai xe giao hang nhanh"
```

### Cache Hit/Miss Flow
```
Request → Check Cache
           │
           ├─ Hit → Return cached result (fast)
           │
           └─ Miss → Call API → Cache result → Return
```

### Benefits:
- **Cost saving**: Không gọi API cho feedback trùng lặp
- **Speed**: Cache hit nhanh hơn API call 100x
- **Consistency**: Cùng feedback → cùng kết quả

## 🔐 Configuration Management

### Environment Variables (.env)
```env
# API
OPENAI_API_KEY=xxx
OPENAI_BASE_URL=xxx
MODEL=xxx

# Processing
MAX_WORKERS=10
MAX_RETRY=3

# Model
TEMPERATURE=0
MAX_TOKENS=150
```

### Config Validation
```python
Config.validate()  # Raises error if invalid
```

## 📊 Error Handling

### Levels:
1. **Task Level**: Mỗi task có try-catch riêng
2. **Batch Level**: Batch processing handle worker errors
3. **Application Level**: UI handle system errors

### Retry Logic:
```python
for attempt in range(1, max_retry + 1):
    try:
        result = call_api()
        return result
    except Exception as e:
        if attempt < max_retry:
            time.sleep(retry_wait)
        else:
            return None
```

## 🧪 Testing Strategy

### Unit Tests
- Test individual components (Classifier, CacheManager)
- Mock external dependencies (API calls)

### Integration Tests
- Test component interactions
- Test end-to-end flow

### Test Scripts
```bash
python scripts/test_system.py
```

## 🔄 Future Enhancements

### Potential Improvements:
1. **Database backend**: Replace JSON cache with Redis/PostgreSQL
2. **Async processing**: Use asyncio instead of threads
3. **Batch API calls**: Group multiple feedbacks in one API call
4. **Model fine-tuning**: Fine-tune model on SPX data
5. **API abstraction**: Support multiple LLM providers
6. **Monitoring**: Add logging and metrics
7. **Web API**: Add REST API layer
8. **Authentication**: Add user authentication

### Scalability Considerations:
- **Horizontal scaling**: Deploy multiple instances
- **Load balancing**: Distribute requests
- **Queue system**: Use Celery/RabbitMQ for async processing
- **Microservices**: Split into separate services

## 📚 Dependencies

### Core:
- `streamlit`: UI framework
- `pandas`: Data manipulation
- `openai`: LLM API client

### Utilities:
- `python-dotenv`: Environment management
- `openpyxl`: Excel file handling
- `tqdm`: Progress bars

### Development:
- `docker`: Containerization
- `docker-compose`: Multi-container orchestration

## 🎓 Best Practices

### Code Organization:
- ✅ Single Responsibility Principle
- ✅ Dependency Injection
- ✅ Type hints
- ✅ Docstrings
- ✅ Error handling

### Performance:
- ✅ Concurrent processing
- ✅ Caching
- ✅ Lazy loading
- ✅ Resource cleanup

### Maintainability:
- ✅ Modular design
- ✅ Clear separation of concerns
- ✅ Configuration management
- ✅ Comprehensive documentation

---

**Version**: 2.0.0  
**Last Updated**: November 2025  
**Architecture**: Centralized Processing  
**Pattern**: MVC-like with Coordinator
