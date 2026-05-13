# SC Chatbot - Social Commerce AI Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/react-18+-black.svg)](https://react.dev)

## 🌟 Overview

SC Chatbot is a production-ready, multi-tenant AI chatbot platform designed for SMEs to automate customer support and integrate seamlessly with social commerce channels (Zalo, Facebook Messenger, Instagram, and **Telegram**).

### 🎯 Mission

Build a production-ready, multi-tenant AI chatbot platform that enables SMEs to automate customer support and integrate seamlessly with social commerce channels (Zalo, Facebook, Instagram, **Telegram**).

### 🚀 Key Features

- **RAG-Powered Chatbot**: Intelligent responses using Retrieval-Augmented Generation
- **Multi-Channel Integration**: Zalo OA, Facebook Messenger, Instagram Direct, **Telegram**
- **Custom Tools**: Define and execute custom tools for business automation
- **Knowledge Management**: Upload FAQs, product docs, policies via UI
- **Admin Dashboard**: Track conversations, analytics, and manage settings
- **On-Premises Ready**: Deploy locally with Docker
- **Configurable via UI**: Manage tokens and settings through web interface (NEW!)

## 🏗️ Tech Stack (POC Phase)

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Backend | FastAPI (Python 3.11+) | Async-first, fast prototyping, auto docs |
| AI/LLM | LangChain + LangGraph | Industry standard for RAG + function calling |
| LLM Gateway | LiteLLM | Unified interface for OpenAI/OpenRouter/local models |
| LLM Model | GPT-4o-mini | Cost-effective for POC |
| Embeddings | all-MiniLM-L6-v2 (local) | Free, in-process, no API costs |
| Vector DB | FAISS (file-based) | Zero setup, embedded in Python |
| Database | SQLite + aiosqlite | Single file, no server needed |
| Frontend | React 18 + Vite | Fast dev server, modern React features |
| Deployment | Docker + Docker Compose | One command startup, portable |

## 📦 Installation

### Quick Start (Docker)

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd e-business

# 2. Copy and configure environment variables
cp .env.example .env
nano .env  # Fill in your API keys

# 3. Start all services
make docker-up

# 4. Access the application
# Backend API:    http://localhost:8000/docs
# Frontend:       http://localhost:3000
```

### Development Mode

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start backend
cd src/backend && uvicorn api.app:app --reload --port 8000

# In another terminal, start frontend
cd src/frontend && npm run dev
```

## 🔑 Getting Started

### 1. Register a New Tenant

Visit the frontend and register a new tenant:

```json
{
  "tenant_key": "my-company",
  "email": "admin@example.com",
  "password": "SecurePassword123!",
  "name": "My Company"
}
```

### 2. Configure LLM

Add your LLM API key to `.env`:

```env
LLM_API_KEY=your-openai-or-openrouter-api-key
LLM_MODEL=gpt-4o-mini
```

### 3. Upload Knowledge

- Go to **Knowledge** page
- Upload PDF, DOCX, or paste text content
- The system will automatically process and chunk documents
- Chatbot will use this knowledge for responses

### 4. Configure Tools

- Go to **Settings** → **Tools**
- Define custom tools (e.g., `check_inventory`, `track_order`)
- Provide JSON Schema for parameters
- Set the endpoint URL

### 5. Connect Zalo OA

1. Register Zalo Official Account at [Zalo Developer Portal](https://www.zalo.me/devapps)
2. Create a Zalo OA app
3. Configure webhook in Zalo OA console
4. Add Zalo credentials to `.env`:

```env
ZALO_APP_ID=your-app-id
ZALO_APP_SECRET=your-app-secret
ZALO_REDIRECT_URI=http://localhost:8000/auth/zalo/callback
```

### 6. Connect Telegram Bot (NEW!)

1. **Create a Telegram Bot**:
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` command
   - Follow instructions to create bot
   - Copy the bot token provided

2. **Add bot token to .env**:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

3. **Configure webhook** (optional, for production):
   ```env
   TELEGRAM_WEBHOOK_URL=https://your-domain.com/webhooks/telegram
   ```

4. **Set up webhook**:
   ```bash
   # Use Telegram's /setwebhook command
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -d "url=https://your-domain.com/webhooks/telegram"
   ```

5. **Test the bot**:
   - Open Telegram, find your bot
   - Send `/start`
   - Try asking questions!

### 7. Configure via UI (NEW!)

Instead of manually editing `.env`, you can configure settings via the web UI:

1. **Access Settings Page**:
   - Navigate to `http://localhost:3000/settings`
   - Select tenant from dropdown (or create new tenant)

2. **Configure Telegram Bot**:
   - Paste bot token in the **Configuration** tab
   - Click **Save Configuration**

3. **Configure other services**:
   - **Zalo**: Enter app ID, secret, and redirect URI
   - **Facebook**: Enter app ID and app secret
   - **Instagram**: Enter access token
   - **WeChat**: Enter app ID and app secret

4. **Upload Knowledge**:
   - Go to **Knowledge** tab
   - Upload PDF, DOCX, or paste text
   - Knowledge is automatically processed

5. **Define Tools**:
   - Go to **Tools** tab
   - Define custom tool with JSON Schema
   - Set endpoint URL and method

6. **View Analytics**:
   - Go to **Analytics** tab
   - View conversation stats and usage

**Benefits of UI Configuration**:
- No need to restart server after changing config
- Centralized management of all integrations
- Easy to test different configurations
- Audit trail for configuration changes

## 📁 Project Structure

```
e-business/
├── src/
│   ├── backend/
│   │   ├── api/               # API endpoints (chat, tools, knowledge, etc.)
│   │   │   ├── webhooks.py    # Zalo, Telegram, Facebook, Instagram
│   │   │   ├── chat.py        # Chat messaging
│   │   │   ├── tools.py       # Tool definitions and execution
│   │   │   ├── knowledge.py   # Knowledge management
│   │   │   ├── auth.py        # Authentication
│   │   │   ├── admin.py       # Admin endpoints
│   │   │   ├── config.py      # Configuration API (NEW!)
│   │   │   └── app.py         # Configuration API implementation
│   │   ├── models/            # SQLAlchemy models
│   │   ├── rag/               # RAG pipeline
│   │   ├── services/          # Business logic (incl. config service)
│   │   └── main.py           # FastAPI app entry
│   └── frontend/              # React + Vite frontend
├── test/                      # Python test suite
├── docs/                      # Project documentation
├── docker-compose.yml         # Multi-container orchestration
├── Dockerfile                 # Backend container definition
├── requirements.txt           # Python dependencies
├── Makefile                   # Development targets
└── README.md                  # This file
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run tests with coverage
make test-cover

# Run specific test file
pytest test/admin/test_login.py -v
```

## 📚 Documentation

For complete documentation, visit: [docs/table-of-contents.html](docs/table-of-contents.html)

Key documentation pages:
- [Getting Started Guide](docs/guides/getting-started.html)
- [Architecture Overview](docs/architecture/overview.html)
- [Technology Deep Dive](docs/architecture/tech-reference.html)
- [API Reference](docs/api-reference/mcp-server.html)
- [Deployment Guide](docs/deployment/docker.html)
- [Multi-Tenant Setup](docs/guides/multi-tenant-setup.html)
- [Channel Integration](docs/guides/channel-integration.html)
- [Function Calling Guide](docs/guides/function-calling.html)

## 🛠️ Available Commands

```bash
# Development
make dev              # Start backend
make frontend         # Start frontend

# Docker
make docker-up        # Start all services
make docker-down      # Stop all services
make build            # Build Docker images
make clean            # Remove containers and volumes

# Testing
make test             # Run tests
make lint             # Run linter
make fmt              # Format code

# Maintenance
make install          # Install dependencies
make db-init          # Initialize database
make docs             # Open documentation
```

## 📊 POC Success Criteria

The POC phase aims to validate:

- ✅ Chatbot responds intelligently using RAG from uploaded FAQs
- ✅ Can call at least 2 custom tools (e.g., check_inventory, track_order)
- ✅ Zalo Official Account integration working end-to-end
- ✅ **Telegram Bot integration working end-to-end** (NEW!)
- ✅ Docker Compose brings up full stack in < 2 minutes
- ✅ Admin can upload knowledge via basic UI
- ✅ **Configuration can be managed via UI instead of editing .env** (NEW!)

## 🔮 Roadmap

### Phase 1: POC (Current)
- [x] Docker Compose setup
- [ ] Zalo OA integration working end-to-end
- [ ] Telegram Bot integration working end-to-end (NEW!)
- [x] RAG chatbot with 2+ custom tools
- [x] Basic admin dashboard
- [x] Knowledge upload functionality
- [x] UI-based configuration (NEW!)

### Phase 2: MVP (Next 6 months)
- Facebook Messenger integration
- PostgreSQL + Redis infrastructure
- Full admin dashboard (analytics, user mgmt)
- .deb/.rpm packages for on-prem deployment

### Phase 3: Production (Future)
- Instagram Direct integration
- Billing & subscription system
- Multi-region AWS deployment
- 100+ tenants, 10,000+ daily active users

## ⚠️ Security Note

Before deploying to production:

1. **Change JWT_SECRET_KEY** in `.env` to a strong random value
2. **Set DEBUG=False** in `.env`
3. **Configure proper HTTPS** for webhook signatures
4. **Review all API keys** and rotate regularly

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

See [team/onboarding.html](docs/team/onboarding.html) for contribution guidelines.

## 📧 Contact

- **Project**: SC Chatbot
- **Email**: [Your email here]
- **GitHub**: [Your GitHub]

---

**For questions or support, please open an issue on GitHub.**