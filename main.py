from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import JSONResponse

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
    s = req.symptoms.lower()
    score = 0
    reasons = []
    
    danger = ['chest pain', 'severe bleeding', 'unconscious', 'no breathing', 'shortness of breath', 'difficulty breathing', 'stroke', 'seizure']
    for k in danger:
        if k in s:
            score += 100
            reasons.append(f'danger sign: {k}')
    
    if 'fever' in s and ('cough' in s or 'breath' in s):
        score += 50
        reasons.append('fever with respiratory symptoms')
    
    mild = ['headache', 'sore throat', 'runny nose', 'fatigue', 'nausea', 'diarrhea']
    for m in mild:
        if m in s:
            score += 5
            reasons.append(f'mild: {m}')
    
    if req.age >= 65:
        score += 10
        reasons.append('age >= 65')

    if score >= 100:
        disposition = '🚨 Emergency — seek immediate care (call emergency services)'
    elif score >= 50:
        disposition = '⚠️ Urgent — request rapid teleconsult'
    elif score >= 15:
        disposition = 'ℹ️ Advisory — schedule teleconsult or self-care as appropriate'
    else:
        disposition = '✅ Self-care — monitor symptoms, rest, and use verified knowledge hub'

    return JSONResponse({
        "score": score,
        "reasons": reasons,
        "advice": disposition
    })
# Run with: uvicorn main:app --reload
# Access at: http://localhost:8000
# Static files at: http://localhost:8000/static/