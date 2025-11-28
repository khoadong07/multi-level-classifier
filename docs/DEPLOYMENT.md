# Deployment Guide

Complete guide for deploying KMLC to production.

## Prerequisites

- Docker & Docker Compose
- Domain name (optional)
- SSL certificate (recommended)
- MongoDB (can use Docker or external service)

## Production Configuration

### 1. Environment Variables

Create `.env` file with production values:

```env
# LLM Configuration
OPENAI_API_KEY=your-production-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL=gpt-3.5-turbo
TEMPERATURE=0.0
MAX_TOKENS=150

# Database
MONGODB_URL=mongodb://mongodb:27017
DATABASE_NAME=kmlc_production

# Security (IMPORTANT: Change these!)
SECRET_KEY=your-very-long-random-secret-key-here

# Processing
MAX_WORKERS=10
CACHE_FILE=classification_cache.json

# Directories
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs
CACHE_DIR=.
```

### 2. Generate Secure Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Update Docker Compose

For production, update `docker-compose-fullstack.yml`:

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:7.0
    container_name: kmlc_mongodb
    restart: always
    volumes:
      - mongodb_data:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=your-secure-password
    networks:
      - kmlc_network

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: kmlc_backend
    restart: always
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - mongodb
    volumes:
      - ./uploads:/app/uploads
      - ./outputs:/app/outputs
    networks:
      - kmlc_network

  worker:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: kmlc_worker
    restart: always
    command: python3 backend/queue_worker.py
    env_file:
      - .env
    depends_on:
      - mongodb
      - backend
    volumes:
      - ./uploads:/app/uploads
      - ./outputs:/app/outputs
    networks:
      - kmlc_network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: kmlc_frontend
    restart: always
    ports:
      - "3000:3000"
    depends_on:
      - backend
    networks:
      - kmlc_network

volumes:
  mongodb_data:

networks:
  kmlc_network:
    driver: bridge
```

## Deployment Steps

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone repository
git clone <repository>
cd kmlc

# 2. Configure environment
cp .env.example .env
nano .env  # Edit with production values

# 3. Build images
docker-compose -f docker-compose-fullstack.yml build

# 4. Start services
docker-compose -f docker-compose-fullstack.yml up -d

# 5. Check status
docker-compose -f docker-compose-fullstack.yml ps

# 6. View logs
docker-compose -f docker-compose-fullstack.yml logs -f
```

### Option 2: Kubernetes

Create Kubernetes manifests:

```yaml
# kmlc-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kmlc-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: kmlc-backend
  template:
    metadata:
      labels:
        app: kmlc-backend
    spec:
      containers:
      - name: backend
        image: kmlc-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: MONGODB_URL
          valueFrom:
            secretKeyRef:
              name: kmlc-secrets
              key: mongodb-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: kmlc-secrets
              key: secret-key
```

Deploy:

```bash
kubectl apply -f kmlc-deployment.yaml
kubectl apply -f kmlc-service.yaml
```

## SSL/TLS Configuration

### Using Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/ssl/certs/your-cert.pem;
    ssl_certificate_key /etc/ssl/private/your-key.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Using Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Security Checklist

- [ ] Change default admin password
- [ ] Set strong SECRET_KEY
- [ ] Use HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up MongoDB authentication
- [ ] Limit CORS origins
- [ ] Enable rate limiting
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Review file upload limits
- [ ] Set up log rotation

## Monitoring

### Health Checks

```bash
# Backend health
curl https://your-domain.com/api/

# Check all services
docker-compose -f docker-compose-fullstack.yml ps
```

### Logging

```bash
# View all logs
docker-compose -f docker-compose-fullstack.yml logs -f

# View specific service
docker logs kmlc_backend -f
docker logs kmlc_worker -f
docker logs kmlc_frontend -f
```

### Metrics

Consider adding:
- Prometheus for metrics
- Grafana for visualization
- ELK stack for log aggregation

## Backup Strategy

### MongoDB Backup

```bash
# Manual backup
docker exec kmlc_mongodb mongodump --out /backup

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker exec kmlc_mongodb mongodump --out /backup/backup_$DATE
```

### File Backup

```bash
# Backup uploads and outputs
tar -czf backup_files_$(date +%Y%m%d).tar.gz uploads/ outputs/
```

## Scaling

### Horizontal Scaling

1. **Backend**: Add more backend replicas
```yaml
backend:
  deploy:
    replicas: 3
```

2. **Workers**: Add more worker instances
```yaml
worker:
  deploy:
    replicas: 5
```

3. **Load Balancer**: Use Nginx or cloud load balancer

### Vertical Scaling

Increase resources in docker-compose:

```yaml
backend:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 4G
      reservations:
        cpus: '1'
        memory: 2G
```

## Troubleshooting

### Common Issues

**1. Backend won't start**
```bash
# Check logs
docker logs kmlc_backend

# Verify environment variables
docker exec kmlc_backend env | grep OPENAI
```

**2. MongoDB connection failed**
```bash
# Check MongoDB status
docker exec kmlc_mongodb mongosh --eval "db.adminCommand('ping')"

# Verify connection string
echo $MONGODB_URL
```

**3. Worker not processing tasks**
```bash
# Check worker logs
docker logs kmlc_worker

# Restart worker
docker-compose -f docker-compose-fullstack.yml restart worker
```

## Maintenance

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild images
docker-compose -f docker-compose-fullstack.yml build

# Restart services (zero-downtime)
docker-compose -f docker-compose-fullstack.yml up -d --no-deps --build backend
docker-compose -f docker-compose-fullstack.yml up -d --no-deps --build frontend
docker-compose -f docker-compose-fullstack.yml up -d --no-deps --build worker
```

### Database Maintenance

```bash
# Compact database
docker exec kmlc_mongodb mongosh kmlc_production --eval "db.runCommand({compact: 'tasks'})"

# Create indexes
docker exec kmlc_mongodb mongosh kmlc_production --eval "db.tasks.createIndex({created_at: -1})"
```

## Performance Optimization

1. **Enable caching**: Use Redis for session storage
2. **CDN**: Serve static assets via CDN
3. **Database indexing**: Ensure proper indexes
4. **Connection pooling**: Configure MongoDB connection pool
5. **Compression**: Enable gzip compression

## Support

For production support:
- Email: support@kompa.ai
- Documentation: https://docs.kompa.ai
- GitHub Issues: https://github.com/kompa/kmlc/issues
