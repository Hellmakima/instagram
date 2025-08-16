# **Lessons Learned**

## **Web Security Best Practices**

- Access tokens are stateless, meaning they do not require server-side session storage because all necessary information for authorization is encoded within the token itself.

### **A. CSRF (Cross-Site Request Forgery)**

some site makes a req from your browser and since you are logged in, it sends a token in the header.

1. **CSRF Tokens**:
   - Backend generates a unique token, stores it server-side, and sends it in a **non-HttpOnly cookie**.
   - Frontend stores it in its JS (so no one can access it).
   - Frontend includes the same token in a header (e.g., `X-CSRF-Token`).
   - Backend validates the cookie token against the header token.

---

### **B. JWT Security**

**Best Practices**:
jWT has data and its hash. u can only recreate the hash if u have key. data is readable by anyone

1. **Storage**:

   - Use **`HttpOnly`**, **`Secure`**, and **`SameSite=Strict` cookies** (not `localStorage`).
   - Avoid sensitive data in JWTs (use encryption/JWE if needed).

---

### **C. CORS (Cross-Origin Resource Sharing)**

**What it is**:

- When one page (A) on browser tries to call some other API (B), the browser first confirms with the A to see if B is allowed to make requests. This is completely implemented by browser.
- At backend of B we need to add A in CORS policy to allow it to make requests.

---

### **D. CSP (Content Security Policy)**

**What it is**:

- Restricts sources for scripts, styles, etc., to prevent XSS.

**Example Header**:

```http
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-abc123'; style-src 'self' https://fonts.googleapis.com; img-src 'self' data:
```

---

### **2. Implementation Guide**

#### **A. Backend (Flask) Setup**

1. **CSRF Protection**:

   - Generate tokens for state-changing requests (POST/PUT/DELETE).
   - Validate tokens in middleware.

2. **IP Tracking (Optional)**:
   - Hash/anonymize IPs for privacy compliance (GDPR).
   - Log temporarily (e.g., 30 days) for security monitoring.

**Example IP Anonymization**:

```python
import hashlib
def anonymize_ip(ip):
    return hashlib.sha256(ip.encode() + b"salt").hexdigest()
```

---

#### **B. Frontend**

1. **For JWT in Cookies**:

   - No token handling needed (cookies are auto-sent by the browser).
   - Include CSRF tokens in headers for non-GET requests.

#### **C. Overall**

- Use JWT (JSON Web Tokens) for access/refresh.
- Use random secure strings (128+ bits) for CSRF.
- Use OAuth 2.0 Authorization Code Flow with PKCE (recommended for SPAs).
- Include claims like sub, iat, exp in JWTs.
- Rotate refresh tokens on use (refresh token rotation).
  **Where to Store**
  | Token Type | Client Storage | Server Storage | DB Storage |
  | ------------- | ------------------------------- | ------------------------- | ---------------------- |
  | Access Token | **In-memory (JS variable)** | Never store | X |
  | Refresh Token | **HttpOnly, Secure cookie** | Optional (if blacklist) | (encrypted) |
  | CSRF Token | **DOM/form field or cookie** | Validate per session | Optional (per-session) |

---

**Reverse Proxy**

- detailed video on [reverse proxy](https://www.youtube.com/watch?v=m1MWjPKS5NM) (serve backend and frotend on same host)
- goes in over what it is
- DNS, ssl cert (https sites), etc
- docker linux setup

### OAuth2.0

- https://www.youtube.com/watch?v=8-0-8a0s-9w
- referance [postman blog](https://blog.postman.com/what-is-oauth-2-0/)
  - Uses
    - allow third party apps to use instagram without having to implement their own login system. (eg. sign in with google)
    - allows limited access to instagram data
    - no need to share user's password
  - agents
    - resource owner: This is the user that is granting third-party access to their data.
    - client: This is the third-party application that is requesting access to the resource owner,s data. When the resource owner grants access, the client gets an access token that can be used to request the resources within the granted scope.
    - authorization server: This is the server that is responsible for granting access to the client.
    - resource server: This is the server that is responsible for serving the client with the requested data.
  - flow
    - user logs in to instagram
    - instagram redirects user to client
    - client requests access token from authorization server
    - authorization server redirects client to instagram
    - instagram redirects client to resource server
    - resource server returns access token to client
    - client uses access token to access instagram data
- also [what-is-pkce](https://blog.postman.com/what-is-pkce/)

A ton of servers possible

1. **Auth Server** - Handles login, tokens, user creds
2. **Resource Server** - Protects and serves data
3. **Frontend Server** - Hosts your SPA or HTML views
4. **Gateway/Proxy Server** - Routes, rate-limits, logs; like a traffic cop
5. **File Server** - For static/media file uploads/downloads
6. **Cache Server** - Like Redis; holds session or temp data
7. **Database Server** - Holds your precious data
8. **Job/Worker Server** - For async/background tasks like emails
9. **Monitoring/Logging Server** - Watches everything

https://gemini.google.com/app/647b32c5f20ae882?hl=en-IN

## Pydantic Models

Pydantic models are a powerful tool for **data validation** and **settings management** in Python. While they are commonly used in FastAPI for validating incoming request bodies and outgoing responses, their utility extends much further.

### Core Uses of Pydantic Models

- **API Data Validation**: This is their most well-known use in frameworks like FastAPI, where they automatically validate and parse JSON data from HTTP requests and serialize Python objects into JSON responses.
- **Configuration Management**: You can use Pydantic to validate application settings loaded from environment variables, `.env` files, or other configuration sources. This ensures your app starts with valid, correctly typed settings.
- **Data Transformation**: Pydantic can be used to convert raw data from various sources (e.g., CSV, XML, other APIs) into structured Python objects, ensuring consistency and type safety before the data is processed by your application.
- **Internal Data Structures**: They are excellent for creating clear, typed data structures within your application's internal logic, making your code more readable, maintainable, and easier to debug. Instead of using plain dictionaries, you can use Pydantic models to enforce a schema for data passed between different functions or services.

## Database layer

Have a **layer between your FastAPI application and your database**. This architectural pattern is often referred to as a **Repository Pattern**, **Data Access Layer (DAL)**, or **Service Layer**, and it's highly recommended for several reasons, especially when considering potential database changes.

---

### Why a Data Access Layer is Crucial

1.  **Database Agnosticism (Decoupling)**:
    This is the primary benefit you've identified. By abstracting database interactions into a separate layer, your FastAPI application's core logic becomes independent of the specific database technology (e.g., PostgreSQL, MongoDB, Cassandra). If you decide to switch from NoSQL to SQL (or vice versa), or even to a different NoSQL/SQL database, you only need to rewrite the code within this data access layer. Your FastAPI routes, business logic, and API contracts remain largely untouched.

2.  **Centralized Data Logic**:
    All database operations (CRUD - Create, Read, Update, Delete) are consolidated in one place. This makes your codebase easier to understand, maintain, and debug. You don't have scattered database queries throughout your application.

3.  **Improved Testability**:
    With a clear separation, you can easily **mock** the data access layer during unit tests for your FastAPI application. This means you can test your application's business logic without needing an actual database connection, making tests faster and more reliable.

4.  **Enforcement of Business Rules**:
    The data access layer can enforce data integrity and business rules related to data storage before interacting with the database.

5.  **Security**:
    It provides a controlled point of access to your database, reducing the risk of direct, unvalidated queries from other parts of your application. This layer can also handle **sanitization** and **parameterized queries** to prevent SQL injection or similar attacks.

6.  **Performance Optimization**:
    This layer is a good place to implement caching strategies, connection pooling, or specific query optimizations without affecting your application's business logic.

---

### How to Implement It in FastAPI

In the context of a FastAPI application, you might structure it as follows:

- **Models (Pydantic)**: Define the data structures for your API requests and responses. These should represent your application's domain objects, not necessarily directly map to database tables/collections.
- **Services/Repositories Layer**: This layer contains the logic for interacting with the database.
  - It takes domain models as input.
  - It translates domain model operations into database-specific queries (using ORMs, ODM, or raw queries).
  - It returns data in a format suitable for your application's domain models.
- **Database (SQLAlchemy/Pydantic-SQLAlchemy/MongoEngine/Motor)**: The actual ORM/ODM or database driver code.
- **FastAPI Endpoints**: These interact with the **Services/Repositories layer**, not directly with the database. They handle request validation, call the appropriate service methods, and return responses.

#### Example Structure:

```
├── main.py             # FastAPI app
├── schemas/
│   └── item.py         # Pydantic models (e.g., Item, ItemCreate)
├── services/
│   └── item_service.py # Core business logic and database interaction methods
├── repositories/       # Or database/data_access - database-specific logic
│   └── item_repository.py # Handles ORM/ODM specifics
├── database.py         # Database session/connection setup
└── dependencies.py     # Dependency injection for services/repositories
```

In this structure:

- `main.py` would call functions from `services/item_service.py`.
- `services/item_service.py` would then call methods in `repositories/item_repository.py`.
- `repositories/item_repository.py` would contain the SQLAlchemy (for SQL) or Motor/Pymongo (for NoSQL) specific code.

---

### Challenges and Considerations

- **Initial Overhead**: It introduces a bit more boilerplate code upfront.
- **Complexity**: For very small, simple applications, it might seem overkill. However, even for small projects, it sets a good foundation for future scalability and maintainability.
- **Choosing the Right Abstraction**: Deciding what level of abstraction to put in the service vs. repository layer can sometimes be tricky. Generally, the repository deals with persistence details, while the service layer orchestrates multiple repositories or applies business logic on top of repository operations.

**In summary, creating a separate data access layer is not just a good idea; it's a fundamental best practice for building robust, maintainable, and adaptable applications, especially when anticipating potential changes to your underlying data storage technology.** It aligns perfectly with the **Single Responsibility Principle** and promotes loose coupling.
