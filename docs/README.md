# SC Chatbot Documentation

This directory contains comprehensive documentation for the **SC Chatbot** (Social Commerce Chatbot) project - a production-ready, multi-tenant AI chatbot platform for SMEs.

## 📚 Documentation Structure

All documentation follows strict rules for consistency and accessibility:

- [x] **Self-contained HTML files**: Each document is a single HTML file with minimal CSS
- [x] **Central navigation**: Access all documents through `table-of-contents.html`
- [x] **Local server access**: Run `cd docs && python3 -m http.server 8888` to browse at http://localhost:8888

## 🎯 Project Overview: SC Chatbot

### Mission
Build a production-ready, multi-tenant AI chatbot platform that enables SMEs to automate customer support and integrate seamlessly with social commerce channels (Zalo, Facebook, Instagram).

### Target Market
Small and Medium Enterprises in Vietnam and Southeast Asia needing affordable, AI-powered customer service automation.

### Core Value Propositions
1. **Real AI chatbot** for customer support (RAG-powered, context-aware)
2. **Internal analysis tool** for business data insights
3. **Multi-channel integration**: Zalo OA (priority), Facebook Messenger, Instagram Direct
4. **Flexible deployment**: Cloud (AWS multi-tenant) or on-premises (.deb/.rpm packages)

## 🏗️ Architecture Overview

For a complete understanding of the system architecture and technology stack, see:
- 📁 **Architecture Overview**: `architecture/overview.html` - High-level architecture diagram and component overview
- 🛠️ **Technology Deep Dive**: `architecture/tech-reference.html` - Detailed explanations of every technology with code examples
- 📋 **Project Plan**: `plan.html` - Comprehensive roadmap with all epics and tasks

## 🛠️ Technology Stack - Detailed Explanations

For in-depth technical explanations of every technology used in this project, visit the **[Technology Deep Dive](architecture/tech-reference.html)** document.

### Core AI & LLM Technologies

#### RAG (Retrieval-Augmented Generation)
**What it is**: A technique that combines vector search with LLMs to provide accurate, context-aware responses. The system retrieves relevant documents from a vector database, injects them as context, and the LLM generates responses based on that context.

**Why we use it**: Enables chatbots to answer questions from proprietary documents (FAQs, product manuals, policies) without retraining the model. Provides factual, grounded responses.

#### LangChain & LangGraph
**What they are**: Frameworks for building LLM applications. LangChain handles the basics (prompt management, chaining), while LangGraph adds state-machine capabilities for complex multi-turn dialogues.

**Why we use them**: Industry standard for RAG and agent-based workflows. Provides modular components that can be composed like Lego bricks.

#### LiteLLM Gateway
**What it is**: A unified interface that abstracts away different LLM providers behind a single API contract.

**Why we use it**: Lets you swap LLM providers without changing code. Supports OpenAI, Anthropic, Cohere, Ollama, and hundreds more models via OpenRouter.

#### Vector Databases - FAISS vs Qdrant

**FAISS (File-based)**
- **What**: Facebook AI Similarity Search - file-based library for efficient vector search
- **When to use**: POC phase, <100k vectors per tenant, no external service needed
- **Pros**: Zero setup, embedded in Python, fast for small datasets
- **Cons**: No concurrent access control, limited scaling, single-tenant by default

**Qdrant (Production)**
- **What**: Cloud-native vector DB with managed service option
- **When to use**: Production, multi-tenant, >100k vectors, advanced filtering needed
- **Pros**: Multi-tenant support, metadata filtering, clustering, cloud options
- **Cons**: Requires separate service, more complex setup

#### Embedding Models
**all-MiniLM-L6-v2 (POC)**: Lightweight, runs locally, ~50MB size, free, no API costs

**OpenAI text-embedding-3-small (Production)**: Higher quality, faster inference on cloud

#### Database Technologies

**SQLite (POC)**: Embedded database, zero configuration, ideal for development and testing

**PostgreSQL (Production)**: Full-featured relational DB with concurrent connections, JSONB, full-text search

#### Caching & Rate Limiting

**functools.lru_cache (POC)**: Decorator-based automatic caching

**TTL dict (In-memory)**: Simple key-value store with time-to-live

**Redis (Production)**: Distributed cache with persistence and pub/sub

#### Async Task Processing

**FastAPI BackgroundTasks (POC)**: Built-in mechanism for simple async tasks

**Celery + Redis/RabbitMQ (Production)**: Distributed task queue for long-running jobs

## 📋 Feature Roadmap

All features below are **planned but not yet implemented**.

### ✅ Epic 1: Multi-Channel Messaging Integration
- [ ] Zalo Official Account API (receive/send messages, templates, rich media)
- [ ] Facebook Messenger (webhook, quick replies, persistent menu)
- [ ] Instagram Direct (basic messaging) - *lower priority*
- [ ] Pluggable channel adapter pattern
- [ ] Webhook signature verification

### ✅ Epic 2: Conversational AI & Knowledge
- [ ] LLM-powered FAQ using RAG from vector database
- [ ] Product consultation (retrieve from crawled data)
- [ ] Semantic product search (natural language queries)
- [ ] Dynamic context memory (last 10 exchanges per session)
- [ ] Multi-turn dialog handling (complex flows)
- [ ] Vector database per tenant (data isolation)
- [ ] Automated knowledge crawler (website scraping, embedding)
- [ ] Manual knowledge import (PDFs, CSV, text via UI)

### ✅ Epic 3: Function Calling & Transactional Tasks
- [ ] Tool definition framework (admins define via UI)
- [ ] Dynamic function calling (LLM decides when to call)
- [ ] Information gathering loop (ask for missing parameters)
- [ ] Order creation & sync to OMS (Haravan, Shopify)
- [ ] Order tracking (status queries)
- [ ] Stock checking by region (inventory API)
- [ ] Booking/reservation (tours, appointments)

### ✅ Epic 4: Administration & Multi-Tenancy
- [ ] Tenant onboarding flow (signup, workspace, API keys)
- [ ] User roles (Super Admin, Tenant Admin, Agent)
- [ ] Conversation dashboard (browse, search, export)
- [ ] Knowledge base manager (add/edit FAQ, upload docs)
- [ ] Tool configurator (define, test custom tools)
- [ ] Analytics & reports (response time, conversion, CSAT, token cost)
- [ ] Billing & plans (usage-based or subscription) - *future*
- [ ] Audit logs (track all changes)

### ✅ Epic 5: External AI Agent Access (MCP Server)
- [ ] MCP server implementation (Model Context Protocol)
- [ ] Agent-friendly endpoints (`POST /mcp/query`)
- [ ] Authentication for MCP (API keys per tenant)

### ✅ Epic 6: Webhook & Real-time Data Sync
- [ ] Incoming webhook receiver (tenant pushes real-time data)
- [ ] Event-triggered notifications (proactive messaging)

### ✅ Epic 7: Non-Functional & Infrastructure
- [ ] Multi-tenant isolation (tenant_id in all queries)
- [ ] High availability (AWS multi-AZ deployment)
- [ ] Response time SLA (p95 < 1 second)
- [ ] Rate limiting (per tenant, per user, per IP)
- [ ] Observability (Prometheus, Grafana, OpenTelemetry)
- [ ] Security (HTTPS, input sanitization, secrets vault)
- [ ] Backup & DR (daily DB backups, cross-region replication)

### ✅ Epic 8: Development & Deployment Artifacts
- [ ] Makefile (dev, build, test, docker targets)
- [ ] Dockerfile and Docker Compose
- [ ] systemd unit files (backend, crawler, admin)
- [ ] Packaging automation (.deb/.rpm via fpm)
- [ ] CI/CD pipeline (GitHub Actions or GitLab CI)

## 📖 Documentation Guidelines

### When Creating/Updating Documentation:

1. **Self-contained HTML files**: Each doc must be standalone with embedded CSS
2. **Minimal CSS**: Use inline styles or small embedded `<style>` block
3. **Central navigation**: All nav links reference `table-of-contents.html`
4. **Organized structure**: Files go in subfolders:
   - `api-reference/` - API endpoints, schemas
   - `architecture/` - System design, tech decisions (includes Technology Deep Dive)
   - `deployment/` - Docker, on-prem, cloud guides
   - `guides/` - How-to guides (multi-tenant, knowledge, tools, channels)
   - `tutorials/` - Step-by-step tutorials
   - `team/` - Onboarding, security, monitoring

5. **Back-to-top link**: Every page includes link to `table-of-contents.html`

6. **Badge system**: Use consistent badges:
   - `badge-poc` (light blue) - POC phase features
   - `badge-mvp` (light purple) - MVP phase features
   - `badge-prod` (light green) - Production phase features
   - `badge-planned` (light orange) - Planned features

7. **Concise content**: Maximum 2-3 scrolls per page (avoid overwhelming)

8. **Preserve structure**: Always maintain existing content structure when updating

9. **Rich technical explanations**: For AI/ML technologies, include:
   - What the technology is
   - Why we chose it
   - How it works (with diagrams/code examples)
   - Pros/cons comparison
   - Production upgrade path

## 🎯 Development Phases

### Phase 1: POC (3 months) - **Currently 5% Complete**
**Goal**: Validate core AI capabilities

**Key Deliverables**:
- Docker Compose setup
- Zalo OA integration working end-to-end
- RAG chatbot with 2+ custom tools
- Basic admin dashboard
- Knowledge upload functionality

### Phase 2: MVP (6 months) - **Planned**
**Goal**: Production-ready multi-tenant platform

**Key Deliverables**:
- .deb/.rpm packages for on-prem
- Facebook Messenger integration
- Full admin dashboard (analytics, user mgmt)
- Monitoring (Prometheus + Grafana)
- PostgreSQL + Redis infrastructure
- 10+ tenants supported

### Phase 3: Production (12 months) - **Planned**
**Goal**: Enterprise-grade platform at scale

**Key Deliverables**:
- Instagram Direct integration
- Billing & subscription system
- Multi-region AWS deployment
- 100+ tenants, 10,000+ daily active users
- SLA: 99.9% uptime, p95 < 500ms
- GDPR/SOC 2 compliance

## 🔑 Critical Success Factors

1. **Vietnamese market first**: Zalo is priority #1 (200M+ users)
2. **Keep POC simple**: Use simplest stack to move fast (SQLite, FAISS, Docker)
3. **Early validation**: Get 3-5 pilot customers by end of POC
4. **Cost-conscious**: Use GPT-4o-mini for POC, optimize with local models later
5. **On-prem differentiator**: Many Vietnamese SMEs prefer on-prem → .deb/.rpm essential
6. **AI quality monitoring**: Track RAG accuracy, tool success rate, user satisfaction
7. **Multi-tenancy from day 1**: Tenant isolation cannot be retrofitted

## 📚 Quick Links

- **Project Plan**: [plan.html](plan.html) - Comprehensive roadmap with all epics and tasks
- **Table of Contents**: [table-of-contents.html](table-of-contents.html) - Central navigation hub
- **Architecture Overview**: [architecture/overview.html](architecture/overview.html) - System design and architecture diagrams
- **Technology Deep Dive**: [architecture/tech-reference.html](architecture/tech-reference.html) - Detailed explanations of every technology with code examples and comparisons
- **Getting Started**: [guides/getting-started.html](guides/getting-started.html) - Quick start guide
- **Docker Deployment**: [deployment/docker.html](deployment/docker.html) - Container setup

## 🤝 Contributing

See [team/onboarding.html](team/onboarding.html) for:
- Team roles (Super Admin, Tenant Admin, Agent)
- Contribution guidelines
- Code style (PEP 8 for Python)
- Testing requirements
- Commit conventions (feat:, fix:, docs:)

## 📊 Technical Glossary

### RAG (Retrieval-Augmented Generation)
A framework that enables LLMs to access external knowledge sources. The system retrieves relevant documents and provides them as context for the model to generate accurate, fact-based responses.

### LangChain
An open-source framework for developing applications powered by language models. Provides building blocks for chains, agents, and memory.

### LangGraph
An extension to LangChain that enables creating stateful, multi-actor applications with cyclic behavior. Essential for conversation memory and agent workflows.

### FAISS (Facebook AI Similarity Search)
A library for efficient similarity search and clustering of dense vectors. Ideal for POC with small-scale deployments.

### Qdrant
A cloud-native vector similarity engine optimized for low latency and high throughput. Supports filtering, metadata storage, and clustering.

### MCP (Model Context Protocol)
An open protocol for connecting AI models to external tools and data sources. Enables standardized integration with third-party services.

### Vector Database
A database that stores and queries data in vector format (embeddings). Enables semantic search based on meaning rather than exact keyword matching.

### Embeddings
Numerical representations of text that capture semantic meaning. Similar texts have similar vector representations, enabling similarity search.

### Function Calling
A capability where LLMs can identify when to call external functions/tools and what parameters to pass. Enables automation of complex workflows.

### Multi-Tenancy
Architecture pattern where a single instance serves multiple customers (tenants), with data logically isolated per tenant.

### Webhook
Callback mechanism where the server pushes data to a client URL when an event occurs. Enables real-time event-driven architecture.

### Docker Compose
Tool for defining and running multi-container applications. Simplifies development and testing with single-file configuration.

### Rate Limiting
Mechanism to restrict API request frequency. Protects against abuse and manages resource allocation fairly.

### Token Bucket Algorithm
Rate limiting strategy where requests consume tokens from a bucket that refills over time. Smoothes traffic bursts.

### Celery
Distributed task queue based on Python, message passing, and worker processes. Handles long-running tasks asynchronously.

### Redis
In-memory data structure store used for caching, session storage, and message queues. Provides sub-millisecond access.

### PostgreSQL
Advanced relational database with JSONB support, full-text search, and row-level security. Production-ready for multi-tenant scenarios.

### SQLAlchemy
Python SQL toolkit and ORM. Provides database abstraction, migrations (Alembic), and connection pooling.

### FastAPI
Modern web framework for building APIs with Python. Provides automatic docs, async support, and type hints.

### React
JavaScript library for building user interfaces. Virtual DOM, component-based, and declarative.

### Vite
Next-generation frontend tooling. Provides instant server start, HMR, and optimized builds.

## 📝 Project Metadata

- **Project Name**: SC Chatbot (Social Commerce Chatbot)
- **Target**: SMEs in Vietnam & Southeast Asia
- **Current Phase**: POC (5% complete)
- **Tech Stack**: Python + FastAPI, React + Vite, LangChain, Docker
- **Deployment**: Cloud (AWS) & On-premises (.deb/.rpm)
- **Last Updated**: May 2026

---

**For the complete project plan with detailed epics and tasks**, see [plan.html](plan.html).

**For browsing all documentation**, start at [table-of-contents.html](table-of-contents.html).

**For detailed technology explanations**, visit [architecture/tech-reference.html](architecture/tech-reference.html).