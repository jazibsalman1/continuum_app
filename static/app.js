     File: static/app.js
app_js = r
document.getElementById('triageBtn').addEventListener('click', async function(){
    const name = document.getElementById('name').value || 'Anonymous'
    const age = parseInt(document.getElementById('age').value || '30')
    const symptoms = document.getElementById('symptoms').value || ''
    const payload = { name, age, symptoms }
    const res = await fetch('/api/triage', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
    })
    const data = await res.json()
    document.getElementById('result').innerText = `Disposition: ${data.disposition}\nScore: ${data.score}\nReasons: ${data.reasons.join(', ')}`
})

document.getElementById('teleBtn').addEventListener('click', async function(){
    const name = document.getElementById('name').value || 'Anonymous'
    const age = parseInt(document.getElementById('age').value || '30')
    const symptoms = document.getElementById('symptoms').value || ''
    const form = new FormData()
    form.append('name', name)
    form.append('age', age)
    form.append('symptoms', symptoms)
    const res = await fetch('/api/request_teleconsult', { method: 'POST', body: form })
    const data = await res.json()
    document.getElementById('result').innerText = `Teleconsult status: ${data.status} — position ${data.position}`
})
