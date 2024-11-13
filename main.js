document.getElementById('scanForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const ipAddress = document.getElementById('ip').value;
    const resultBox = document.getElementById('result-box');
    resultBox.textContent = 'Scanning...';

    try {
        const response = await fetch('https://aa98-3-105-184-108.ngrok-free.app/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ip: ipAddress }),
            mode: 'cors',
        });

        if (!response.ok) {
            const errorData = await response.json();
            resultBox.textContent = `Error: ${errorData.error}`;
            return;
        }

        const data = await response.json();
        const portResults = data.port_result.join('\n');
        resultBox.textContent = `Scan Results for ${data.target}:\n${portResults}\nScan Duration: ${data.duration} seconds`;
    } catch (error) {
        resultBox.textContent = `Request failed: ${error.message}`;
    }
});
