from fastapi import FastAPI, HTTPException
import os

app = FastAPI()

@app.post("/run")
async def run_task(task: str):
    return {"message": f"Executing task: {task}"}

@app.get("/read")
async def read_file(path: str):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(path, "r") as f:
        return {"content": f.read()}
