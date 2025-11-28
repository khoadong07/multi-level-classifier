# Contributing to KMLC

Thank you for your interest in contributing to Kompa MultiLevel Classifier!

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- Git

### Local Development

1. **Fork and Clone**
```bash
git clone https://github.com/your-username/kmlc.git
cd kmlc
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

4. **Start Services**
```bash
# Start MongoDB
docker-compose -f docker-compose-fullstack.yml up -d mongodb

# Start backend
cd backend
uvicorn main:app --reload

# Start frontend (in another terminal)
cd frontend
npm run dev
```

## Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints
- Write docstrings for functions
- Keep functions small and focused

```python
def process_task(task_id: str) -> dict:
    """
    Process a classification task.
    
    Args:
        task_id: Unique task identifier
        
    Returns:
        dict: Task result with status and stats
    """
    pass
```

### TypeScript (Frontend)
- Use TypeScript strict mode
- Follow React best practices
- Use functional components with hooks
- Keep components small and reusable

```typescript
interface Props {
  taskId: string
  onComplete: (result: TaskResult) => void
}

export default function TaskProcessor({ taskId, onComplete }: Props) {
  // Component logic
}
```

## Commit Messages

Follow conventional commits:

```
feat: add user export functionality
fix: resolve authentication timeout issue
docs: update API documentation
refactor: simplify task processing logic
test: add unit tests for classifier
chore: update dependencies
```

## Pull Request Process

1. Create a feature branch
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes
3. Write/update tests
4. Update documentation
5. Commit with clear messages
6. Push and create PR

```bash
git push origin feature/your-feature-name
```

7. Fill out PR template
8. Wait for review

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
./test_llm_inference.sh
```

## Documentation

- Update README.md for user-facing changes
- Update API docs for endpoint changes
- Add inline comments for complex logic
- Update CHANGELOG.md

## Questions?

- Open an issue for bugs
- Start a discussion for features
- Contact maintainers for urgent matters

Thank you for contributing! 🎉
