from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Allow all CORS (you can restrict this later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or set to [your_ngrok_url] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import HTMLResponse

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return HTMLResponse(open("static/index.html").read())

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(request: Request, path: str):
    host = request.headers.get("host", "")
    url = ""
    if host.startswith("auth."):
        url = f"http://127.0.0.1:5001/{path}"
    else:
        url = f"http://127.0.0.1:5002/{path}"

    async with httpx.AsyncClient() as client:
        req_headers = dict(request.headers)
        req_body = await request.body()
        resp = await client.request(
            request.method, url, headers=req_headers, content=req_body
        )

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers={k: v for k, v in resp.headers.items() if k.lower() in {"content-type", "set-cookie"}}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=5000)
