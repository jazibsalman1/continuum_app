from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess

app = FastAPI()

# Static folder mount
app.mount("/static", StaticFiles(directory="static"), name="static")

# Home page route
@app.get("/")
def read_index():
    return FileResponse("static/index.html")

# Request model
class TriageRequest(BaseModel):
    name: str
    age: int
    symptoms: str


@app.post("/api/triage")
async def triage(req: TriageRequest):
    prompt = f"""
    Patient Name: {req.name}
    Age: {req.age}
    Symptoms: {req.symptoms}
    """

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15
        )
        ai_advice = result.stdout.decode().strip()
    except Exception as e:
        ai_advice = f"Error getting AI advice: {str(e)}"

    return JSONResponse({
        "advice": ai_advice
    })

# Instructions to run the app:
# 1. Install dependencies: pip install -r requirements.txt
# 2. Run the app: uvicorn main:app --reload
# 3. Access the app at: http://localhost:8000   
# Run with: uvicorn main:app --reload
# Access at: http://localhost:8000