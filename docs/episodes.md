## Episode 1 – Scope and Architecture

- Define the problem the system is solving  
- Clarify scope and non-goals  
- Identify core responsibilities  
- Establish the high-level architecture  

## Episode 2 – Boundaries and Responsibilities

- Identify the major system capabilities  
- Separate application orchestration from infrastructure  
- Define generic capabilities vs domain-specific behavior  
- RAG as a reusable capability  
- Conversation persistence as a generic service  
- LLM provider pattern as an integration boundary  

## Episode 3 – RAG as a Capability, Not a Feature

- Define what a generic RAG pipeline should own  
- Retriever and prompt builder as extension points  
- How domain logic plugs into RAG  
- Why RAG should not know about chat, schools, or APIs  

## Episode 4 – Domain Modeling and Data Access

- Model divisions, schools, and relationships  
- Decide when to enforce hierarchy vs flexibility  
- Separate read models from write models  
- Place caching and data access correctly  

## Episode 5 – Designing for Change and Extension

- Trace an end-to-end request through the system  
- Add new domains or retrieval strategies cleanly  
- Understand how requirements impact architecture  
- Recognize when abstractions need to evolve  
