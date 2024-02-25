document.addEventListener('DOMContentLoaded', (event) => {
    const video = document.getElementById('videoFeed');
    const startButton = document.getElementById('startButton');
    const stopButton = document.getElementById('stopButton');
    const messageDiv = document.getElementById('message');
    let mediaRecorder;
    let recordedChunks = [];

    // Function to start recording
    const startRecording = () => {
        startButton.disabled = true;
        stopButton.disabled = false;
        recordedChunks = [];
        mediaRecorder.start();
    };

    // Function to stop recording
    const stopRecording = () => {
        mediaRecorder.stop();
    };

    // Access the user's camera and start the video feed
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
            mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm; codecs=vp9' });

            // Event handler for when data is available
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };

            // Event handler for when recording is stopped
            mediaRecorder.onstop = () => {
                const blob = new Blob(recordedChunks, { type: 'video/webm' });

                // Create a FormData object to send the video file to the server
                const formData = new FormData();
                formData.append('video', blob, 'recorded_video.webm');

                // Use fetch to send the FormData to the server
                fetch('/upload-video', {
                    method: 'POST',
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    messageDiv.textContent = data.message;
                })
                .catch(error => {
                    console.error('Error:', error);
                });

                // Reset variables
                recordedChunks = [];
                startButton.disabled = false;
                stopButton.disabled = true;
            };
        })
        .catch((error) => {
            console.error('Error accessing the camera:', error);
        });

    // Event listener for the "Start" button
    startButton.addEventListener('click', startRecording);

    // Event listener for the "Stop" button
    stopButton.addEventListener('click', stopRecording);
});
