from flask import Flask, request, jsonify, render_template
import cv2  # Import OpenCV
import os
import shutil

from datetime import datetime

app = Flask(__name__)

print("worked")

directory_name = "frames"

# Check if the directory exists
if os.path.exists(directory_name):
    # Remove the directory and all its contents
    shutil.rmtree(directory_name)

# Recreate the directory
os.makedirs(directory_name)

@app.route('/')
def index():
    # Render an HTML template containing the video capture functionality.
    return render_template('index2.html')



last_seconds = 0

@app.route('/upload-video', methods=['POST'])
def upload_video():
    global last_seconds  # Indicate that we'll be using the global variable

    video = request.files['video']
    if video:
        # Ensure the frames directory exists
        frames_dir = 'frames'
        os.makedirs(frames_dir, exist_ok=True)

        # Save the video clip to a temporary file
        temp_video_path = os.path.join('temp', f"{datetime.now().strftime('%Y%m%d%H%M%S')}.webm")
        os.makedirs('temp', exist_ok=True)
        video.save(temp_video_path)

        # Open the video file and start processing
        cap = cv2.VideoCapture(temp_video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)  # Get frames per second of the video
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break  # Break the loop if there are no frames left

            # Use the global last_seconds variable to keep track of time
            seconds = last_seconds + int(frame_count / fps)
            frame_within_second = int(frame_count % fps)

            # Save each frame with the naming scheme based on seconds and frame count
            frame_filename = f'{seconds}s{frame_within_second}f.png'
            cv2.imwrite(os.path.join(frames_dir, frame_filename), frame)
            frame_count += 1

        # Update the last_seconds global variable for the next video
        last_seconds += int(frame_count / fps) + (1 if frame_count % fps > 0 else 0)

        cap.release()

        # Optionally, remove the temporary video file after processing
        os.remove(temp_video_path)
        print(f"Video uploaded and processed into {frame_count}")
        return jsonify({"message": f"Video uploaded and processed into {frame_count} frames successfully"}), 200

    else:
        print("no video uploaded")
        return jsonify({"error": "No video uploaded"}), 400


if __name__ == '__main__':
    app.run(debug=True)
    #ngrok http http://127.0.0.1:5000