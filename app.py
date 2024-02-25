from flask import Flask, render_template, request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

# Configure file uploads
videos = UploadSet("videos", extensions=("mp4", "mov"))
app.config["UPLOADED_VIDEOS_DEST"] = "uploads"
configure_uploads(app, videos)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "video" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    video = request.files["video"]

    if video.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if video and videos.allowed(video.filename):
        # Save the video
        video_path = f"uploads/{video.filename}"
        video.save(video_path)

        # You can add further processing or save the video information in a database

        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return jsonify({"error": "Invalid file format"}), 400
    
def process_video(filename):
    # Use FFmpeg or another tool to extract frames
    # Example using FFmpeg
    import subprocess

    output_folder = f"uploads/frames/{filename}_frames"
    subprocess.run(["ffmpeg", "-i", f"uploads/videos/{filename}", f"{output_folder}/frame_%03d.jpg"])

if __name__ == "__main__":


    app.run(debug=True)
#ngrok http http://localhost:5000

