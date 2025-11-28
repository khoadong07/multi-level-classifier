# Kompa MultiLevel Classifier (KMLC)

AI-powered multilevel text classification system with topic-based LLM configurations.

## Features

- 🤖 **Multi-LLM Support**: Configure different LLM providers per topic
- 👥 **User Management**: Role-based access control (Admin/User)
- 📊 **Topic Management**: Create and manage classification topics with custom prompts
- 🔄 **Queue Processing**: Background task processing with MongoDB persistence
- 💾 **Smart Caching**: Reduce API calls with intelligent caching
- 📈 **Real-time Progress**: Track classification progress in real-time
- 🔐 **Secure Authentication**: JWT-based authentication with bcrypt password hashing

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Next.js   │────▶│   FastAPI   │────▶│   MongoDB   │
│  Frontend   │     │   Backend   │     │  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Worker    │
                    │   Process   │
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  LLM API    │
                    │  (OpenAI)   │
                    └─────────────┘
```

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **MongoDB**: Document database with Motor async driver
- **JWT**: Secure authentication
- **Bcrypt**: Password hashing
- **OpenAI SDK**: LLM integration

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Axios**: HTTP client
- **Lucide React**: Icon library

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 20+

### 1. Clone and Configure

```bash
git clone <repository>
cd kmlc

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### 2. Start Services

```bash
# Start all services
docker-compose -f docker-compose-fullstack.yml up -d

# Check status
docker-compose -f docker-compose-fullstack.yml ps
```

### 3. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

## Project Structure

```
.
├── backend/                 # FastAPI backend
│   ├── main.py             # Main API application
│   ├── auth.py             # Authentication logic
│   ├── auth_routes.py      # Auth endpoints
│   ├── topic_routes.py     # Topic endpoints
│   ├── database.py         # MongoDB operations
│   ├── models.py           # Pydantic models
│   ├── queue_worker.py     # Background worker
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   └── lib/           # Utilities
│   ├── package.json
│   └── tailwind.config.js
│
├── app/                    # Core classification engine
│   ├── core/
│   │   ├── classifier.py  # LLM classifier
│   │   ├── processor.py   # Batch processor
│   │   └── cache_manager.py
│   └── models/
│
├── docker-compose-fullstack.yml
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/change-password` - Change password
- `GET /api/auth/me` - Get current user
- `POST /api/auth/users` - Create user (Admin)
- `GET /api/auth/users` - List users (Admin)
- `DELETE /api/auth/users/{username}` - Delete user (Admin)

### Topics
- `POST /api/topics` - Create topic (Admin)
- `GET /api/topics` - List topics
- `GET /api/topics/{id}` - Get topic
- `PUT /api/topics/{id}` - Update topic (Admin)
- `DELETE /api/topics/{id}` - Delete topic (Admin)

### Tasks
- `POST /api/upload` - Upload file
- `POST /api/classify/{job_id}` - Start classification
- `GET /api/status/{job_id}` - Get task status
- `GET /api/tasks` - List tasks
- `DELETE /api/tasks/{job_id}` - Delete task
- `GET /api/download/{job_id}` - Download result

## Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Run Tests

```bash
# Test LLM inference
./test_llm_inference.sh

# Test backend
python backend/test_backend.py
```

## Configuration

### Environment Variables

```env
# LLM Configuration
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL=gpt-3.5-turbo

# Database
MONGODB_URL=mongodb://mongodb:27017
DATABASE_NAME=kmlc

# Security
SECRET_KEY=your-secret-key

# Processing
MAX_WORKERS=10
```

### Topic Configuration

Each topic can have its own:
- LLM provider and model
- API endpoint and key
- Custom prompt template
- Temperature and max tokens

## Deployment

### Production Checklist

- [ ] Change default admin password
- [ ] Set strong SECRET_KEY
- [ ] Configure production MongoDB
- [ ] Set up SSL/TLS
- [ ] Configure CORS properly
- [ ] Set up monitoring
- [ ] Configure backups

### Docker Production

```bash
# Build images
docker-compose -f docker-compose-fullstack.yml build

# Start services
docker-compose -f docker-compose-fullstack.yml up -d

# View logs
docker-compose -f docker-compose-fullstack.yml logs -f
```

## Monitoring

### Check Service Health

```bash
# Backend health
curl http://localhost:8000/

# Check containers
docker ps

# View logs
docker logs kmlc_backend
docker logs kmlc_worker
docker logs kmlc_frontend
```

## Troubleshooting

### Common Issues

**1. Frontend shows "Application error"**
- Clear browser cache (Ctrl+Shift+Delete)
- Try incognito mode
- Check browser console (F12)

**2. Tasks not processing**
- Check worker logs: `docker logs kmlc_worker`
- Verify MongoDB connection
- Check LLM API credentials

**3. Login fails**
- Verify MongoDB is running
- Check backend logs
- Ensure bcrypt is installed correctly

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Create an issue on GitHub
- Contact: support@kompa.ai
- Documentation: https://docs.kompa.ai

## Acknowledgments

- Built with FastAPI and Next.js
- Powered by OpenAI and compatible LLMs
- UI inspired by modern design principles
