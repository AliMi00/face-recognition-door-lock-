import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from face_rec.face_rec import FaceRecognition

app = Flask(__name__)

# Configuration
KNOWN_FACES_DIR = 'known_faces'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['KNOWN_FACES_DIR'] = KNOWN_FACES_DIR
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize FaceRecognition
face_recognizer = FaceRecognition(app.config['KNOWN_FACES_DIR'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/recognize', methods=['POST'])
def recognize():
    """
    Endpoint to recognize faces in an uploaded image.
    Expects a file with key 'image'.
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request.'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No image selected for uploading.'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)
        print(f"Image saved to {image_path}")

        # Load image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            return jsonify({'error': 'Invalid image file.'}), 400

        # Convert image from BGR (OpenCV) to RGB (face_recognition)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Recognize faces
        result = face_recognizer.recognize(rgb_image)

        # Optionally, remove the uploaded image after processing
        os.remove(image_path)

        return jsonify({'result': result}), 200
    else:
        return jsonify({'error': 'Allowed image types are png, jpg, jpeg.'}), 400

@app.route('/add_person', methods=['POST'])
def add_person():
    """
    Endpoint to add a new person to the known faces database.
    Expects 'name' and a file with key 'image'.
    """
    if 'name' not in request.form:
        return jsonify({'error': 'No name provided.'}), 400

    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request.'}), 400

    name = request.form['name']
    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No image selected for uploading.'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)
        print(f"Image saved to {image_path}")

        # Add person to the database
        message = face_recognizer.add_person(name, image_path)

        # Optionally, remove the uploaded image after processing
        os.remove(image_path)

        if "successfully" in message:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 400
    else:
        return jsonify({'error': 'Allowed image types are png, jpg, jpeg.'}), 400

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Face Recognition API',
        'endpoints': {
            'POST /recognize': 'Recognize faces in an image.',
            'POST /add_person': 'Add a new person with an image.'
        }
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
