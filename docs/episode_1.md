# Episode 1 — From Business Requirements to Architecture

## What This Episode Covers

In this episode, we will:

* Define the business requirements for our product
* Identify the hidden complexity behind those requirements
* Translate requirements into a high-level system architecture
* Establish design principles that guide the rest of the series

---

## 1. Problem Statement

We are building a system that provides intelligent, grounded answers about Division 1 baseball coaches.

A user should be able to:

* Select a school or coach
* Ask questions about that coach
* Receive answers grounded in known data
* Continue conversations over time

The challenge is not answering a single question — it’s building a system that can evolve without constant rewrites.

---

## 2. Primary User Flows

### 2.1 Start a Conversation

* User selects a school or coach
* User asks a question
* System returns an answer grounded in context

### 2.2 Continue a Conversation

* User returns later
* User loads a previous chat
* User asks follow-up questions in the same thread

### 2.3 Browse Conversation History

* User can list recent conversations
* User can retrieve a specific conversation by ID

---

## 3. Functional Requirements

### 3.1 Context Selection

* System must accept a context selector (school or coach)
* Context must influence retrieval and answer grounding

### 3.2 Question Answering

* System must:

  * Use retrieved context when available
  * Avoid hallucinating beyond known data
  * Explicitly state when it cannot answer from context

### 3.3 Conversation Persistence

* System must store:

  * Chat ID
  * User ID
  * Message history
  * Timestamps
* System must support:

  * Save conversation after each turn
  * Retrieve conversation by chat ID
  * List recent conversations for a user

### 3.4 Conversation Retrieval

* Retrieve full conversation history
* Support pagination or limits for recent chats

### 3.5 Feedback (Optional but Recommended)

* Capture:

  * Helpful / not helpful
  * Category (incorrect, missing data, hallucination)
  * Optional free-form notes

---

## 4. Non-Functional Requirements

### 4.1 Correctness and Grounding

* Answers must be grounded and explainable
* System must refuse to answer when data is insufficient

### 4.2 Maintainability

* Architecture must support:

  * Swapping LLM providers
  * Changing retrieval strategies
  * Evolving prompt formats
  * Adding new domains

### 4.3 Extensibility

Future capabilities should be possible without redesign:

* Vector search
* Hybrid retrieval
* Streaming responses
* Tool calling
* Multi-tenant support

### 4.4 Observability (MVP)

* Log major lifecycle events
* Enable basic tracing and debugging

---

## 5. What Makes This Hard?

This problem is deceptively complex:

* Context changes per conversation
* Conversations are long-lived
* LLMs are external, slow, and non-deterministic
* We want flexibility without duplication
* We want correctness without over-coupling

This is why architecture matters.

---

## 6. Architectural Principles

Before drawing diagrams, we establish principles:

1. Architecture follows business flows, not folder structure
2. Coordination is not business logic
3. The RAG pipeline must be domain-agnostic
4. Persistence is separate from generation
5. Anything that varies belongs behind an abstraction

These principles guide every design decision.

---

## 7. High-Level System Flow

A single request flows through the system as:

UI → API → Orchestrator → RAG Pipeline → LLM
Persistence happens alongside the flow (store/retrieve conversation history)

Key points:

* The backend is stateless between requests
* The client drives the conversation flow
* Persistence is triggered explicitly

This flow explains what happens, not how it is implemented.

---

## 8. Layered Architecture Overview

### API Layer

* HTTP boundary
* Validation and serialization
* No business logic

### Orchestration Layer

* Coordinates use cases
* Owns flow, not rules
* Delegates work

### Business Logic Layer

* Domain rules
* Prompt construction
* Context resolution

### Repository Layer

* Data access only
* No business decisions

### Integration Layer

* External systems (LLMs, APIs)
* Provider-specific logic
* Protocol translation

### Infrastructure Layer

* Dependency injection
* Configuration
* Cross-cutting concerns

Each layer has one reason to change.

---

## 9. What We Are Intentionally Not Covering Yet

Out of scope for this episode:

* Prompt engineering
* Agent frameworks
* RAG internals
* Vector databases
* Authentication and session management

These will be introduced only when they solve a real problem.

---

## 10. Anti-Pattern Preview

A common failure mode:

* Hard-coding chat logic per domain
* Duplicating orchestration logic
* Binding business logic directly to an LLM provider

This leads to fragile systems and slow iteration.

We will contrast this with proper abstraction later in the series.

---

## 11. Episode Summary

In this episode we:

* Defined real business requirements
* Exposed hidden complexity
* Established architectural principles
* Designed a high-level, extensible system

No code yet — just decisions.

---

## 12. What’s Next

In Episode 2, we will:

* Trace a single chat request end-to-end
* Walk through the orchestrator
* Introduce the generic RAG pipeline
* Show how persistence fits without leaking concerns

---
