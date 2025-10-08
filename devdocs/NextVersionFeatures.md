## Features

- custom themes and templates (cyberpunk, barbie, clash of clans, etc)
- text post (like tweets)
- reddit features
  - comment trees
  - communities
- end-to-end encryption

## Architecture

- decide the DB (wheather to keep using MongoDB or switch to PostgreSQL)
- caching (denormalization in DB)
  - keep recent comments, likes, etc. for each post.

**Resource Server (Validation):** The Resource Server performs three checks _internally_ without calling the Auth Server:

- **JWT validation**
  - **Claims:** It checks critical claims (payload fields) like:
    - `jti` (JWT ID): Is the token unique?
    - `exp` (Expiration Time): Is the token still valid?
    - `iss` (Issuer): Is the token from the correct Auth Server?
    - `aud` (Audience): Is the token intended for this Resource Server?
  - **Scopes/Permissions:** It checks the scopes or roles in the JWT payload to see if the user is authorized for the specific endpoint.
