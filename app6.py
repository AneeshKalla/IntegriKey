from flask import Flask, request, jsonify, render_template, send_file, abort
import cv2  # Import OpenCV
import os
import shutil
from ultralytics import YOLO
from datetime import datetime
import numpy as np
from PIL import Image


import logging
logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
app.debug = True


print("worked")

model = YOLO('yolov8m-seg.pt')

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
    return render_template('index5.html')



last_seconds = 0
frames_list = []  # Store frames here


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
           

            if frame_count % int(fps) == 0 and last_seconds%2 == 0:  # Capture one frame per second
                frames_list.append(frame)  # Add the frame to the list
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

        process_frames_with_yolo(5)

        print(f"Video uploaded and processed into {frame_count}")
        return jsonify({"message": f"Video uploaded and processed into {frame_count} frames successfully"}), 200

    else:
        print("no video uploaded")
        return jsonify({"error": "No video uploaded"}), 400


results = []


output_dir = 'yoloFrames'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def process_frames_with_yolo(size):
    print("starting processing")
    index = 0
    for frame in frames_list[len(frames_list)-size:]:
        print("got to frame")
        pred = model(frame)  # Assume this returns a list of predictions with masks
        frame_with_overlay = pred[0].plot()
        results.append((frame, frame_with_overlay, pred))

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{output_dir}/overlay_{index}_{timestamp}.png"
        index += 1
        cv2.imwrite(filename, frame_with_overlay)  
    #return results




@app.route('/last-overlayed-image', methods=['GET'])
def last_overlayed_image():
   
    #print("started")
    last_result = results[-1]  # Get the last element in results
    #print("last result acquired")
    last_image = last_result[1]
    #print("last image acquired")
    #print(last_image)
    #if last_image != None:
    #print("past if statement")
    pil_image = Image.fromarray(last_image.astype('uint8'))
    filename = 'last_image.png'
    # Save the PIL Image object to a file
    filename = 'last_image.png'  # Save last_image to a file or use an existing filename
    pil_image.save(filename)  # Assuming last_image is a PIL Image or similar; adjust saving accordingly
    #print("saved")
    return send_file(filename, mimetype='image/png')
        #else:
            #return abort(404, description="No overlaid image found.")





if __name__ == '__main__':
    app.run(debug=True)
    #ngrok http http://127.0.0.1:5000



    #data after second 225 is good