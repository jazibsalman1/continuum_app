 Continuum — Minimal Prototype (backend + frontend)
# Project layout (single-file presentation)

# File: requirements.txt
# ----------------------
# fastapi
# uvicorn[standard]
# python-multipart
# jinja2

# File: main.py (FastAPI backend serving API + static frontend)
# ------------------------------------------------------------
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import json
import os

app = FastAPI()

# Serve the frontend files from ./static
if not os.path.exists('static'):
    os.makedirs('static')

app.mount('/static', StaticFiles(directory='static'), name='static')

# Simple in-memory "teleconsult" queue (demo only)
teleconsult_requests = []

class TriageRequest(BaseModel):
    name: str
    age: int
    symptoms: str

@app.get('/', response_class=HTMLResponse)
async def root():
    return FileResponse('static/index.html')

@app.post('/api/triage')
async def triage(req: TriageRequest):
    # Very simple rule-based triage placeholder
    s = req.symptoms.lower()
    score = 0
    reasons = []
    # Danger keywords
    danger = ['chest pain', 'severe bleeding', 'unconscious', 'no breathing', 'shortness of breath', 'difficulty breathing', 'stroke', 'seizure']
    for k in danger:
        if k in s:
            score += 100
            reasons.append(f'danger sign: {k}')
    # Fever + cough -> possible urgent
    if 'fever' in s and ('cough' in s or 'breath' in s):
        score += 50
        reasons.append('fever with respiratory symptoms')
    # Mild common symptoms
    mild = ['headache', 'sore throat', 'runny nose', 'fatigue', 'nausea', 'diarrhea']
    for m in mild:
        if m in s:
            score += 5
            reasons.append(f'mild: {m}')
    # Age factor
    if req.age >= 65:
        score += 10
        reasons.append('age >= 65')

    # Decision thresholds (demo)
    if score >= 100:
        disposition = 'Emergency — seek immediate care (call emergency services)'
    elif score >= 50:
        disposition = 'Urgent — request rapid teleconsult'
    elif score >= 15:
        disposition = 'Advisory — schedule teleconsult or self-care as appropriate'
    else:
        disposition = 'Self-care — monitor symptoms, rest, and use verified knowledge hub'


@app.post('/api/request_teleconsult')
async def request_teleconsult(name: str = Form(...), age: int = Form(...), symptoms: str = Form(...)):
    req = {'name': name, 'age': age, 'symptoms': symptoms}
    teleconsult_requests.append(req)
    # Simple placeholder response: in real app you'd create a session, notify clinicians, etc.
    return JSONResponse({'status': 'queued', 'position': len(teleconsult_requests)})

@app.get('/api/teleconsult_queue')
async def get_queue():
    return JSONResponse({'queue_length': len(teleconsult_requests), 'queue': teleconsult_requests})

# If run directly, start uvicorn
if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)


# Write static files to disk so the prototype is runnable from this project folder
with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write('fastapi\nuvicorn[standard]\npython-multipart\njinja2\n')

# Short README content
readme = '''
Continuum — Minimal Prototype

Run locally:
1. python3 -m venv venv
2. source venv/bin/activate   (on Windows: venv\\Scripts\\activate)
3. pip install -r requirements.txt
4. uvicorn main:app --reload
5. Open http://127.0.0.1:8000 in your browser

Notes:
- This is a demo. Do NOT use for real medical decisions.
- Replace the rule-based triage with a properly validated clinical model before any real usage.
'''
with open('README.txt', 'w', encoding='utf-8') as f:
    f.write(readme)

# End of code file (the canvas shows the files and you can copy them out)
print('Created prototype files: main.py, static/index.html, static/app.js, requirements.txt, README.txt')
