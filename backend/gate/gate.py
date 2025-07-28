# A'udhu billahi min ash-shaytan ir-rajim Bismillahi ar-Rahmani ar-Rahim

from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
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

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return HTMLResponse(open("static/index.html").read())

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(request: Request, path: str):
    url = ""
    # host = request.headers.get("host", "")
    # if host.startswith("auth."):
    if path.startswith("auth/"):
        url = f"http://127.0.0.1:5001/{path}"
    else:
        url = f"http://127.0.0.1:5002/{path}"

    async with httpx.AsyncClient() as client:
        req_headers = dict(request.headers)
        req_body = await request.body()
        try:
            resp = await client.request(
                request.method, url, headers=req_headers, content=req_body
            )
        except httpx.ConnectError:
            return HTMLResponse(open("static/404.html").read())

    if resp.status_code == 404:
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
