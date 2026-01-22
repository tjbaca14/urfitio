# Diagram 1: High-Level Chat Sequence Flow

## Complete User Journey: From UI Interaction to Persistent Storage

```mermaid
sequenceDiagram
    actor User
    participant Browser as Client (React)
    participant API as Backend API
    participant RAG as RAG Pipeline
    participant LLM as LLM Provider
    participant DB as PostgreSQL

    Note over User,DB: New Conversation Flow

    User->>Browser: Selects Division & School
    activate Browser
    Browser->>Browser: Store context selection (Zustand)
    Note right of Browser: Context: "Stanford"

    User->>Browser: Types first message
    Browser->>Browser: Generate UUID for chat
    Note right of Browser: chatId: "abc-123"

    Browser->>Browser: Optimistic UI update
    Note right of Browser: Message appears immediately

    Browser->>API: POST /api/v1/chats
    Note right of Browser: ChatRequest payload

    activate API
    API->>RAG: process_chat(request)
    activate RAG

    RAG->>RAG: Retrieve context from cache
    Note right of RAG: O(1) lookup: "Stanford" → context

    RAG->>RAG: Augment prompt with context
    Note right of RAG: Wraps context in data tags

    RAG->>LLM: generate(augmented_messages)
    activate LLM
    LLM->>LLM: Call external LLM API
    LLM-->>RAG: Message(role="assistant", content="...")
    deactivate LLM

    RAG-->>API: Assistant response
    deactivate RAG

    API-->>Browser: ChatResponse (Message)
    deactivate API

    Browser->>Browser: Add assistant message to state
    Browser->>User: Display response
    deactivate Browser

    Note over User,DB: Persist Conversation

    Browser->>API: PUT /api/v1/chats/abc-123
    Note right of Browser: Full conversation history
    activate API
    API->>DB: UPSERT chat_history
    activate DB
    DB-->>API: Success
    deactivate DB
    API-->>Browser: Saved ChatHistoryDTO
    deactivate API

    Note over User,DB: Continuing Conversation (Subsequent Messages)

    User->>Browser: Types follow-up message
    Browser->>Browser: Append to messages array
    Browser->>API: POST /api/v1/chats
    Note right of Browser: Same chatId with full history

    activate API
    API->>RAG: process_chat(request)
    Note right of RAG: Context can be re-retrieved
    RAG->>LLM: generate(messages)
    LLM-->>RAG: Response
    RAG-->>API: Message
    API-->>Browser: ChatResponse
    deactivate API

    Browser->>API: PUT /api/v1/chats/abc-123
    API->>DB: UPDATE chat_history
    DB-->>API: Success
    API-->>Browser: Updated DTO
```

## Key Design Decisions Illustrated

### 1. **Client-Side ID Generation**
- **Why**: Enables optimistic updates, offline support, reduces coupling
- **Trade-off**: Must handle ID collisions (UUID v4 makes this negligible)

### 2. **Optimistic UI Updates**
- **Why**: Instant feedback, perceived performance
- **Trade-off**: Must handle rollback on error (currently TODO)

### 3. **Full Message History in Request**
- **Why**: Backend is stateless, client controls conversation context
- **Trade-off**: Larger payloads (mitigated: JSON compression, reasonable limits)

### 4. **Separate Save Operation**
- **Why**: Decouples generation from persistence, allows retry logic
- **Trade-off**: Two API calls (could be combined, but separation is cleaner)

### 5. **Context as Query Parameter**
- **Why**: Generic abstraction - "contextQuery" could be school, document ID, user ID, etc.
- **Pattern**: Dependency Inversion - client doesn't know what context means

## State Management Strategy

```
┌─────────────────────────────────────────────┐
│              Client State                    │
├─────────────────────────────────────────────┤
│                                              │
│  Zustand Store (In-Memory + LocalStorage)   │
│  ├─ currentChatId                            │
│  ├─ messages[] ◄────────┐                   │
│  ├─ selectedDivision     │                   │
│  └─ selectedSchool       │                   │
│                          │                   │
│  React Query (Server State Cache)           │
│  ├─ ['chat', chatId] ────┘ Hydrates on load │
│  ├─ ['chats', userId]    Cached queries     │
│  └─ ['divisions']        24hr TTL           │
│                                              │
└─────────────────────────────────────────────┘
                     │
                     │ Persists to
                     ↓
┌─────────────────────────────────────────────┐
│          Backend Persistence                 │
├─────────────────────────────────────────────┤
│                                              │
│  PostgreSQL: chat_history table              │
│  ├─ id (PK)                                  │
│  ├─ user_id (FK, indexed)                   │
│  ├─ messages (JSON[])  ◄─ Source of truth   │
│  ├─ created_date                             │
│  └─ updated_date                             │
│                                              │
└─────────────────────────────────────────────┘
```

**Why this architecture?**
- **Client state is disposable** - can be rebuilt from backend
- **Backend is source of truth** - enables multi-device sync
- **Cache invalidation strategy** - React Query handles staleness
- **LocalStorage for UX only** - Remembers user preferences, not data
