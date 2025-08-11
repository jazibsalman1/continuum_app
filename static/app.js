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

    document.getElementById("result").textContent = data.advice;
});
