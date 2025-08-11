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

# Function to get AI advice from Ollama llama3 model
def get_ai_advice(name, age, symptoms):
    prompt = f"""
    Patient Name: {name}
    Age: {age}
    Symptoms: {symptoms}

    You are a medical triage assistant. 
    Give clear, short, and safe advice about what the patient should do next.
    Avoid any dangerous or false claims.
    """

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.stdout.decode().strip()
    except Exception as e:
        return f"Error getting AI advice: {str(e)}"
@app.post("/api/triage")
async def triage(req: TriageRequest):
    # Replace this with real Ollama call when ready
    # ai_advice = get_ai_advice(req.name, req.age, req.symptoms)

    # Dummy structured advice for now
    ai_advice = {
        "summary": f"Hi {req.name}, based on your symptoms, here is what I suggest.",
        "recommendations": [
            "Get plenty of rest.",
            "Stay hydrated with water and fluids.",
            "Take over-the-counter meds like paracetamol if feverish.",
            "Monitor symptoms, and see a doctor if things worsen."
        ],
        "follow_up": "If symptoms persist beyond 7 days or worsen, please consult a healthcare professional."
    }

    return JSONResponse({
        "patient": {
            "name": req.name,
            "age": req.age,
            "symptoms": req.symptoms
        },
        "advice": ai_advice
    })

# Note: This is a placeholder function. Replace with actual Ollama integration when available.
# Instructions to run the app:
# 1. Install dependencies: pip install -r requirements.txt
# 2. Run the app: uvicorn main:app --reload
# 3. Access the app at: http://localhost:8000   



# Run with: uvicorn main:app --reload
# Access at: http://localhost:8000
# Static files at: http://localhost:8000/static/
