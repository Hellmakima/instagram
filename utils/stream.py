from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

def stream_data():
    yield "part 1\n"*10000
    yield "part 2\n"*10000
    yield "done\n"*10000

@app.get("/")
def home():
    return StreamingResponse(stream_data(), media_type="text/plain")

"""
# Test it
import requests

with requests.get("http://localhost:8000", stream=True) as r:
    # for chunk in r.iter_content(chunk_size=1057):
    for chunk in r.iter_content(chunk_size=None):
        print(len(chunk.decode()), flush=True)

"""