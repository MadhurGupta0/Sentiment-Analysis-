document.getElementById('startBackendButton').addEventListener('click', function() {
    fetch('/start-backend', {  // Calls the endpoint to start the backend
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('backendStatus').textContent = data.message || data.error;
    })
    .catch(error => {
        document.getElementById('backendStatus').textContent = "Error: " + error;
    });
});

document.getElementById('analyze').addEventListener('click', function() {
    const fileInput = document.getElementById('fileInput').files[0];
    if (!fileInput) {
        alert("Please select a file before uploading.");
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput);

    document.getElementById('loading').style.display = 'block';

    fetch('http://127.0.0.1:5000/analyze', {  // Calls the backend API route
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        if (data.error) {
            alert(data.error);
        } else {
            document.getElementById('positive').textContent = data.positive;
            document.getElementById('negative').textContent = data.negative;
            document.getElementById('neutral').textContent = data.neutral;
        }
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        alert("Error: " + error);
    });
});
