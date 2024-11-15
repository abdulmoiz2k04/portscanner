document.getElementById('scanForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const ipAddress = document.getElementById('ip').value;
    const resultBox = document.getElementById('result-box');
    resultBox.textContent = 'Scanning...';

    try {
        const response = await fetch('https://s724dcxi2f.execute-api.ap-southeast-2.amazonaws.com/prod/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ip: ipAddress }),
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
