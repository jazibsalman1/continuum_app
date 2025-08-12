from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import subprocess
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Static folder mount
app.mount("/static", StaticFiles(directory="static"), name="static")

# Home page route
@app.get("/")
def read_index():
    return FileResponse("static/index.html")

# Request model with basic validation
class TriageRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., gt=0, lt=120)
    symptoms: str = Field(..., min_length=5, max_length=500)

@app.post("/api/triage")
async def triage(req: TriageRequest):
    prompt = f"""
Patient Name: {req.name}
Age: {req.age}
Symptoms: {req.symptoms}

You are a professional medical triage assistant.
Provide a concise, clear, and safe advice for the patient.
Keep it short and easy to understand.
Avoid any dangerous or misleading suggestions.
Respond as a helpful human medical assistant.
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "medllama2"],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        stderr_output = result.stderr.decode().strip()
        if stderr_output:
            logging.warning(f"Ollama stderr: {stderr_output}")

        ai_advice = result.stdout.decode().strip()
        if not ai_advice:
            raise RuntimeError("Empty response from Ollama model")

    except subprocess.TimeoutExpired:
        logging.error("Ollama command timed out")
        raise HTTPException(status_code=504, detail="AI model timed out. Please try again later.")
    except Exception as e:
        logging.error(f"Error calling Ollama: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting AI advice: {str(e)}")

    return JSONResponse({
        "advice": ai_advice
    })
# Error handling for 404
@app.exception_handler(404)
def not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Resource not found. Please check the URL."}
    )
# Error handling for 500
@app.exception_handler(500)
def internal_server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error. Please try again later."}
    )
# Instructions for running the app
# Save this code in a file named main.py
# Ensure you have a directory named 'static' with an 'index.html' file in it
# The 'index.html' file should contain the HTML code for your frontend
# You can use the provided 'static/index.html' as a starting point
# Run the app with: uvicorn main:app --reload
# This will start the FastAPI server and serve the static files from the 'static' directory
# Make sure to have the 'ollama' command available in your PATH for the AI model        
# to work correctly. The model should be named 'medllama2'. 
# Ensure you have the necessary permissions to run subprocess commands.
# The app will be accessible at http://localhost:8000
# The static files (HTML, CSS, JS) will be served from the 'static'
# directory, and the main page will be at http://localhost:8000/
# The API endpoint for triage requests will be at http://localhost:8000/api/triage
# Make sure to have the necessary Python packages installed:
# pip install fastapi uvicorn pydantic
# You can run the app using the command:
# uvicorn main:app --reload