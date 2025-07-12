from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.csrf_config import CsrfConfig
import httpx # For making HTTP requests to downstream services
import os

# --- Configuration ---
AUTH_SERVER_URL = "http://localhost:8001"
RESOURCE_SERVER_URL = "http://localhost:8002"

# Allowed origins for your frontend
FRONTEND_ORIGINS = [
    "http://localhost:5002", # Your Flask frontend
    "http://127.0.0.1:5002", # Another possible localhost alias
    # Add your production frontend URL(s) here
]

# --- FastAPI App Setup ---
app = FastAPI(title="API Gateway with CSRF")

# --- CSRF Configuration for fastapi-csrf-protect ---
# This class needs to be defined in your app's main scope or imported
@CsrfProtect.load_config
def get_csrf_config():
    return CsrfConfig(
        secret=os.environ.get("CSRF_SECRET_KEY", "your-super-secret-csrf-key"), # IMPORTANT: Use a strong, random key in production
        # Cookie settings (ensure Secure in production, SameSite=Lax is common for SPA)
        cookie_name="X-CSRF-TOKEN",
        cookie_path="/",
        cookie_domain=None, # Set to your domain (e.g., "yourdomain.com") in production
        cookie_secure=False, # Set to True in production (requires HTTPS)
        cookie_samesite="lax", # "strict" or "lax"
        header_name="X-CSRF-Token", # Header frontend will send the token in
        max_age=3600, # CSRF cookie expiry in seconds (1 hour)
    )

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True, # Crucial for sending cookies (like CSRF and session cookies)
    allow_methods=["*"],    # Allow all methods
    allow_headers=["*"],    # Allow all headers (including your custom X-CSRF-Token)
)

# --- HTTPX Client for Proxying ---
client = httpx.AsyncClient()

# --- Helper to forward requests ---
async def forward_request(
    request: Request,
    target_base_url: str,
    csrf_protect: CsrfProtect # Inject CsrfProtect instance
):
    try:
        # Construct target URL
        path = request.url.path
        query = request.url.query
        target_url = f"{target_base_url}{path}{'?' + query if query else ''}"

        # Prepare headers for forwarding
        # We need to explicitly exclude headers that httpx might add automatically
        # or that are specific to the client-gateway connection (e.g., Host)
        forward_headers = {k: v for k, v in request.headers.items() if k.lower() not in ["host", "content-length", "transfer-encoding"]}

        # Add the CSRF token from the cookie to the headers for internal validation by CsrfProtect
        # The CsrfProtect dependency will handle validation for incoming requests
        # and attach the cookie to the outgoing response if a new token is set
        # We also need to add the JS-accessible token to the response header from the gateway
        # This is handled by CsrfProtect automatically for protected routes.

        # Read the request body once
        request_body = await request.body()

        # Make the request to the downstream service
        proxy_response = await client.request(
            method=request.method,
            url=target_url,
            headers=forward_headers,
            content=request_body,
            # Pass cookies received by the gateway directly.
            # httpx will handle setting/sending cookies from the `request` object.
            cookies=request.cookies
        )

        # Prepare the response back to the client
        response = Response(content=proxy_response.content, status_code=proxy_response.status_code)

        # Copy headers from the downstream response, excluding Hop-by-Hop headers
        for name, value in proxy_response.headers.items():
            if name.lower() not in ["content-encoding", "content-length", "transfer-encoding", "connection", "keep-alive", "proxy-authenticate", "proxy-authorization", "te", "trailers", "upgrade"]:
                response.headers[name] = value

        return response

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Proxy error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

# --- Gateway Endpoints ---

# --- Authentication Endpoints (Proxy to Auth Server) ---
# Login endpoint - no CSRF validation on incoming request, but sets token on success response
@app.post("/auth/login")
async def login(request: Request, csrf_protect: CsrfProtect = Depends()):
    response = await forward_request(request, AUTH_SERVER_URL, csrf_protect)
    # If login was successful (check status code from Auth Server's response)
    if response.status_code == 200:
        # Issue a new CSRF token and set it in the response cookie
        # This creates the HttpOnly cookie and adds the header for the frontend to read
        csrf_protect.set_csrf_cookie(response)
    return response

# Logout endpoint - no CSRF validation on incoming request, but clears token on success response
@app.post("/auth/logout")
async def logout(request: Request, csrf_protect: CsrfProtect = Depends()):
    response = await forward_request(request, AUTH_SERVER_URL, csrf_protect)
    # If logout was successful (check status code from Auth Server's response)
    if response.status_code == 200:
        # Unset the CSRF token cookie from the response
        csrf_protect.unset_csrf_cookie(response)
    return response

# Register endpoint - no CSRF validation
@app.post("/auth/register")
async def register(request: Request, csrf_protect: CsrfProtect = Depends()):
    return await forward_request(request, AUTH_SERVER_URL, csrf_protect)

# --- Resource Endpoints (Proxy to Resource Server with CSRF validation) ---
# Example protected POST route
@app.post("/api/{path:path}")
async def protected_api_post(request: Request, path: str, csrf_protect: CsrfProtect = Depends()):
    # validate_csrf will check the incoming request headers and cookies
    # If invalid, it will raise an HTTPException automatically
    await csrf_protect.validate_csrf(request)
    return await forward_request(request, RESOURCE_SERVER_URL, csrf_protect)

# Example protected PUT route
@app.put("/api/{path:path}")
async def protected_api_put(request: Request, path: str, csrf_protect: CsrfProtect = Depends()):
    await csrf_protect.validate_csrf(request)
    return await forward_request(request, RESOURCE_SERVER_URL, csrf_protect)

# Example protected DELETE route
@app.delete("/api/{path:path}")
async def protected_api_delete(request: Request, path: str, csrf_protect: CsrfProtect = Depends()):
    await csrf_protect.validate_csrf(request)
    return await forward_request(request, RESOURCE_SERVER_URL, csrf_protect)

# Example GET route (no CSRF validation required for GETs, but CSRF cookie might be set on first load)
@app.get("/api/{path:path}")
async def api_get(request: Request, path: str, csrf_protect: CsrfProtect = Depends()):
    # For GET requests, we don't *validate* the CSRF token, but the initial
    # GET request to a page *might* be where the HttpOnly CSRF cookie is first issued.
    # CsrfProtect will handle setting the cookie if it determines it's a new session.
    response = await forward_request(request, RESOURCE_SERVER_URL, csrf_protect)
    # It's good practice to set the CSRF cookie on initial GET requests to the app
    # (if not already present), so the frontend has it for subsequent POSTs.
    # CsrfProtect usually handles this automatically on relevant routes.
    # We can explicitly ensure it's set if we want for initial entry points.
    if csrf_protect.get_csrf_cookie(request) is None: # Only set if not already present in request
         csrf_protect.set_csrf_cookie(response)
    return response


# --- CSRF Token Endpoint (Optional, but useful for SPAs if not using headers for token delivery) ---
# If you prefer to get the JS-accessible token from a specific endpoint
@app.get("/csrf-token")
async def get_csrf_token(request: Request, csrf_protect: CsrfProtect = Depends()):
    response = JSONResponse(content={"csrf_token": csrf_protect.get_csrf_from_headers(request)})
    # Ensure the HttpOnly cookie is set if it's not already
    # (e.g., if this is the very first request the frontend makes to get the token)
    if csrf_protect.get_csrf_cookie(request) is None:
        csrf_protect.set_csrf_cookie(response)
    return response


if __name__ == "__main__":
    import uvicorn
    # IMPORTANT: Use a real, strong secret key in production environment variables
    # e.g., export CSRF_SECRET_KEY="<your_very_long_random_string>"
    uvicorn.run(app, host="0.0.0.0", port=8000)