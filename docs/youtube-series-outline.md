# YouTube Series: Building Extensible AI Applications

## Series Theme
**"Traditional Software Design Principles Applied to AI/LLM Systems"**

Demonstrating how proper abstraction, generic design, and classic software patterns create maintainable AI applications - not special-cased, hard-to-maintain code.

---

## Target Audience
- Software engineers building AI/LLM applications
- Teams struggling with maintainability of AI codebases
- Developers wanting to apply traditional SE principles to AI use cases

---

## Series Structure: 6 Episodes × 15-20 Minutes

---

### **Episode 1: The Cost of Special-Cased Design**
**Duration**: 15-17 minutes
**Focus**: Problem statement & architecture principles

#### Content Outline:
1. **Opening Hook** (2 min)
   - Show common pattern: "Let me just add Anthropic API calls here"
   - Fast forward 6 months: 5 duplicated services, impossible to maintain
   - **Thesis**: "Most AI apps fail due to poor abstraction, not technical limits"

2. **Anti-Pattern Walkthrough** (5 min)
   - Live code example: `SchoolChatService`, `ProductChatService`, etc.
   - Highlight code duplication
   - Show real scenarios:
     - "Switch to OpenAI" → Must rewrite 5 services
     - "Change prompt format" → Update 12 string literals
     - "Add caching" → Modify every service
   - **Key point**: "Each service is a liability, not an asset"

3. **High-Level Architecture Preview** (5 min)
   - Show Diagram 1: High-level sequence flow
   - Introduce layers: API → Orchestration → RAG → Integrations
   - Contrast with special-cased: "One pipeline vs. N services"
   - **Principle**: Separation of Concerns

4. **Design Principles Overview** (3 min)
   - SOLID principles apply to AI
   - Dependency Inversion: Depend on abstractions (BaseLLMProvider, not AnthropicProvider)
   - Open/Closed: Open for extension, closed for modification
   - Single Responsibility: Each layer has one reason to change

5. **Episode Close** (2 min)
   - Preview: "Next episode, we build the foundation"
   - Call to action: "Think about YOUR codebase - which pattern does it follow?"

**Key Takeaway**: Special-cased AI code is a maintenance nightmare; proper abstraction is not "over-engineering"

---

### **Episode 2: Layered Architecture - Building the Foundation**
**Duration**: 18-20 minutes
**Focus**: Architecture layers & dependency flow

#### Content Outline:
1. **Recap & Setup** (2 min)
   - Quick recap: Special-cased vs. generic
   - Today's goal: "Build the skeleton that supports everything"

2. **Layered Architecture Deep Dive** (8 min)
   - Show Diagram 2: Layered architecture
   - Walk through each layer:
     - **API Layer**: HTTP → Domain translation (routes.py)
     - **Orchestration Layer**: Coordination (ChatOrchestrator, RAGPipeline)
     - **Business Logic**: Domain rules (ConversationService, PromptBuilder)
     - **Repository Layer**: Data access (ChatRepository, BaseRepository)
     - **Database Layer**: Persistence (SQLAlchemy models)
     - **Integration Layer**: External systems (BaseLLMProvider)
     - **Infrastructure Layer**: Cross-cutting (DI, config, HTTP client)

   - **Key points**:
     - Dependency flow: Top → Down only
     - Each layer tested independently
     - Forbidden: Bottom → Top dependencies

3. **Live Code Walkthrough** (7 min)
   - Start with `main.py` → Application lifecycle
   - Show `startup.py` → Dependency injection container
     - Initialize HTTP client, DB, LLM provider, cache
     - Store in app.state
   - Show `dependencies.py` → FastAPI Depends() pattern
   - Show `routes.py` → Minimal route logic (just delegates)

   - **Emphasize**:
     - Routes don't know about LLM providers
     - Services don't know about HTTP
     - Clear boundaries = easy testing

4. **Testing Strategy** (2 min)
   - Show test for API layer (integration test with test client)
   - Show test for service layer (unit test with mocked repository)
   - **Benefit**: Each layer tested in isolation

5. **Episode Close** (1 min)
   - Recap: Layers separate concerns
   - Preview: "Next episode, the heart of the system - the RAG pipeline"

**Key Takeaway**: Layers enforce boundaries; boundaries enable testing and maintenance

---

### **Episode 3: Generic RAG Pipeline - The Heart of the System**
**Duration**: 18-20 minutes
**Focus**: RAG abstraction & Template Method pattern

#### Content Outline:
1. **Opening** (2 min)
   - What is RAG? (Retrieve → Augment → Generate)
   - Why generic? "This pipeline works for schools, products, legal docs, anything"

2. **RAG Algorithm Walkthrough** (5 min)
   - Show Diagram 4: RAG pipeline flow
   - Walk through `rag/pipeline.py`:
     - **Step 1: Retrieve** - Get context (Protocol interface)
     - **Step 2: Augment** - Add context to prompt (PromptBuilder)
     - **Step 3: Ensure System** - Prepend system message if needed
     - **Step 4: Generate** - Call LLM (Strategy interface)

   - **Key point**: Fixed algorithm, pluggable components (Template Method)

3. **Retriever Protocol** (4 min)
   - Show Protocol definition: `async def retrieve(query: str) -> Optional[str]`
   - Show implementations:
     - `ContextRetriever` (cache-based, O(1))
     - `VectorDBRetriever` (semantic search)
     - `HybridRetriever` (cache + vector)

   - **Benefit**: Swap retrieval strategy without touching pipeline
   - Live demo: Change from cache → vector DB (1 line in DI config)

4. **PromptBuilder** (3 min)
   - Show `prompt_builder.py`:
     - `format_user_message()` - Pure function
     - `get_system_prompt()` - Configurable

   - **Why separate?**
     - Prompt changes don't affect pipeline logic
     - Easy to A/B test prompts
     - Could have different builders per domain

5. **Live Demo: Adding New Domain** (4 min)
   - Scenario: "We have school chat, now add product chat"
   - Special-cased: Copy-paste 200 lines
   - Generic design:
     - Create `ProductRetriever` (implements Protocol)
     - Inject into pipeline
     - Done! Same endpoint, same pipeline

   - Show code side-by-side

6. **Episode Close** (2 min)
   - Recap: Generic RAG = one implementation, infinite domains
   - Preview: "Next episode, we tackle the trickiest part - LLM provider abstraction"

**Key Takeaway**: Template Method + Protocols = flexible, reusable RAG pipeline

---

### **Episode 4: LLM Provider Abstraction - Factory + Strategy Patterns**
**Duration**: 18-20 minutes
**Focus**: Provider abstraction, Factory, Strategy, Adapter patterns

#### Content Outline:
1. **The Problem** (2 min)
   - "Anthropic API changed → broke 12 files"
   - "Want to use OpenAI → must rewrite everything"
   - **Solution**: Abstract the provider interface

2. **Strategy Pattern** (5 min)
   - Show Diagram 3 (LLM provider section)
   - Define `BaseLLMProvider` (ABC):
     ```python
     async def generate(self, messages: List[Message]) -> Message
     ```
   - **Key**: Generic Message format (not provider-specific)

   - Show `AnthropicProvider`:
     - Translate Message → Anthropic format
     - Call Anthropic API
     - Translate response → Message

   - **Benefit**: Pipeline doesn't know which provider it's using

3. **Adapter Pattern** (4 min)
   - Deep dive into `anthropic.py`:
     - `_separate_system_messages()` (Anthropic quirk)
     - `_to_anthropic_format()` (Message → Anthropic JSON)
     - `_parse_response()` (Anthropic JSON → Message)

   - Show HTTPClient wrapper (centralized error handling)

   - **Key point**: Provider-specific logic contained in adapter

4. **Factory Pattern** (4 min)
   - Show `llm/factory.py`:
     ```python
     provider_map = {
         "anthropic": AnthropicProvider,
         "openai": OpenAIProvider,
     }
     ```
   - `create(config)` selects provider based on config

   - **Benefit**: Adding OpenAI = 1 new file + 1 line in factory

5. **Live Demo: Adding OpenAI Provider** (3 min)
   - Create `openai.py` (~80 lines)
   - Add `"openai": OpenAIProvider` to factory
   - Change env: `LLM_PROVIDER=openai`
   - Run same request → works!

   - Show diff: 0 changes to existing files

6. **Episode Close** (2 min)
   - Recap: Factory + Strategy + Adapter = swappable providers
   - Preview: "Next episode, we wire it all together with dependency injection"

**Key Takeaway**: Proper abstraction makes provider changes trivial

---

### **Episode 5: Dependency Injection - Wiring It All Together**
**Duration**: 16-18 minutes
**Focus**: DI pattern, testing benefits, composition

#### Content Outline:
1. **The Problem** (2 min)
   - Hard-coded dependencies = impossible to test
   - "To test chat, must spin up DB + Anthropic API" ❌

2. **Dependency Injection Fundamentals** (4 min)
   - Show anti-pattern:
     ```python
     class ChatOrchestrator:
         def __init__(self):
             self.llm_provider = AnthropicProvider()  # Tight coupling!
     ```

   - Show proper DI:
     ```python
     class ChatOrchestrator:
         def __init__(self, llm_provider: BaseLLMProvider):
             self.llm_provider = llm_provider  # Injected!
     ```

   - **Benefit**: Can inject mock in tests, real provider in prod

3. **FastAPI Depends() Pattern** (5 min)
   - Show `dependencies.py`:
     ```python
     async def get_llm_provider(request: Request) -> BaseLLMProvider:
         return request.app.state.llm_provider

     async def get_chat_orchestrator(
         llm_provider: BaseLLMProvider = Depends(get_llm_provider),
         cache: dict = Depends(get_cache),
     ) -> ChatOrchestrator:
         return ChatOrchestrator(llm_provider, cache)
     ```

   - Show route using it:
     ```python
     @app.post("/chats")
     async def post_chat(
         request: ChatRequest,
         orchestrator: ChatOrchestrator = Depends(get_chat_orchestrator),
     ):
         return await orchestrator.process_chat(request)
     ```

   - **Benefit**: Route doesn't create dependencies, just receives them

4. **Application Lifecycle** (3 min)
   - Show `startup.py`:
     - `lifespan()` context manager
     - Initialize all singletons (HTTP client, DB, LLM provider, cache)
     - Store in app.state
     - Cleanup on shutdown

   - **Pattern**: Application Container (DI Container)

5. **Testing Benefits** (3 min)
   - Show test with DI:
     ```python
     async def test_chat_endpoint(test_client):
         mock_provider = Mock(spec=BaseLLMProvider)
         mock_provider.generate.return_value = Message(...)

         # Override dependency
         app.dependency_overrides[get_llm_provider] = lambda: mock_provider

         response = await test_client.post("/chats", json={...})
         assert response.status_code == 200
     ```

   - **Zero** Anthropic API calls in tests!

6. **Episode Close** (1 min)
   - Recap: DI = loose coupling = testability
   - Preview: "Final episode, we put it all together and see the full picture"

**Key Takeaway**: Dependency injection is the glue that makes everything testable

---

### **Episode 6: Putting It All Together - Request Flow & Extension Points**
**Duration**: 20-22 minutes (finale, slightly longer)
**Focus**: Complete request flow, real-world scenarios, future extensions

#### Content Outline:
1. **Opening** (2 min)
   - "We've built all the pieces. Now let's see them work together."
   - Recap journey: Layers → RAG → Providers → DI

2. **Complete Request Flow** (6 min)
   - Show Diagram 3: Detailed backend sequence
   - Walk through EVERY step of a real request:
     1. POST /api/v1/chats
     2. Route resolves dependencies (DI)
     3. ChatOrchestrator.process_chat()
     4. RAGPipeline.generate():
        - Retriever.retrieve() (Protocol)
        - PromptBuilder.format_user_message()
        - BaseLLMProvider.generate() (Strategy)
     5. Return Message

   - **Highlight every pattern applied**:
     - 💉 Dependency Injection
     - 🏭 Factory
     - 🎯 Strategy
     - 🔌 Protocol
     - 🏗️ Builder
     - 🎭 Facade
     - 🔄 Adapter
     - 📋 Template Method

3. **Real-World Scenarios** (6 min)

   **Scenario 1: Switch from Anthropic to OpenAI**
   - Files changed: 1 line in `.env` (`LLM_PROVIDER=openai`)
   - Show it working!

   **Scenario 2: Add Vector Database Retrieval**
   - Create `VectorDBRetriever` (new file)
   - Change DI injection (1 line)
   - Show same pipeline, different retrieval

   **Scenario 3: A/B Test Prompts**
   - Create `ExperimentalPromptBuilder`
   - Inject based on user segment
   - Zero changes to pipeline

   **Scenario 4: Add Streaming Responses**
   - Add `stream()` method to `BaseLLMProvider`
   - Implement in `AnthropicProvider` and `OpenAIProvider`
   - Pipeline: `response = await provider.stream(messages) if streaming else await provider.generate(messages)`
   - **Show flexibility**

4. **Extension Points** (4 min)
   - What can you add without modifying existing code?
     - New LLM providers (Cohere, Mistral, local LLMs)
     - New retrieval strategies (hybrid, graph-based, API-based)
     - New prompt formats (few-shot, structured output)
     - Middleware (logging, caching, rate limiting)
     - New domains (products, legal, medical)

   - **Key principle**: Open/Closed Principle in action

5. **Comparison: Maintenance Over Time** (3 min)
   - Show Diagram 5: Anti-pattern vs. proper abstraction
   - Timeline:
     - **Day 1**: Special-cased feels faster (copy-paste)
     - **Month 3**: First cracks (5 duplicate services)
     - **Month 6**: Maintenance nightmare (bug requires 5 fixes)
     - **Year 1**: Rewrite discussions start

   vs.

     - **Day 1**: Generic requires design thinking
     - **Month 3**: Adding domains is trivial
     - **Month 6**: Bug fix = one line
     - **Year 1**: Still maintainable, team happy

6. **Closing Thoughts** (2 min)
   - **Core lesson**: "Traditional software design principles don't become obsolete with AI"
   - SOLID, design patterns, separation of concerns → **more important than ever**
   - AI makes codebases complex; proper abstraction makes them manageable

   - **Call to action**:
     - Review your AI codebase - which pattern does it follow?
     - Refactor toward abstraction (even incrementally)
     - Share this series with your team

   - **Final message**: "Build AI apps like you'd build any production system - with care, abstraction, and maintainability in mind."

**Key Takeaway**: Proper abstraction is an investment that pays dividends forever

---

## Recurring Themes Across Episodes

1. **Show, Don't Just Tell**
   - Every principle backed by code examples
   - Side-by-side comparisons (bad vs. good)
   - Live demos where possible

2. **Emphasize Trade-offs**
   - Upfront design cost vs. long-term maintenance savings
   - Abstraction adds code, but reduces complexity
   - "Is this over-engineering?" → "No, this is planning for change"

3. **Real-World Scenarios**
   - "Switch providers" (happens often)
   - "Change prompts" (happens constantly)
   - "Add new domain" (business growth)
   - "Bug in prompt formatting" (maintenance)

4. **Pattern Recognition**
   - Annotate diagrams with pattern names
   - Explain WHY each pattern exists
   - Show what happens WITHOUT the pattern

5. **Incremental Adoption**
   - "You don't have to rewrite everything"
   - "Start with one abstraction (provider)"
   - "Gradually refactor toward clean architecture"

---

## Visual Style Guidelines

1. **Diagrams**:
   - Use Mermaid diagrams (included in docs)
   - Color-code layers consistently
   - Annotate with pattern names
   - Show data flow clearly

2. **Code Examples**:
   - Syntax highlighting
   - Side-by-side comparisons (split screen)
   - Highlight changed lines
   - Use ❌ / ✅ for bad/good patterns

3. **On-Screen Text**:
   - Key principles as overlays
   - Pattern names when they appear
   - Trade-offs as callout boxes

---

## Engagement Hooks

1. **Opening Hook** (Every episode):
   - Relatable problem ("Have you ever had to change every LLM call in your app?")
   - Quick preview of solution

2. **Mid-Episode Engagement**:
   - "Pause here - how would YOU solve this?"
   - "Comment below - which pattern are you excited to try?"

3. **Closing Hook** (Every episode):
   - Cliffhanger for next episode
   - Call to action (comment, share, subscribe)

---

## Downloadable Resources

Provide in video descriptions:

1. **GitHub Repository**:
   - Full codebase
   - Commit history showing evolution
   - Branch per episode

2. **Diagram Files**:
   - All Mermaid diagrams
   - Editable formats

3. **Cheat Sheet**:
   - Pattern catalog
   - When to use each pattern
   - Common anti-patterns to avoid

4. **Refactoring Guide**:
   - Step-by-step: special-cased → generic
   - Testing strategy
   - Migration checklist

---

## Success Metrics

Track for each episode:

1. **Engagement**:
   - View duration (target: >70% completion)
   - Comments asking questions
   - Shares within engineering communities

2. **Impact**:
   - GitHub repo stars/forks
   - Questions about applying to other domains
   - "I refactored my app using this" testimonials

3. **Community Building**:
   - Discord/Slack channel for discussions
   - Office hours or live Q&A follow-up
   - Guest episodes (other engineers using these patterns)

---

## Post-Series Ideas

1. **Bonus Episodes**:
   - "Testing Strategies for AI Applications"
   - "Observability in Generic RAG Pipelines"
   - "Scaling to Multiple LLMs Simultaneously"

2. **Case Studies**:
   - Interview teams using similar architectures
   - Before/after maintenance costs

3. **Advanced Topics**:
   - Agent orchestration (multi-step reasoning)
   - Multi-modal pipelines (text + images)
   - Fine-tuning management

---

## Final Thoughts

This series is about **changing mindset**:
- From "AI is different, normal rules don't apply"
- To "AI is software, and software needs good architecture"

The goal is not to teach specific frameworks, but to teach **thinking** - how to:
- Identify what varies vs. what stays constant
- Design interfaces before implementations
- Compose systems from reusable pieces
- Plan for change, not just current requirements

If developers finish this series and think "I need to refactor my AI app," that's success. 🎯
