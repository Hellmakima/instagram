from fastapi import FastAPI, Depends, Request, Response
from fastapi_csrf_protect import CsrfProtect
from pydantic_settings import BaseSettings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

csrf = CsrfProtect()

class CsrfSettings(BaseSettings):
    secret_key: str|None = "CSRF_SECRET"
    cookie_samesite: str = "lax"
    cookie_secure: bool = False

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

@app.post("/protected-endpoint")
async def protected(request: Request, response: Response, csrf_protect: CsrfProtect = Depends()):
    await csrf_protect.validate_csrf(request)
    return {"status": "success", "message": "CSRF validated!"}

@app.get("/csrf-token")
async def generate_csrf_token(
    response: Response,
    csrf_protect: CsrfProtect = Depends()
):
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    csrf_protect.set_csrf_cookie(signed_token, response)
    return {"detail": "CSRF token generated successfully.", "csrf_token": csrf_token}


async def verify_csrf(
    request: Request,
    response: Response,
    csrf_protect: CsrfProtect = Depends(),
):
    await csrf_protect.validate_csrf(request)
    csrf_protect.unset_csrf_cookie(response)

"""
# Corresponding nextJS code

```bash
npx create-next-app@latest csrf-demo --ts
cd csrf-demo
npm install axios
```

Note that we are using localhost and not 127.0.0.1

```js
"use client";

import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [csrfToken, setCsrfToken] = useState<string | null>(null);
  const [response, setResponse] = useState<string>("");

  const getCsrfToken = async () => {
    try {
      const res = await axios.get("http://localhost:8000/csrf-token", {
        withCredentials: true,
      });
      setCsrfToken(res.data.csrf_token);
      setResponse("CSRF token fetched successfully!");
    } catch (err) {
      console.error(err);
      setResponse("Failed to fetch CSRF token.");
    }
  };

  const postWithCsrf = async () => {
    if (!csrfToken) return setResponse("No CSRF token available.");
    try {
      const res = await axios.post(
        "http://localhost:8000/protected-endpoint",
        { data: "hello" },
        {
          headers: { "X-CSRF-Token": csrfToken },
          withCredentials: true,
        }
      );
      setResponse("POST success: " + JSON.stringify(res.data));
    } catch (err: any) {
      console.error(err);
      setResponse("POST failed: " + err.response?.status);
    }
  };

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">Next + FastAPI CSRF Demo</h1>
      <button onClick={getCsrfToken} className="mr-2 p-2 border">
        Get CSRF Token
      </button>
      <button onClick={postWithCsrf} className="p-2 border">
        POST with CSRF
      </button>
      <p className="mt-4">{response}</p>
      <p>CSRF Token: {csrfToken}</p>
    </main>
  );
}
```
"""