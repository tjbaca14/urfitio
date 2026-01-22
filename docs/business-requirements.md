# Business Requirements Document (BRD)
## UrFitIO - NCAA Baseball Recruiting Intelligence Platform

**Version**: 1.0
**Date**: January 2026
**Status**: Active Development

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Business Problem](#business-problem)
3. [Business Objectives](#business-objectives)
4. [Target Users](#target-users)
5. [User Stories](#user-stories)
6. [Functional Requirements](#functional-requirements)
7. [Non-Functional Requirements](#non-functional-requirements)
8. [Scope](#scope)
9. [Assumptions and Constraints](#assumptions-and-constraints)
10. [Success Metrics](#success-metrics)
11. [Glossary](#glossary)

---

## Executive Summary

UrFitIO is an AI-powered platform that provides intelligent, grounded answers about NCAA Division 1 baseball coaches and schools. The system helps prospective student-athletes and their families make informed decisions about college recruiting by providing accurate, context-aware information through a conversational interface.

**Core Value Proposition**: Replace scattered, time-consuming research across multiple websites with a single, reliable, conversational interface that provides grounded answers backed by verified data.

---

## Business Problem

### Current State

Prospective student-athletes face significant challenges when researching college baseball programs:

1. **Information Fragmentation**: Data scattered across NCAA websites, school athletics pages, news articles, and recruiting forums
2. **Time-Intensive Research**: Families spend dozens of hours researching programs, coaches, and fit
3. **Information Overload**: Difficult to synthesize large amounts of information into actionable insights
4. **Staleness**: Information quickly becomes outdated (coaching changes, program updates)
5. **Inconsistency**: Different sources provide conflicting information
6. **Lack of Personalization**: No way to filter information relevant to specific player needs

### Pain Points

**For Student-Athletes**:
- "I don't know which schools match my skill level"
- "I can't find information about coaching style and philosophy"
- "I don't know if the academic programs align with my goals"
- "I'm overwhelmed by the number of options"

**For Parents**:
- "I want to verify information coaches are telling us"
- "I need to understand financial aid and scholarship opportunities"
- "I want to research program history and reputation"
- "I need to compare multiple schools efficiently"

**For Coaches/Advisors**:
- "I need quick access to program information to advise my athletes"
- "I want to provide data-backed recommendations"

---

## Business Objectives

### Primary Objectives

1. **Reduce Research Time**: Decrease time spent researching college programs by 70%
2. **Increase Information Accuracy**: Provide verifiable, grounded answers with source attribution
3. **Improve Decision Confidence**: Help families make informed decisions backed by data
4. **Enable Ongoing Discovery**: Allow users to explore programs over time, not just one-time research

### Secondary Objectives

1. **Build Trust**: Establish UrFitIO as the authoritative source for NCAA baseball recruiting intelligence
2. **Create Network Effects**: Enable users to save and share insights
3. **Gather Intelligence**: Understand common questions and information gaps in recruiting
4. **Platform for Expansion**: Build foundation for other sports, divisions, and recruiting services

---

## Target Users

### Primary Personas

#### 1. **Student-Athlete** (High School Junior/Senior)
- **Age**: 16-18
- **Goals**: Find the right fit (athletic, academic, social, financial)
- **Tech Savvy**: High (mobile-first, expects instant answers)
- **Pain Points**: Overwhelmed by options, unsure how to evaluate fit
- **Use Case**: Quick research during recruiting process, comparing offers

#### 2. **Parent**
- **Age**: 40-55
- **Goals**: Support child's decision, verify information, understand financial implications
- **Tech Savvy**: Medium (comfortable with web/mobile apps)
- **Pain Points**: Wants verification, concerned about cost, limited baseball knowledge
- **Use Case**: Deep research on program reputation, coach tenure, academic quality

#### 3. **High School Coach/Advisor**
- **Age**: 30-60
- **Goals**: Guide multiple athletes to appropriate programs
- **Tech Savvy**: Medium-High
- **Pain Points**: Limited time, needs quick access to program details for many schools
- **Use Case**: Bulk research across programs, providing recommendations to athletes

### Secondary Personas

#### 4. **Club/Travel Coach**
Similar to high school coach but may work with athletes across multiple years and regions.

#### 5. **Recruiting Consultant**
Professional advisor helping families navigate recruiting for a fee.

---

## User Stories

### Epic 1: School Discovery

**As a** student-athlete
**I want to** ask questions about specific schools
**So that** I can learn about programs that interest me

**Acceptance Criteria**:
- User can select a school from a list
- User can ask natural language questions about that school
- System provides accurate answers grounded in school data
- System cites sources where applicable

---

**As a** parent
**I want to** filter schools by division
**So that** I can focus on programs at the appropriate competitive level

**Acceptance Criteria**:
- User can view all NCAA divisions (D1, D2, D3)
- User can filter school list by selected division
- Filter persists across sessions

---

### Epic 2: Conversational Intelligence

**As a** user
**I want to** have a conversation about a school (multiple questions)
**So that** I can explore different aspects without starting over

**Acceptance Criteria**:
- User can ask follow-up questions in same conversation
- System maintains context across multiple turns
- User can reference previous questions ("What about academics?")
- Conversation history is preserved

---

**As a** user
**I want to** receive accurate, grounded answers
**So that** I can trust the information I'm getting

**Acceptance Criteria**:
- System only answers based on available data
- System explicitly states when it doesn't have information
- System does not hallucinate or make up facts
- Answers include context about the school

---

### Epic 3: Conversation Management

**As a** user
**I want to** save my conversations
**So that** I can return to them later

**Acceptance Criteria**:
- Conversations are automatically saved
- User can view list of past conversations
- User can resume a previous conversation
- Conversations include school context and timestamp

---

**As a** user
**I want to** see my recent conversations
**So that** I can quickly access schools I'm researching

**Acceptance Criteria**:
- User can view list of recent conversations (10 most recent)
- List shows school name and last message timestamp
- User can click to resume conversation
- List updates when new conversations are created

---

### Epic 4: Information Quality

**As a** user
**I want to** know when information might be outdated
**So that** I can verify with the school

**Acceptance Criteria**:
- System includes data freshness indicators (future enhancement)
- System prompts user to verify critical information (coaching changes, scholarships)

---

**As a** user
**I want to** provide feedback on answer quality
**So that** the system can improve

**Acceptance Criteria**:
- User can mark answer as helpful/not helpful
- User can categorize issues (incorrect, missing data, hallucination)
- User can provide optional notes
- Feedback is captured for analysis

---

## Functional Requirements

### FR-1: School and Division Management

**FR-1.1**: System shall provide a list of all NCAA baseball divisions (D1, D2, D3)

**FR-1.2**: System shall provide a list of schools within each division

**FR-1.3**: System shall allow filtering schools by division

**FR-1.4**: System shall allow searching schools by name (partial match)

**FR-1.5**: System shall display school details (name, division, basic info)

---

### FR-2: Conversational Interface

**FR-2.1**: System shall accept natural language questions via text input

**FR-2.2**: System shall maintain conversation context for multi-turn interactions

**FR-2.3**: System shall generate responses based on school-specific context

**FR-2.4**: System shall refuse to answer questions when data is insufficient

**FR-2.5**: System shall handle questions about:
- Coaching staff (names, tenure, philosophy)
- Program history (championships, conference standings)
- Facilities (fields, training facilities)
- Academic programs
- Location and campus information
- Recruiting priorities and needs

---

### FR-3: Context-Aware Responses (RAG)

**FR-3.1**: System shall retrieve relevant context based on selected school

**FR-3.2**: System shall augment user questions with retrieved context

**FR-3.3**: System shall generate answers using a Large Language Model (LLM)

**FR-3.4**: System shall ensure answers are grounded in provided context

**FR-3.5**: System shall format answers in a conversational, easy-to-read style

---

### FR-4: Conversation Persistence

**FR-4.1**: System shall automatically save conversations after each interaction

**FR-4.2**: System shall store:
- Unique conversation ID
- User ID
- School context
- Complete message history (user questions + assistant responses)
- Creation timestamp
- Last updated timestamp

**FR-4.3**: System shall allow users to retrieve conversation by ID

**FR-4.4**: System shall allow users to list their conversations (most recent first)

**FR-4.5**: System shall support pagination for conversation lists

**FR-4.6**: System shall allow resuming conversations with full context

---

### FR-5: User Feedback

**FR-5.1**: System shall allow users to provide feedback on responses

**FR-5.2**: System shall capture feedback type (helpful/not helpful)

**FR-5.3**: System shall allow users to categorize issues:
- Incorrect information
- Missing information
- Hallucination (answer not grounded in data)
- Other

**FR-5.4**: System shall allow optional free-form feedback notes

**FR-5.5**: System shall store feedback with:
- User ID
- Conversation ID
- Message ID
- Feedback category
- Notes
- Timestamp

---

### FR-6: Data Management

**FR-6.1**: System shall store school context data (coach info, program details, etc.)

**FR-6.2**: System shall support updating school context without downtime

**FR-6.3**: System shall cache frequently accessed school data for performance

**FR-6.4**: System shall support bulk import of school data

---

## Non-Functional Requirements

### NFR-1: Performance

**NFR-1.1**: Response Generation
- System shall generate responses within 5 seconds (95th percentile)
- System shall generate responses within 3 seconds (median)

**NFR-1.2**: Data Retrieval
- System shall retrieve school data within 100ms (99th percentile)
- School list shall load within 1 second

**NFR-1.3**: Conversation History
- Conversation list shall load within 2 seconds
- Individual conversation retrieval shall complete within 1 second

---

### NFR-2: Scalability

**NFR-2.1**: System shall support 100 concurrent users (Phase 1)

**NFR-2.2**: System shall support 1,000 concurrent users (Phase 2)

**NFR-2.3**: Database shall support storing 100,000+ conversations

**NFR-2.4**: System shall cache school context data to minimize database queries

---

### NFR-3: Reliability

**NFR-3.1**: System shall have 99% uptime during business hours (8am-8pm ET)

**NFR-3.2**: System shall handle LLM API failures gracefully (retry with exponential backoff)

**NFR-3.3**: System shall prevent data loss during conversation saves (transaction management)

**NFR-3.4**: System shall log all errors for debugging and monitoring

---

### NFR-4: Usability

**NFR-4.1**: Interface shall be intuitive for users ages 16-60

**NFR-4.2**: System shall provide clear error messages when issues occur

**NFR-4.3**: System shall indicate when processing (loading states)

**NFR-4.4**: System shall work on desktop and mobile browsers

**NFR-4.5**: System shall be accessible (WCAG 2.1 Level AA - future goal)

---

### NFR-5: Security

**NFR-5.1**: System shall require user authentication (future - Phase 2)

**NFR-5.2**: System shall prevent SQL injection via parameterized queries

**NFR-5.3**: System shall prevent prompt injection attacks

**NFR-5.4**: System shall not expose internal system details in error messages

**NFR-5.5**: System shall use HTTPS for all API communication

---

### NFR-6: Maintainability

**NFR-6.1**: System shall be modular to allow independent updates to components

**NFR-6.2**: System shall support swapping LLM providers without code rewrites

**NFR-6.3**: System shall log all user interactions for debugging

**NFR-6.4**: System shall have comprehensive API documentation

**NFR-6.5**: System shall follow coding standards (PEP 8 for Python, ESLint for TypeScript)

---

### NFR-7: Data Quality

**NFR-7.1**: System shall provide correct answers 90%+ of the time (measured via feedback)

**NFR-7.2**: System shall refuse to answer when data is insufficient (no hallucinations)

**NFR-7.3**: School context data shall be reviewed for accuracy before import

**NFR-7.4**: System shall track answer quality via user feedback

---

## Scope

### In Scope (Phase 1 - MVP)

1. **Division 1 Baseball Only**: Focus on NCAA Division 1 baseball programs
2. **Core Conversational Features**: Ask questions, receive answers, maintain context
3. **Conversation Management**: Save, retrieve, list conversations
4. **Basic School Data**: Coach information, program basics, location
5. **Desktop and Mobile Web**: Responsive web interface
6. **Feedback Collection**: Capture user feedback on answer quality

### In Scope (Phase 2 - Enhancement)

1. **Division 2 and Division 3**: Expand to all NCAA baseball divisions
2. **User Authentication**: User accounts, login, profile
3. **Advanced Filtering**: Filter schools by location, conference, academic ranking
4. **Comparison Features**: Side-by-side school comparisons
5. **Export/Share**: Export conversations, share insights
6. **Enhanced Data**: Recruiting timelines, scholarship info, recent news

### Out of Scope (Future Consideration)

1. **Other Sports**: Football, basketball, etc. (future expansion)
2. **Direct Messaging**: Messaging between users and coaches
3. **Application Management**: Tracking college applications
4. **Financial Aid Calculators**: Detailed cost/scholarship calculators
5. **Video Content**: Coach interviews, facility tours
6. **Mobile Native Apps**: iOS/Android native applications

---

## Assumptions and Constraints

### Assumptions

1. **Users have internet access**: System requires internet connectivity
2. **Users are comfortable with chat interfaces**: Familiarity with conversational UI
3. **School data is available**: We can source/create school context data
4. **LLM API availability**: Anthropic/OpenAI APIs are reliable and available
5. **Users speak English**: Initial launch is English-only
6. **Basic authentication**: User identification via simple ID (no login required for MVP)

### Constraints

#### Technical Constraints

1. **LLM Cost**: Each response costs $0.01-0.05, limiting free tier usage
2. **LLM Rate Limits**: API providers have rate limits (requests per minute)
3. **Context Window**: LLM has maximum context size (limits conversation length)
4. **Response Time**: LLM generation takes 2-5 seconds
5. **Data Freshness**: Manual updates to school data (not real-time)

#### Business Constraints

1. **Budget**: Limited budget for LLM API costs (must optimize usage)
2. **Team Size**: Small development team (1-3 developers)
3. **Timeline**: MVP target of 3-4 months
4. **Data Sources**: Reliant on public data sources (NCAA, school websites)

#### Regulatory Constraints

1. **Privacy**: Must comply with privacy regulations (COPPA for users under 13)
2. **Data Accuracy**: Must disclaim that information should be verified with schools
3. **Educational Use**: Cannot guarantee admission or recruiting outcomes

---

## Success Metrics

### User Engagement Metrics

1. **Daily Active Users (DAU)**: Target 100 DAU within 3 months of launch
2. **Messages per Session**: Target 5+ messages per session (indicates engagement)
3. **Return Rate**: Target 40% of users return within 7 days
4. **Conversation Completion**: Target 70% of conversations reach resolution

### Product Quality Metrics

1. **Answer Accuracy**: 90%+ positive feedback on answer quality
2. **Response Time**: 95% of responses generated within 5 seconds
3. **Uptime**: 99% availability during business hours
4. **Error Rate**: <1% of requests result in errors

### Business Metrics

1. **User Acquisition**: 500 registered users within 6 months (Phase 2)
2. **Cost per Query**: Maintain under $0.05 per query (LLM + infrastructure)
3. **User Satisfaction**: Net Promoter Score (NPS) of 50+
4. **Referral Rate**: 20% of users refer at least one other user

### Learning Metrics

1. **Top Questions**: Identify 10 most common question types
2. **Data Gaps**: Identify information users request but we don't have
3. **Feature Requests**: Track most requested features via feedback
4. **User Pain Points**: Identify top 5 user frustrations from feedback

---

## Glossary

**RAG (Retrieval-Augmented Generation)**: AI technique that retrieves relevant context before generating a response

**LLM (Large Language Model)**: AI model (like Claude, GPT-4) that generates human-like text

**Hallucination**: When an LLM generates factually incorrect information not grounded in provided context

**Grounded Answer**: Response based on retrieved data, not generated from LLM's training alone

**Context**: School-specific information provided to the LLM to generate accurate answers

**Prompt**: User's question or input to the system

**Turn**: One exchange in a conversation (user question + assistant response)

**Session**: Period of user activity, typically ends after 30 minutes of inactivity

**Conversation**: Multi-turn dialogue about a specific school, saved and retrievable

**Division**: NCAA classification (D1, D2, D3) based on school size and athletic budget

**Student-Athlete**: High school student pursuing collegiate athletics and academics

---

## Approval and Sign-Off

**Document Owner**: Product Manager
**Last Updated**: January 2026
**Next Review**: March 2026

**Stakeholder Approvals**:
- [ ] Product Manager
- [ ] Engineering Lead
- [ ] UX Designer
- [ ] Business Owner

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | Product Team | Initial BRD creation |

---

## Appendix

### Related Documents

- [Architecture Documentation](README.md)
- [YouTube Series Outline](youtube-series-outline.md)
- [Episode 1: Requirements to Architecture](episode_1.md)

### References

- NCAA Official Website
- College Baseball Recruiting Best Practices
- AI/LLM Application Design Patterns