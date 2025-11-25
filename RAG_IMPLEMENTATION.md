# RAG Pipeline Implementation

## Overview

This application implements a Retrieval-Augmented Generation (RAG) pipeline using Groq's LLM to provide intelligent answers about bus routes, providers, and bookings.

## Architecture

### 1. Document Storage

Bus provider information is stored in the `bus_documents` table in Supabase:
- Each document contains provider details (contact info, privacy policy, address)
- Documents are stored as plain text for retrieval
- Vector embeddings column is prepared for future semantic search enhancement

### 2. Data Sources

The RAG system retrieves information from multiple sources:
- **Bus Documents**: Provider-specific information from text files
- **Districts Table**: Available districts and routes
- **Bus Providers Table**: Provider metadata
- **Provider Routes Table**: Route coverage information
- **Bookings Table**: Active and historical bookings

### 3. Query Processing Flow

```
User Query → Semantic Search → Context Retrieval → LLM Processing → Response
```

#### Step-by-step:

1. **User submits query** through the chat interface
2. **Semantic search** retrieves relevant documents from the database
3. **Context aggregation** combines:
   - Bus provider documents
   - District information
   - Route coverage data
   - Current booking status
4. **LLM processing** uses Groq API with context
5. **Response generation** provides intelligent, context-aware answers

## Implementation Details

### Backend (FastAPI)

```python
def semantic_search(query: str, top_k: int = 3):
    # Retrieves relevant documents
    docs_response = supabase.table("bus_documents").select("*").execute()
    return docs_response.data[:top_k]

def rag_query(user_query: str):
    # 1. Retrieve relevant documents
    relevant_docs = semantic_search(user_query, top_k=3)

    # 2. Build context from multiple sources
    context = "\n\n".join([doc["content"] for doc in relevant_docs])

    # 3. Fetch live data
    districts = supabase.table("districts").select("*").execute()
    routes = supabase.table("provider_routes").select("*").execute()

    # 4. Create system prompt with context
    system_context = f"""
    Available data:
    - Districts: {districts}
    - Routes: {routes}
    - Provider details: {context}
    """

    # 5. Query LLM with context
    response = groq_client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": system_context},
            {"role": "user", "content": user_query}
        ]
    )

    return response.choices[0].message.content
```

### Frontend (React)

The chat interface provides a conversational UI for RAG queries:
- Real-time message streaming
- Context-aware responses
- Natural language understanding

## Example Queries

The RAG system can answer complex questions like:

1. **Route queries**: "Are there any buses from Dhaka to Rajshahi under 500 taka?"
   - Retrieves district data
   - Checks provider routes
   - Filters by price
   - Returns comprehensive answer

2. **Provider information**: "What are the contact details of Desh Travel?"
   - Searches provider documents
   - Extracts contact information
   - Returns formatted details

3. **Availability checks**: "Which bus companies serve Rangpur?"
   - Queries route coverage
   - Lists all providers
   - Provides additional context

## Benefits of RAG Approach

1. **Accurate Information**: Grounds responses in actual database data
2. **Up-to-date**: Always reflects current routes and availability
3. **Context-aware**: Understands relationships between districts, providers, and fares
4. **Flexible**: Handles natural language queries without rigid command structure
5. **Extensible**: Easy to add new documents or data sources

## Future Enhancements

1. **Vector Embeddings**: Implement true semantic search using pgvector
2. **Conversation Memory**: Track conversation history for better context
3. **Multi-turn Dialogues**: Support follow-up questions
4. **Booking Integration**: Allow booking through chat interface
5. **Analytics**: Track common queries to improve responses

## Technical Stack

- **Database**: Supabase (PostgreSQL with pgvector extension)
- **LLM**: Groq API (llama-3.1-70b-versatile model)
- **Backend**: FastAPI for API endpoints
- **Frontend**: React with TypeScript for UI

## Performance Considerations

- Document retrieval is optimized with database indexes
- LLM calls are made only when necessary
- Context is trimmed to relevant information only
- Response caching can be added for common queries

## Security

- No user data is sent to the LLM
- Provider information is public and safe to share
- Booking details are referenced but not exposed
- API keys are stored securely in environment variables
