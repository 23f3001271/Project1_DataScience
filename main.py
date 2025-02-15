from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import subprocess
import json

app = FastAPI()

# Define a model for the task request
class TaskRequest(BaseModel):
    task: str

# POST endpoint to run tasks
@app.post("/run")
async def run_task(task_request: TaskRequest):
    task_description = task_request.task
    try:
        # Example task handling
        if "install uv" in task_description:
            # Task A1: Install uv and run datagen.py
            subprocess.run(["pip", "install", "uv"], check=True)
            subprocess.run(["python", "datagen.py", "user@example.com"], check=True)
            return {"status": "Task A1 completed successfully"}
        
        elif "format" in task_description:
            # Task A2: Format using prettier
            subprocess.run(["npx", "prettier@3.4.2", "--write", "/data/format.md"], check=True)
            return {"status": "Task A2 completed successfully"}
        
        # Add more task handling logic here...

        else:
            raise HTTPException(status_code=400, detail="Task not recognized")
    
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error executing task: {str(e)}")

# GET endpoint to read file contents
@app.get("/read")
async def read_file(path: str):
    try:
        if not path.startswith("/data/"):
            raise HTTPException(status_code=403, detail="Access to this path is forbidden")
        
        with open(path, "r") as file:
            content = file.read()
        return {"content": content}
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
