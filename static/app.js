document.getElementById("triageForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const age = parseInt(document.getElementById("age").value);
    const symptoms = document.getElementById("symptoms").value;

    const res = await fetch("/api/triage", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, age, symptoms })
    });

    const data = await res.json();

    // Build HTML for advice display
    const advice = data.advice;
    let html = `<strong>Summary:</strong> ${advice.summary}<br><br>`;
    html += `<strong>Recommendations:</strong><ul>`;
    advice.recommendations.forEach(rec => {
        html += `<li>${rec}</li>`;
    });
    html += `</ul>`;
    html += `<strong>Follow-up:</strong> ${advice.follow_up}`;

    document.getElementById("result").innerHTML = html;
});
