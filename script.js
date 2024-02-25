function uploadVideo() {
    const form = document.getElementById("uploadForm");
    const messageDiv = document.getElementById("message");

    const formData = new FormData(form);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        messageDiv.innerHTML = `<p>${data.message || data.error}</p>`;
    })
    .catch(error => {
        console.error("Error:", error);
        messageDiv.innerHTML = "<p>An error occurred during the upload.</p>";
    });
}