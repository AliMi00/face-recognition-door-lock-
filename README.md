
# Face Recognition API

This is a simple Flask API that provides two main functionalities:

1. Recognizing faces from an uploaded image.
2. Adding a new person with their face to the known faces database.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [CLI endpoint](#cli-endpoint)
- [GUI endpoint](#gui-endpoint)
- [Folder Structure](#folder-structure)
- [Acknowledgements](#acknowledgements)


## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure that you have OpenCV and numpy installed:
   ```bash
   pip install opencv-python numpy
   ```

4. (Optional) Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/MacOS
   # or
   venv\Scripts\activate  # For Windows
   ```

5. Create the necessary folders for uploading images and storing known faces:
   ```bash
   mkdir known_faces uploads
   ```

## Usage

To start the API, run the following command:

```bash
python app.py
```

By default, the API will run on `http://0.0.0.0:5000`.

## API Endpoints

### 1. `POST /recognize`

This endpoint is used to recognize faces from an uploaded image.

- **URL**: `/recognize`
- **Method**: `POST`
- **Payload**: A form-data with the key `image` containing the image file.
- **Response**:
  - `200 OK`: Returns the recognized faces.
  - `400 Bad Request`: If no image is provided or if an invalid file is uploaded.

#### Example Request (using `curl`):
```bash
curl -X POST http://localhost:5000/recognize -F 'image=@path_to_image.jpg'
```

#### Example Response:
```json
{
  "result": ["Person1"]
}
```

### 2. `POST /add_person`

This endpoint is used to add a new person to the known faces database.

- **URL**: `/add_person`
- **Method**: `POST`
- **Payload**: A form-data with the following fields:
  - `name`: The name of the person.
  - `image`: The image file of the person.
- **Response**:
  - `200 OK`: Returns a success message.
  - `400 Bad Request`: If the required fields are missing or if an invalid file is uploaded.

#### Example Request (using `curl`):
```bash
curl -X POST http://localhost:5000/add_person -F 'name=John Doe' -F 'image=@path_to_image.jpg'
```

#### Example Response:
```json
{
  "message": "John Doe added successfully"
}
```

### 3. `GET /`

A simple health-check endpoint that returns a message and lists available API endpoints.

#### Example Request:
```bash
curl http://localhost:5000/
```

#### Example Response:
```json
{
  "message": "Face Recognition API",
  "endpoints": {
    "POST /recognize": "Recognize faces in an image.",
    "POST /add_person": "Add a new person with an image."
  }
}
```

## CLI Endpoint

## CLI Endpoint

The API also provides a CLI tool for capturing an image from the webcam and sending it to the API for face recognition.

To use the CLI tool, follow these steps:

1. Ensure you have a webcam connected to your system.

2. Run the CLI tool:
   ```bash
   python CLI_main.py
   ```

3. Follow the interactive prompts:
    - Choose an option to either recognize faces or add a new person.
    - If you choose to recognize faces, the webcam will open, and you can capture an image by pressing the `Space` key.
    - If you choose to add a new person, you will be prompted to enter the person's name and capture an image.


The CLI tool will display the response from the API, including the recognized faces or any error messages.

## GUI Endpoint

## GUI Endpoint

The API also provides a simple GUI tool for capturing an image from the webcam and sending it to the API for face recognition or adding a new person to the database.

### Features

- Capture an image from the webcam.
- Send the captured image to the API for face recognition.
- Add a new person with their face to the known faces database.

### Usage

1. Ensure you have a webcam connected to your system.

2. Run the GUI tool:
   ```bash
   python GUI_main.py
   ```

3. The GUI window will open with the following components:
   - **Name Input**: A text field to enter the name of the person (used when adding a new person).
   - **Capture & Recognize Button**: Captures an image from the webcam and sends it to the API for face recognition.
   - **Capture & Add Person Button**: Captures an image from the webcam and sends it to the API to add a new person with the entered name.
   - **Result Display**: Displays the result of the recognition or the status of adding a new person.

4. Follow the on-screen instructions:
   - Enter the name in the text field if you are adding a new person.
   - Click the "Capture & Recognize" button to recognize faces.
   - Click the "Capture & Add Person" button to add a new person.

The GUI tool will display the response from the API, including the recognized faces or any error messages.



## Folder Structure

- `known_faces/`: This directory contains the images of known faces, categorized by the person’s name.
- `uploads/`: This directory temporarily stores uploaded images for recognition.

## Acknowledgements

- The face recognition functionality is powered by the `FaceRecognition` class from the `face_rec` module.
- This API utilizes OpenCV for image processing.

