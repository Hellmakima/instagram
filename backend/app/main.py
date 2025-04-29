"""
File: app/main.py

Contains the FastAPI app
Collects all the routers from api folder and mounts them to the app
Serves static files from static folder
Manages the database connection

to run the app: uvicorn app.main:app --reload --port 5000
"""
# mongodb connection client
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))

# fastapi app
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# from app.api.router import router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# app.include_router(router)

@app.get("/")
async def root(name: str="Sufiyan"):
    return {"message": f"Hello from FastAPI",
            "query": name}

@app.on_event("shutdown")
async def shutdown_event():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)