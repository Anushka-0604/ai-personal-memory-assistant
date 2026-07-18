# Phase 6 APIs – Conversational AI

Phase 6 introduced a complete conversational layer to the AI Personal Memory & Decision Assistant. New APIs were added for managing chat sessions, storing conversation history, and interacting with the AI assistant.

---

# 1. Create Chat Session

## Endpoint

POST /chat/sessions

## Description

Creates a new chat session for the authenticated user.

## Authentication

Required (JWT Bearer Token)

## Request Body

```json
{
    "title": "Machine Learning Notes"
}
```

## Success Response

```json
{
    "id": 1,
    "title": "Machine Learning Notes",
    "created_at": "...",
    "updated_at": "..."
}
```

---

# 2. Get All Chat Sessions

## Endpoint

GET /chat/sessions

## Description

Returns all chat sessions belonging to the authenticated user.

## Authentication

Required

## Success Response

```json
[
    {
        "id": 1,
        "title": "Machine Learning Notes",
        "created_at": "...",
        "updated_at": "..."
    }
]
```

---

# 3. Get Chat Session

## Endpoint

GET /chat/sessions/{session_id}

## Description

Returns details of a specific chat session.

## Authentication

Required

## Path Parameter

session_id

---

# 4. Rename Chat Session

## Endpoint

PUT /chat/sessions/{session_id}

## Description

Updates the title of an existing chat session.

## Authentication

Required

## Request Body

```json
{
    "title": "Deep Learning Discussion"
}
```

## Success Response

```json
{
    "id": 1,
    "title": "Deep Learning Discussion"
}
```

---

# 5. Delete Chat Session

## Endpoint

DELETE /chat/sessions/{session_id}

## Description

Deletes the selected chat session and its associated messages.

## Authentication

Required

---

# 6. Get Chat Messages

## Endpoint

GET /chat/sessions/{session_id}/messages

## Description

Returns the complete conversation history for a chat session in chronological order.

## Authentication

Required

## Success Response

```json
[
    {
        "role": "user",
        "content": "Hello"
    },
    {
        "role": "assistant",
        "content": "Hi! How can I help you?"
    }
]
```

---

# 7. Chat with AI

## Endpoint

POST /chat

## Description

Main conversational endpoint used by the AI assistant.

This endpoint automatically:

- Saves the user message.
- Loads previous conversation history.
- Performs semantic search on stored memories.
- Applies similarity threshold filtering.
- Builds the Retrieval-Augmented Generation (RAG) prompt.
- Sends the prompt to the Gemini LLM.
- Saves the assistant response.
- Returns the final answer.

## Authentication

Required

## Request Body

```json
{
    "session_id": 1,
    "question": "What is my favourite programming language?",
    "top_k": 5
}
```

## Success Response

```json
{
    "answer": "Your favourite programming language is Python.",
    "retrieved_memories": [
        {
            "content": "My favourite programming language is Python.",
            "similarity": 0.92
        }
    ]
}
```

---

# API Workflow

The conversational API follows the workflow below:

1. Authenticate user using JWT.
2. Validate chat session ownership.
3. Store the user's message.
4. Retrieve previous conversation history.
5. Perform semantic search over stored memories.
6. Filter memories using the similarity threshold.
7. Build the prompt using conversation history and retrieved memories.
8. Generate a response using Gemini.
9. Save the assistant response.
10. Return the final response.

---

# Security

All conversational APIs require JWT authentication.

Every request validates that the authenticated user owns the requested chat session before performing any operation.

Unauthorized users cannot view, modify, or delete another user's conversations.