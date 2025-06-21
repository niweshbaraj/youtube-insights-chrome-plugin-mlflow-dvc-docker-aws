document.getElementById('sendRequest').addEventListener('click', async () => {
    const randomText = ["I love this!", "This is terrible."][Math.floor(Math.random() * 2)];

    try {
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ comments: [randomText] })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log('Response:', data);
        document.getElementById('response').innerText = JSON.stringify(data);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('response').innerText = `Error: ${error.message}`;
    }
});