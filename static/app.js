document.getElementById("triageForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const resultEl = document.getElementById("result");

    // Show spinner and processing message
    resultEl.textContent = "";
    const spinner = document.createElement("span");
    spinner.textContent = "⏳ Processing your request...";
    resultEl.appendChild(spinner);

    const name = document.getElementById("name").value.trim();
    const age = parseInt(document.getElementById("age").value);
    const symptoms = document.getElementById("symptoms").value.trim();

    try {
        const response = await fetch("/api/triage_stream", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, age, symptoms }),
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        // Clear previous spinner/message before streaming output
        resultEl.textContent = "";

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let advice = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            advice += decoder.decode(value);
            resultEl.textContent = advice;
        }
    } catch (err) {
        resultEl.textContent = `Error: ${err.message}`;
    }
});
