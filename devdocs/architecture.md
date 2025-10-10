# Servers

## Auth Server

### FE Endpoints

- GET `/auth/csrf-token`
- POST `/auth/register`
- POST `/auth/login`
- POST `/auth/refresh_token`
- POST `/auth/logout`

### Internal Endpoints

- GET `/user_id/{username}` (get user_id by username)
- GET `/username/{user_id}` (get username by user_id)

## Resource Server

### FE Endpoints

_(No endpoints listed in the diagram)_

# Databases

## Auth Database

### users

- \_id
- username
- email
- hashed_password
- created_at
- is_verified
- is_suspended
- suspended_till
- last_activity_at
- is_pending_deletion
- delete_at

### refresh_tokens

- \_id
- user_id
- refresh_token
- expires_at
- revoked

## Resource Database

### users

- \_id (FK)
- description
- display_name
- profile_picture_url
