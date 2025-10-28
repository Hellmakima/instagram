from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/app")
def read_main(request: Request):
    return {
        "message": "Hello World",
        "root_path": request.scope.get("root_path"),
        "url": request.url,
        "headers": request.headers,
        "cookies": request.cookies,
        "query_params": request.query_params,
        "client": request.client,
        "state": request.state,
        # "app": request.app,
        # "background": request.background,
        "base_url": request.base_url,
        "method": request.method,
        # "path": request.path,
        "path_params": request.path_params,
    }

data = {
  "message": "Hello World",
  "root_path": "",
  "url": {
    "_url": "http://auth.nmaa.com/app?hi=4"
  },
  "headers": {
    "host": "auth.nmaa.com",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-US,en-IN;q=0.9,en;q=0.8,ja;q=0.7",
    "cache-control": "max-age=0",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "via": "1.1 Caddy",
    "x-forwarded-for": "127.0.0.1",
    "x-forwarded-host": "auth.nmaa.com",
    "x-forwarded-proto": "http"
  },
  "cookies": {

  },
  "query_params": {
    "hi": "4"
  },
  "client": [
    "127.0.0.1",
    0],
  "state": {
    "_state": {

    }
  },
  "base_url": {
    "_url": "http://auth.nmaa.com/"
  },
  "method": "GET",
  "path_params": {

  }
}