# Database Schema

## Users Table

| Column | Type | Description |
|----------|------|-------------|
| id | Integer | Primary Key |
| name | String | User name |
| email | String | Unique email |
| hashed_password | String | Encrypted password |

---

## Relationships

Currently:

User

↓

Authentication

Future:

User

↓

Memories

↓

Embeddings

↓

Chat History