from fastapi import FastAPI, Depends, Request
from fastapi_csrf_protect import CsrfProtect
from pydantic import BaseModel

class CsrfSettings(BaseModel):
    secret_key: str = "supersecretsharedkey"  # SAME SECRET!

app = FastAPI()

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

@app.get("/test")
def test():
    return "Hello from RESOURCE 📦"

@app.post("/critical")
async def critical_endpoint(request: Request, csrf_protect: CsrfProtect = Depends()):
    await csrf_protect.validate_csrf(request)  # validates token in headers and cookie
    return {"message": "Critical action authorized by RESOURCE 🔐"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("resource:app", host="127.0.0.1", port=5002, reload=True)
