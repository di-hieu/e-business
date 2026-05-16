# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SC Chatbot is a multi-tenant AI chatbot platform for SMEs, featuring RAG-powered chatbot, social commerce channel integrations (Zalo, Facebook, Instagram, Telegram), and admin dashboard. Currently in POC phase using GPT-4o-mini and local embeddings.

## Architecture

```
src/backend/
├── api/              # FastAPI routes (chat, tools, knowledge, auth, admin, config, webhooks)
│   ├── __init__.py  # API router assembly
│   ├── app.py       # Configuration API endpoints
│   ├── admin.py     # Admin dashboard endpoints
│   ├── auth.py      # Authentication endpoints
│   ├── chat.py      # Chat messaging endpoints
│   ├── config.py    # Configuration API (NEW!)
│   ├── knowledge.py # Knowledge management endpoints
│   ├── tools.py     # Tool definition/execution endpoints
│   └── webhooks.py  # Zalo, Telegram, Facebook, Instagram webhook handlers
├── models/           # SQLAlchemy models (Tenant, User, Conversation, Message, KnowledgeDocument, ToolDefinition, ChatSession)
├── rag/              # RAG pipeline (FAISS + sentence-transformers embeddings)
├── services/         # Business logic (AuthService, ConfigService, ToolService)
└── main.py           # FastAPI app entry point
```

```
src/frontend/
├── src/
│   ├── App.jsx       # React router configuration
│   ├── api/client.js # Axios HTTP client
│   └── pages/        # Login, Dashboard, ChatInterface, Knowledge, Analytics, Settings
└── vite.config.js    # Vite configuration
```

```
test/
├── admin/            # Admin dashboard tests
├── channels/         # Channel integration tests (Zalo, Telegram, Facebook, Instagram)
├── conftest.py      # Shared fixtures (test_db, sample_tenant, sample_user, mock_llm, mock_tools)
├── fixtures/         # Test data
├── rag/              # RAG pipeline tests
├── tools/            # Function calling tests
├── tenants/          # Multi-tenant tests
└── load/             # Performance/load tests
```

## Key Patterns

### Multi-Tenancy
- `tenant_key` (unique identifier) + `tenant_id` (database primary key)
- All queries filter by `tenant_id`
- Configuration is tenant-scoped via `tenant_key`

### RAG Pipeline
- Uses `sentence-transformers/all-MiniLM-L6-v2` for embeddings (local, no API cost)
- FAISS vector store for similarity search
- `RAGPipeline` class handles: `load_knowledge()` → `retrieve_context()` → `generate_response()`
- Chunk size: 200 characters, overlap: 20 characters

### Configuration Management
- **Environment variables**: `.env.example` defines all config keys
- **UI-based config**: `ConfigService` supports fetching/saving via `/api/config/variables/` endpoint
- Sensitive configs (API keys) require admin authentication
- Cache in `_config_cache` dict for performance

### Webhooks
- `telegram_webhook`, `zalo_webhook`, `facebook_webhook`, `instagram_webhook` handlers
- All share common webhook pattern: validate → parse → route to chat handler
- Telegram uses `/webhooks/telegram` endpoint
- Zalo uses `/webhooks/zalo` endpoint

## Common Commands

### Development

```bash
# Start backend (dev mode)
make dev
# or
cd src/backend && uvicorn main:app --reload --port 8000

# Start frontend
make frontend
# or
cd src/frontend && npm run dev

# Start all services (Docker)
make docker-up
# or
docker-compose up -d

# Build Docker images
make build
# or
docker-compose build
```

### Testing

```bash
# Run all tests
make test
# or
pytest test/ -v

# Run tests with coverage
make test-cover
# or
pytest test/ --cov=src/backend --cov-report=html

# Run specific test file
pytest test/channels/test_telegram_channel.py -v
pytest test/admin/test_admin_dashboard.py -v

# Run tests with markers
pytest test/ -m "not slow"
pytest test/ -m "channel"
pytest test/ -m "rag"
pytest test/ -m "tools"
pytest test/ -m "poc"  # POC-specific tests

# Run E2E tests
pytest test/e2e/ -v
```

### Linting & Formatting

```bash
# Check linting
make lint
# or
flake8 src/backend/ --max-line-length=120
isort --check-only src/backend/

# Format code
make fmt
# or
isort src/backend/
black src/backend/
```

### Database

```bash
# Initialize database
make db-init
# or
cd src/backend && python -c "from models.database import init_db; import asyncio; asyncio.run(init_db())"

# Run migrations
make db-migrate
# or
alembic upgrade head
```

## API Endpoints

### Core
- `GET /` - Health check
- `GET /health` - Health endpoint
- `GET /metrics` - Basic metrics

### API (`/api/`)
- `POST /api/chat` - Send chat message
- `GET /api/knowledge` - List knowledge documents
- `POST /api/knowledge/upload` - Upload document
- `POST /api/tools/execute` - Execute custom tool
- `GET /api/tools` - List available tools
- `POST /api/config/variables` - Get/set config variables
- `GET /api/admin/tenants` - List tenants (admin only)

### Webhooks (`/webhooks/`)
- `POST /webhooks/telegram` - Telegram webhook handler
- `POST /webhooks/zalo` - Zalo OA webhook handler
- `POST /webhooks/facebook` - Facebook Messenger webhook handler
- `POST /webhooks/instagram` - Instagram Direct webhook handler

## Testing Guidelines

### Unit Tests
- Test individual functions/classes in isolation
- Use `pytest` with `--strict-markers`
- Mock external dependencies (LLM, database, HTTP clients)

### Integration Tests
- Test API endpoints with `TestClient`
- Use `conftest.py` fixtures (`sample_tenant`, `sample_user`, `mock_llm`, `mock_tools`)
- Test multi-tenant scenarios

### E2E Tests
- Use Playwright for browser automation
- Test full user flows (login → chat → upload knowledge)
- Test channel integrations end-to-end

### POC Tests
- Mark with `@pytest.mark.poc`
- Focus on core functionality validation
- May use mock data or simplified scenarios

## POC Success Criteria

- ✅ Chatbot responds intelligently using RAG from uploaded FAQs
- ✅ Can call at least 2 custom tools (check_inventory, track_order)
- ✅ Zalo Official Account integration working end-to-end
- ✅ **Telegram Bot integration working end-to-end**
- ✅ Docker Compose brings up full stack in < 2 minutes
- ✅ Admin can upload knowledge via basic UI
- ✅ Configuration can be managed via UI instead of editing `.env`

## Key Files to Reference

- `src/backend/main.py` - FastAPI app entry point
- `src/backend/models/database.py` - Database setup
- `src/backend/rag/pipeline.py` - RAG implementation
- `src/backend/services/config_service.py` - Configuration management
- `src/backend/api/webhooks.py` - Webhook handlers
- `test/conftest.py` - Shared test fixtures
- `test/channels/test_telegram_channel.py` - Telegram tests
- `test/pyproject.toml` - pytest configuration
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables reference

## Important Notes

- **Debug mode**: `DEBUG=True` in production requires changing to `DEBUG=False`
- **Database**: SQLite for POC, PostgreSQL planned for production
- **LLM**: GPT-4o-mini for POC, upgrade to GPT-4o or Claude later
- **Embeddings**: Local `all-MiniLM-L6-v2` for POC (free, no API costs)
- **Vector DB**: FAISS for POC, Qdrant planned for production
- **Frontend build**: `npm run build` produces production-ready bundle
- **API docs**: Available at `http://localhost:8000/docs`

## Recent Changes

- `src/backend/api/app.py` - Configuration API endpoints (NEW!)
- `src/backend/api/admin.py` - Admin dashboard endpoints
- `src/backend/api/webhooks.py` - Telegram webhook handler (NEW!)
- `test/channels/test_telegram_channel.py` - Telegram integration tests (NEW!)
- `src/frontend/src/pages/Settings.jsx` - Settings page with UI config (NEW!)
