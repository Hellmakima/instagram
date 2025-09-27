# A'udhu billahi min ash-shaytan ir-rajim Bismillahi ar-Rahmani ar-Rahim

r"""
This files serves as a temporary replacement for Nginx.

We'll route all requests from nmaa.com to this server
Setup:

open "C:\Windows\System32\drivers\etc\hosts"
add the following lines:
```host
127.0.0.1 nmaa.com
127.0.0.1 auth.nmaa.com
127.0.0.1 resource.nmaa.com
```

flush DNS cache:
`ipconfig /flushdns`

run this script:
uv run uvicorn gate:app --reload --port 80

"""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
from fastapi.responses import HTMLResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(request: Request, path: str):
    host = request.headers.get("host", "")
    if host.startswith("auth."):
        url = f"http://127.0.0.1:5001/{path}"
    elif host.startswith("resource."):
        url = f"http://127.0.0.1:5002/{path}"
    else:
        url = f"http://127.0.0.1:3000/{path}"

    async with httpx.AsyncClient() as client:
        req_headers = dict(request.headers)
        req_body = await request.body()
        try:
            resp = await client.request(
                request.method, url, headers=req_headers, content=req_body
            )
        except httpx.ConnectError:
            print(f"""
Failed to connect to {url},
host: {host}, 
path: {path}, 
method: {request.method}, 
headers: {req_headers}"""
)
            return HTMLResponse(open("static/404.html").read())

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers={k: v for k, v in resp.headers.items() if k.lower() in {"content-type", "set-cookie"}}
    )


# It's a basic reverse proxy, but **not good enough** to fully simulate Nginx. Missing:

# * WebSocket support
# * Streaming (e.g. chunked transfer)
# * TLS termination
# * Load balancing
# * Timeout/retry control
# * Header filtering/sanitization
# * Compression (gzip, etc.)

# Use only for dev/testing. For prod, use real Nginx or Traefik.
