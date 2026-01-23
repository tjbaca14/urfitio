# UrFitIO Backend Architecture Documentation

A Domain-Driven, Pattern-Based Architecture for AI and LLM Applications

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Architecture at a Glance](#architecture-at-a-glance)
4. [Domain Structure](#domain-structure)
5. [Design Patterns](#design-patterns)
6. [Key Architectural Decisions](#key-architectural-decisions)
7. [Detailed Documentation](#detailed-documentation)
8. [Development Guide](#development-guide)
9. [YouTube Series](#youtube-series)

---

## Overview

This documentation describes the architecture of UrFitIO's backend, a FastAPI-based application that demonstrates how traditional software engineering principles and design patterns apply to AI and LLM systems.

Core philosophy: AI applications are software systems first. They benefit from the same architectural principles that make traditional software maintainable and extensible.

Separation of responsibility is the foundation of successful AI systems. When responsibilities collapse, retrieval, orchestration, domain logic, persistence, infrastructure, and prompt behavior bleed into each other and the system becomes brittle and hard to evolve.

### Technology Stack

- Framework: FastAPI (async Python)
- Database: PostgreSQL with SQLAlchemy (async ORM)
- LLM: Anthropic Claude API (swappable via provider pattern)
- Validation: Pydantic
- Cache: In-memory

### Key Characteristics

- Domain-driven design with clear bounded contexts (NCAA, Chat, RAG, Common)
- Layered architecture: API to application to domain to repository to database
- Protocol-based interfaces using Python Protocols
- Generic RAG pipeline that remains domain-agnostic
- Dependency injection via FastAPI Depends
- Repository pattern with DTO-based data access

---

## High-Level System Requirements

At a minimum, this system must:

- Persist chat conversations reliably
- Retrieve historical conversations efficiently
- Provide a reusable RAG capability for context-aware responses
- Manage domain-specific content for the NCAA domain, including divisions, schools, and contextual data
- Interact with LLM providers through a swappable, well-defined interface

These requirements intentionally span multiple concerns:

- application orchestration
- domain modeling
- persistence
- retrieval
- external integrations

The architecture exists to keep these concerns explicit, isolated, and independently evolvable.

---

## Out of Scope

This project intentionally does not address:

- Authentication or authorization
- User management or identity workflows
- Frontend or UI architecture
- Multi-tenant access control
- Billing, quotas, or rate limiting

These concerns are excluded to keep the focus on AI system design rather than platform concerns.

---

## Separation of Responsibility in Prompts and Agentic Systems

Separation of responsibility is equally critical in prompt design and agentic implementations.

When responsibilities are unclear, prompts become overloaded. System instructions, domain rules, retrieval context, conversational state, and control flow get collapsed into a single prompt. This makes prompts brittle, opaque, and tightly coupled to implementation details.

This project treats prompts and agents as architectural artifacts rather than string templates.

In practice, this means:

- System prompts define behavior and constraints, not domain facts
- Domain context is injected deliberately rather than hard-coded into prompts
- Retrieval provides evidence, not instructions
- Agents orchestrate capabilities rather than embed logic inside prompts

By separating these concerns, prompts remain stable, agents remain composable, and changes to domain logic or retrieval strategy do not require rewriting instructions.

---

## Quick Start

### Understanding the System in 5 Minutes

1. **What it does**: Provides AI-powered chat about NCAA Division 1 baseball schools
2. **How it works**: User selects school → asks question → RAG retrieves context → LLM generates answer
3. **Why it's special**: Generic, reusable architecture that works for ANY domain (not just schools)

### Request Flow (High-Level)

```
User Question
    ↓
POST /api/v1/chats (ChatRequest)
    ↓
ChatApplicationService (orchestrates)
    ↓
RAGPipeline.generate()
    ├─→ Retrieve context (SchoolCacheService)
    ├─→ Augment prompt (PromptBuilder)
    └─→ Generate response (LLM Provider)
    ↓
Return Message
```

**See**: [High-Level Sequence Diagram](docs/diagrams/01-high-level-sequence.md)

---

## Architecture at a Glance

### Four Core Domains

```
┌─────────────────────────────────────────────────────────┐
│                    NCAA Domain                          │
│  Divisions + Schools (with context caching)             │
│  Routes: /api/v1/divisions, /api/v1/schools            │
└─────────────────────────────────────────────────────────┘
                           ↓ (provides context)
┌─────────────────────────────────────────────────────────┐
│                    RAG Domain                           │
│  Generic Retrieval-Augmented Generation pipeline        │
│  Works with ANY domain (schools, products, legal, etc.) │
└─────────────────────────────────────────────────────────┘
                           ↓ (consumed by)
┌─────────────────────────────────────────────────────────┐
│                    Chat Domain                          │
│  User conversations with RAG-powered responses          │
│  Routes: /api/v1/chats                                  │
└─────────────────────────────────────────────────────────┘
                           ↓ (uses)
┌─────────────────────────────────────────────────────────┐
│                    Common Domain                        │
│  Shared infrastructure (BaseRepository, Clients, DI)    │
└─────────────────────────────────────────────────────────┘
```

**See**: [Domain Architecture Diagram](docs/diagrams/06-domain-architecture.md)

### Seven Architectural Layers

1. **API Layer**: HTTP boundary (FastAPI routes, Pydantic models)
2. **Application Layer**: Use case orchestration (ChatApplicationService)
3. **Domain Layer**: Business logic (ConversationService, RAGPipeline, SchoolCacheService)
4. **Repository Layer**: Data access abstraction (ChatRepository, SchoolRepository)
5. **Database Layer**: Persistence (SQLAlchemy ORM models)
6. **Integration Layer**: External systems (BaseLLMProvider, AnthropicProvider)
7. **Infrastructure Layer**: Cross-cutting concerns (DI, HTTP client, cache)

**See**: [Layered Architecture Diagram](docs/diagrams/02-layered-architecture.md)

---

## Domain Structure

### 1. NCAA Domain (`app/ncaa/`)

**Purpose**: Manage NCAA divisions and schools

**Subdomains**:
- **Divisions**: CRUD for NCAA divisions (D1, D2, D3)
- **Schools**: School management with division relationships + context caching

**Key Service**: `SchoolCacheService` - Builds in-memory cache of school contexts for O(1) RAG retrieval

**API Routes**:
```
GET /api/v1/divisions              # List all divisions
GET /api/v1/divisions/{id}         # Get division by ID
GET /api/v1/schools                # List schools (filterable by division_id)
GET /api/v1/schools/{id}           # Get school by ID
```

**Database Schema**:
```
Division (id, division_type)
  └─1:N─→ School (id, name, division_id, context, created_date)
```

---

### 2. Chat Domain (`app/chat/`)

**Purpose**: Manage user chat conversations

**Components**:
- **ChatApplicationService**: Orchestrates chat feature (coordinates RAG + persistence)
- **ConversationService**: Handles conversation persistence logic
- **ChatRepository**: Data access for chat history

**API Routes**:
```
POST /api/v1/chats                 # Generate response (does NOT persist)
PUT  /api/v1/chats/{id}            # Save/update conversation
GET  /api/v1/chats/{id}            # Retrieve conversation
GET  /api/v1/chats/user/{user_id}  # List user's conversations
```

**Database Schema**:
```
ChatHistory (id, user_id, messages (JSON), created_date, updated_date)
Feedback (id, user_id, feedback, category, created_date)
```

**Design Decision**: Chat owns its persistence (not in Common domain) because conversation management is chat-specific business logic.

---

### 3. RAG Domain (`app/rag/`)

**Purpose**: Generic Retrieval-Augmented Generation pipeline

**Key Component**: `RAGPipeline` (Template Method Pattern)

**Algorithm** (fixed, with pluggable steps):
1. **Retrieve**: Get context via `Retriever` protocol
2. **Augment**: Format prompt via `PromptBuilder` protocol
3. **Ensure System Prompt**: Add system message if missing
4. **Generate**: Call LLM via `Generator` protocol

**Protocols (Interfaces)**:
```python
class Retriever(Protocol):
    async def retrieve(query: str) -> Optional[str]

class PromptBuilder(Protocol):
    def format_user_message(query: str, context: Optional[str]) -> str
    def get_system_prompt() -> str

class Generator(Protocol):
    async def generate(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> Message:
```

**Current Implementations**:
- `SchoolContextRetriever`: Retrieves school context from cache
- `DefaultPromptBuilder`: Wraps context in XML tags

**Why Generic?**: Same pipeline works for schools, products, legal docs, etc. - just inject different retriever/builder.

**See**: [RAG Abstraction Diagram](docs/diagrams/04-rag-abstraction.md)

---

### 4. Common Domain (`app/common/`)

**Purpose**: Shared infrastructure and cross-cutting concerns

**Key Components**:

#### BaseRepository[TModel, TDTO]
Generic CRUD with automatic DTO ↔ ORM conversion
```python
async def get_by_id(session, id_value) -> Optional[TDTO]
async def get_all(session, limit, offset, **filters) -> List[TDTO]
async def create(session, dto: TDTO) -> TDTO
async def update(session, dto: TDTO) -> TDTO
async def delete(session, id_value) -> bool
```

#### Clients
- **PostgresDB**: Async connection pool, context manager for sessions
- **HTTPClient**: Async httpx wrapper with centralized error handling
- **InMemoryCacheClient**: Pickle-based in-memory cache

#### Models
- **Message**: Universal format `{role: str, content: str}` used across Chat, RAG, LLM integrations
- **BaseDTOModel**: Pydantic base with `from_attributes=True` for ORM conversion

---

## Design Patterns

### 8 Core Patterns Applied

#### 1. **Dependency Injection**
**Where**: Throughout (FastAPI Depends)
**Why**: Loose coupling, easy testing, swappable implementations
```python
async def get_chat_application_service(
    rag_pipeline: RAGPipeline = Depends(get_rag_pipeline),
    conversation_service: ConversationService = Depends(get_conversation_service),
) -> ChatApplicationService:
    return ChatApplicationService(rag_pipeline, conversation_service)
```

#### 2. **Factory Pattern**
**Where**: `LLMProviderFactory`, RAG factory
**Why**: Configuration-driven provider selection
```python
provider_map = {
    "anthropic": AnthropicProvider,
    "openai": OpenAIProvider,  # Easy to add
}
```

#### 3. **Strategy Pattern**
**Where**: `LLMProvider` with multiple implementations
**Why**: Interchangeable LLM providers at runtime


#### 4. **Protocol Pattern**
**Where**: `Retriever`, `PromptBuilder`, `Generator`  protocols
**Why**: Structural typing without inheritance
```python
class Retriever(Protocol):
    async def retrieve(query: str) -> Optional[str]
```

#### 5. **Template Method**
**Where**: `RAGPipeline.generate()`
**Why**: Fixed algorithm with pluggable steps
```python
async def run(messages, context_key):
    context = await self.retriever.retrieve(context_key)  # Step 1
    augmented = self.prompt_builder.format(...)           # Step 2
    return await self.llm_provider.generate(...)          # Step 3
```

#### 6. **Repository Pattern**
**Where**: `BaseRepository`, domain-specific repositories
**Why**: Data access abstraction, DTO isolation from ORM
```python
class ChatRepository(BaseRepository[ChatHistory, ChatHistoryDTO]):
    # Inherits generic CRUD, adds domain-specific queries
    async def get_user_chats(session, user_id) -> List[ChatHistoryDTO]
```

#### 7. **Application Service Pattern**
**Where**: `ChatApplicationService`
**Why**: Orchestrates use cases across multiple domain services
```python
class ChatApplicationService:
    async def generate_response(chat_request):
        # Orchestrates: RAG pipeline (from RAG domain)
        return await self.rag_pipeline.generate(...)
```

#### 8. **Adapter Pattern**
**Where**: `AnthropicProvider`
**Why**: Translate between internal Message format and provider-specific API format
```python
class AnthropicProvider:
    def _to_anthropic_format(messages) -> List[dict]
    def _parse_response(response) -> Message
```

**See**: [Detailed Pattern Explanations](docs/diagrams/03-detailed-backend-sequence.md#pattern-catalog-why-each-pattern-exists)

---

## Key Architectural Decisions

### 1. NCAA as Unified Domain
**Decision**: Merge schools and divisions into single `ncaa/` domain

**Rationale**: Schools and divisions are tightly coupled (FK relationship), always deployed together, shared business context.

**Alternative Rejected**: Separate top-level domains - would create artificial boundary.

---

### 2. Chat Owns Conversation Persistence
**Decision**: Move `ConversationService` from `common/` to `chat/`

**Rationale**: Conversation persistence is chat domain concern, not generic infrastructure. Enables chat to evolve independently.

**Alternative Rejected**: Keep in `common/conversation/` as generic - not truly generic, specific to chat use case.

---

### 3. RAG Domain Owns RAG Instantiation
**Decision**: `rag/dependencies.py` assembles RAG pipeline, chat just consumes it

**Rationale**: RAG domain encapsulates implementation details. Chat doesn't need to know about retriever/builder composition.

**Alternative Rejected**: Chat assembles RAG components - leaks implementation details.

---

### 4. SchoolContextRetriever in RAG Domain
**Decision**: Retriever lives in `rag/retrievers/`, not `ncaa/schools/`

**Rationale**: Retriever is RAG infrastructure. NCAA exposes `SchoolCacheService`, retriever consumes it. Follows allowed dependency direction: RAG → NCAA.

**Alternative Rejected**: Put in `ncaa/schools/retrievers/` - would make NCAA depend on RAG concepts.

---

### 5. Protocols Over Abstract Base Classes
**Decision**: Use Python `Protocol` for interfaces

**Rationale**: Structural typing (duck typing with type safety), no inheritance required, easier to add new implementations.

**Alternative Rejected**: Abstract base classes - unnecessary inheritance hierarchy.

---

## Detailed Documentation

### Diagrams and Deep Dives

1. **[High-Level Sequence Diagram](docs/diagrams/01-high-level-sequence.md)**
   - Complete user journey from UI to database
   - Request/response flow
   - State management strategy

2. **[Layered Architecture](docs/diagrams/02-layered-architecture.md)**
   - 7 architectural layers explained
   - Dependency flow rules
   - Layer responsibilities and testing strategy
   - SOLID principles applied

3. **[Detailed Backend Sequence](docs/diagrams/03-detailed-backend-sequence.md)**
   - Complete request flow with pattern annotations
   - All 8 design patterns explained in detail
   - Dependency injection flow
   - Real-world impact examples

4. **[RAG Abstraction](docs/diagrams/04-rag-abstraction.md)**
   - Generic RAG architecture
   - Protocol-based design
   - Pluggable components (retrievers, builders, providers)
   - Why generic > special-cased

5. **[Anti-Pattern vs. Proper Abstraction](docs/diagrams/05-comparison-bad-vs-good.md)**
   - Side-by-side code comparison
   - Impact analysis (adding features, maintenance)
   - Testing complexity comparison
   - Maintenance over time

6. **[Domain Architecture](docs/diagrams/06-domain-architecture.md)**
   - Four-domain structure detailed
   - Cross-domain dependencies
   - Complete file structure
   - Future extension points

---

## Development Guide

### Adding a New Feature: OpenAI Support

**Goal**: Switch from Anthropic to OpenAI with minimal changes

**Steps**:
1. Create `app/integrations/llm/openai.py`:
   ```python
   class OpenAIProvider(BaseLLMProvider):
       async def generate(self, messages: List[Message]) -> Message:
           # OpenAI-specific implementation
           pass
   ```

2. Update factory (1 line):
   ```python
   provider_map = {
       "anthropic": AnthropicProvider,
       "openai": OpenAIProvider,  # Add this line
   }
   ```

3. Update `.env`:
   ```
   LLM_PROVIDER=openai
   ```

**Files Changed**: 1 new file, 1 line in existing file

**Files NOT Changed**: Routes, services, pipeline, repositories, tests

**Result**: Zero breaking changes, fully swappable at runtime.

---

### Adding a New Retriever: Vector DB

**Goal**: Add semantic search via vector database

**Steps**:
1. Create `app/rag/retrievers/vector_retriever.py`:
   ```python
   class VectorDBRetriever:  # No inheritance needed!
       async def retrieve(self, query: str) -> Optional[str]:
           embedding = await self.embedding_model.embed(query)
           results = await self.vector_db.search(embedding)
           return results[0].content if results else None
   ```

2. Update `app/rag/dependencies.py` (1 line):
   ```python
   # retriever = SchoolContextRetriever(cache)  # Old
   retriever = VectorDBRetriever(vector_db, embedding_model)  # New
   ```

**Files Changed**: 1 new file, 1 line in existing file

**Files NOT Changed**: RAGPipeline, ChatApplicationService, routes

**Result**: New retrieval strategy without touching core pipeline.

---

### Testing Strategy

#### Unit Tests
- **Domain Layer**: Test business logic with mocked repositories
- **Application Layer**: Test orchestration with mocked domain services
- **Repository Layer**: Test with in-memory/test database

#### Integration Tests
- **API Layer**: Full HTTP cycle with FastAPI TestClient
- **Database**: Real queries with test fixtures

#### Example: Testing RAGPipeline
```python
async def test_rag_pipeline():
    # Mock dependencies
    mock_retriever = Mock(spec=Retriever)
    mock_retriever.retrieve.return_value = "test context"

    mock_provider = Mock(spec=BaseLLMProvider)
    mock_provider.generate.return_value = Message(role="assistant", content="test")

    # Test with real pipeline, mocked components
    pipeline = RAGPipeline(
        retriever=mock_retriever,
        prompt_builder=PromptBuilder(),
        llm_provider=mock_provider,
    )

    result = await pipeline.generate([Message(role="user", content="test")])
    assert result.content == "test"
```

---

## YouTube Series

This architecture is the foundation for a YouTube series: **"Building Extensible AI Applications"**

### Series Theme
Traditional software design principles applied to AI/LLM systems - demonstrating how proper abstraction creates maintainable AI applications.

### Episode Topics
1. **The Cost of Special-Cased Design** - Anti-patterns and their consequences
2. **Layered Architecture** - Building the foundation
3. **Generic RAG Pipeline** - Template Method + Protocols
4. **LLM Provider Abstraction** - Factory + Strategy + Adapter
5. **Dependency Injection** - Wiring it all together
6. **Putting It All Together** - Complete request flow + extension points

---

## Project Structure

```
backend/
├── app/
│   ├── main.py                     # FastAPI app setup
│   ├── startup.py                  # Application container + lifespan
│   ├── settings.py                 # Configuration
│   │
│   ├── ncaa/                       # NCAA DOMAIN
│   │   ├── db_models.py            # Division, School ORM
│   │   ├── divisions/              # Divisions subdomain
│   │   │   ├── dependencies.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   └── service.py
│   │   └── schools/                # Schools subdomain
│   │       ├── dependencies.py
│   │       ├── models.py
│   │       ├── repository.py
│   │       ├── routes.py
│   │       └── service/
│   │           ├── cache_service.py
│   │           └── school_service.py
│   │
│   ├── chat/                       # CHAT DOMAIN
│   │   ├── dependencies.py
│   │   ├── repository.py
│   │   ├── routes.py
│   │   ├── models/
│   │   │   ├── db_models.py
│   │   │   └── dto.py
│   │   └── services/
│   │       ├── chat_application.py
│   │       └── conversation_store.py
│   │
│   ├── rag/                        # RAG DOMAIN
│   │   ├── dependencies.py
│   │   ├── factory.py
│   │   ├── pipeline.py             # RAGPipeline + Protocols
│   │   ├── prompt_builders/
│   │   │   └── default.py
│   │   └── retrievers/
│   │       └── school_retriever.py
│   │
│   ├── common/                     # COMMON DOMAIN
│   │   ├── dependencies.py
│   │   ├── models.py
│   │   ├── repository.py           # BaseRepository[T, DTO]
│   │   └── clients/
│   │       ├── cache.py
│   │       ├── db.py
│   │       └── http_client.py
│   │
│   └── integrations/               # INTEGRATIONS
│       └── llm/
│           ├── base.py             # BaseLLMProvider ABC
│           ├── anthropic.py
│           ├── factory.py
│           └── models.py
│
├── docs/                           # DOCUMENTATION
│   ├── business-requirements.md
│   ├── episode_1.md
│   ├── youtube-series-outline.md
│   └── diagrams/
│       ├── 01-high-level-sequence.md
│       ├── 02-layered-architecture.md
│       ├── 03-detailed-backend-sequence.md
│       ├── 04-rag-abstraction.md
│       ├── 05-comparison-bad-vs-good.md
│       ├── 06-domain-architecture.md
│       └── images/
│
└── README.md                      # You are here
```

---

## Benefits of This Architecture

### 1. Extensibility
- Add new domain: Create folder, implement interfaces
- Add new retriever: Implement `Retriever` protocol (no changes to pipeline)
- Add new LLM provider: Create provider class, add to factory (2 files)

### 2. Testability
- Each domain tested independently
- Mock cross-domain dependencies via interfaces
- Clear integration points

### 3. Maintainability
- Bug in chat persistence? Look in `chat/repository.py`
- Bug in school caching? Look in `ncaa/schools/service/cache_service.py`
- Bug in RAG? Look in `rag/pipeline.py`
- Single responsibility = single place to fix

### 4. Reusability
- RAG pipeline works for ANY domain (schools, products, legal, etc.)
- BaseRepository reusable across all domains
- Common clients reusable

### 5. Evolution
- NCAA domain can change without affecting chat
- Chat can change persistence without affecting RAG
- RAG can add retrievers without touching chat

---

## Key Takeaways

1. **AI applications are software first**: Traditional design principles (SOLID, DDD, patterns) apply and are MORE important with AI complexity.

2. **Generic > Special-Cased**: Upfront design investment pays dividends forever. Special-cased code feels faster initially but becomes a tar pit.

3. **Protocols > Inheritance**: Python Protocols provide interface benefits without inheritance hell.

4. **Composition > Configuration**: Dependency injection enables runtime composition without code changes.

5. **Separation of Concerns**: Clear domain boundaries + layered architecture = maintainable system.

6. **Test at the Right Level**: Domain logic tested in isolation, integration points tested with real dependencies.

---

## Contributing

When adding new features:
1. Identify which domain owns the feature
2. Follow existing patterns (DI, Repository, etc.)
3. Add tests at appropriate layer
4. Update relevant documentation

When refactoring:
1. Ensure changes stay within domain boundaries
2. Don't break abstractions
3. Add integration tests for cross-domain changes

---

## Questions?

- **Architecture questions**: See detailed diagrams in `docs/diagrams/`
- **Pattern questions**: See [Detailed Backend Sequence](docs/diagrams/03-detailed-backend-sequence.md#pattern-catalog-why-each-pattern-exists)
- **Domain questions**: See [Domain Architecture](docs/diagrams/06-domain-architecture.md)

---
