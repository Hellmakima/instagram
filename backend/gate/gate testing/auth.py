from fastapi import FastAPI, Depends, Request, Response
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from pydantic import BaseModel

class CsrfSettings(BaseModel):
    secret_key: str = "supersecretsharedkey"

app = FastAPI()

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

@app.get("/test")
def form(csrf_protect: CsrfProtect = Depends()):
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    response = JSONResponse({
        "csrf_token": csrf_token.split(".")[0],  # send correct raw value
        "signed_token": signed_token,  # helpful for debugging
        "message": "Hello from AUTH 🛡️"
    })
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response


@app.post("/critical")
async def critical_endpoint(request: Request, csrf_protect: CsrfProtect = Depends()):
    await csrf_protect.validate_csrf(request)  # validates token in headers and cookie
    return {"message": "Critical action authorized 🔐"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("auth:app", host="127.0.0.1", port=5001, reload=True)
