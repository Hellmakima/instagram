"""
File: **app/middleware/auth.py**

Authentication middleware for FastAPI
Handles JWT token verification for protected routes
"""

# TODO: refer https://chat.deepseek.com/a/chat/s/f91737ea-01d1-44cf-8227-a271fcfdd123

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from jose import jwt, JWTError, ExpiredSignatureError
from app.core.config import settings
from app.utils.loggers import flow_logger
from app.schemas.auth import TokenData  # TODO: Import your existing model
from app.core.security import verify_token

# List of public paths that don't require authentication
PUBLIC_PATHS = {
    "/", "/login", "/register", "/docs", "/openapi.json", 
    "/static", "/favicon.ico", "/refresh"  # Add refresh endpoint to public paths
    # TODO: rewrite this list
}

async def auth_middleware(request: Request, call_next):
    # Skip auth for public endpoints
    if any(request.url.path.startswith(path) for path in PUBLIC_PATHS):
        return await call_next(request)
    
    # Special handling for refresh endpoint
    if request.url.path == "/refresh":
        return await handle_refresh_token(request, call_next)
    
    # Standard access token verification
    return await verify_access_token(request, call_next)

async def verify_access_token(request: Request, call_next):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        flow_logger.warning("Missing access token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = auth_header.split(" ")[1]
    
    try:
        decoded = jwt.decode(
            token=token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        if decoded.get("type") != "access":
            flow_logger.error(f"Invalid token type: {decoded.get('type')}")
            raise JWTError("Invalid token type")
        
        request.state.user = TokenData(username=decoded["sub"])  # Use your existing model
        flow_logger.info(f"Authenticated user: {decoded['sub']}")
        
    except ExpiredSignatureError:
        flow_logger.warning("Access token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except JWTError as e:
        flow_logger.error(f"JWT validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return await call_next(request)

async def handle_refresh_token(request: Request, call_next):
    """Special handling for refresh token endpoint"""
    try:
        body = await request.json()
        refresh_token = body.get("refresh_token")
        token_type = body.get("token_type", "refresh")
        
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token required"
            )
        
        # Use your existing verify_token function
        username = verify_token(refresh_token, token_type=token_type)
        request.state.user = TokenData(username=username)
        
    except HTTPException:
        raise  # Re-raise existing HTTP exceptions
    except Exception as e:
        flow_logger.error(f"Refresh token error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    return await call_next(request)