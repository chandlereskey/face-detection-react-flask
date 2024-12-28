import base64

import numpy as np
from flask import Flask, request, Response, jsonify
from flask_cors import CORS, cross_origin
from face_recognition.generate_embeddings import generate_embeddings
import cv2
from face_recognition.detect_face_and_return_frame import embeddings, detect_faces


class Camera:
    def __init__(self):
        # Initialize the camera
        self.cap = cv2.VideoCapture(0)

    def __del__(self):
        # Release the camera
        self.cap.release()

    def get_frame(self):
        # Capture frame-by-frame
        ret, frame = self.cap.read()
        if not ret:
            return None
        new_frame = detect_faces(frame, embeddings)
        # Encode the frame in JPEG format
        ret, jpeg = cv2.imencode('.jpg', new_frame)
        return jpeg.tobytes()


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def gen(frame):
    while True:
        new_frame = detect_faces(frame, embeddings)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/video-stream-from-flask", methods=['GET'])
def generate_video():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video-stream-from-flask-example', methods=['POST'])
def video_stream():
    data = request.json
    image_data = data['image']

    # Decode the base64 image data
    image_data = base64.b64decode(image_data.split(',')[1])
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Process the image using OpenCV (example: convert to grayscale)
    # gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = detect_faces(img, embeddings)

    # Encode the processed image to base64
    _, buffer = cv2.imencode('.jpg', img)
    processed_image = base64.b64encode(buffer).decode('utf-8')
    processed_image = f"data:image/jpeg;base64,{processed_image}"

    return jsonify({'image': processed_image})


@app.route("/generate_embeddings", methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type'])
def generate_txt_file():
    if len(request.files) == 0:
        return "no images"
    generate_embeddings(request.files)
    return 'embeddings generated'

if __name__ == '__main__':
    app.run(debug=True, port=5001)