import os
import pickle
import face_recognition
import cv2

class FaceRecognition:
    def __init__(self, db_dir):
        """
        Initialize the FaceRecognition with the directory of known face encodings.
        
        Parameters:
        - db_dir (str): Path to the directory containing known face encodings (.pickle files).
        """
        self.db_dir = db_dir
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
            print(f"Created database directory at {self.db_dir}")

    def add_person(self, name, image_path):
        """
        Add a new person to the known faces database.
        
        Parameters:
        - name (str): Name of the person.
        - image_path (str): Path to the person's image.
        
        Returns:
        - str: Success message or error message.
        """
        # Check if the person already exists
        encoding_file = os.path.join(self.db_dir, f"{name}.pickle")
        if os.path.exists(encoding_file):
            return f"Person '{name}' already exists."

        # Load the image
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 0:
            return "No face found in the image."
        elif len(encodings) > 1:
            print(f"WARNING: Multiple faces found in {image_path}. Using the first one.")

        encoding = encodings[0]

        # Save the encoding to a .pickle file
        with open(encoding_file, 'wb') as f:
            pickle.dump(encoding, f)
            print(f"Saved encoding for {name}.")

        return f"Person '{name}' added successfully."

    def recognize(self, face_image):
        """
        Recognize a person from a given image.
        
        Parameters:
        - face_image (numpy.ndarray): Image array in which to recognize faces.
        
        Returns:
        - str: Name of the recognized person or status.
        """
        known_encodings = []
        known_names = []

        # Load all known faces from the folder
        for file in os.listdir(self.db_dir):
            if file.endswith('.pickle'):
                name = file.split('.')[0]
                with open(os.path.join(self.db_dir, file), 'rb') as f:
                    encoding = pickle.load(f)
                    known_encodings.append(encoding)
                    known_names.append(name)
                    print(f"Loaded {name} face encoding")

        # Find the face encodings in the provided image
        face_encodings = face_recognition.face_encodings(face_image)

        if len(face_encodings) == 0:
            return "no_persons_found"

        # Compare each face found in the image to known faces
        results = []
        for encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, encoding)
            name = "unknown_person"

            # Use the known face with the smallest distance if any match
            face_distances = face_recognition.face_distance(known_encodings, encoding)
            best_match_index = None
            if len(face_distances) > 0:
                best_match_index = face_distances.argmin()
                if matches[best_match_index]:
                    name = known_names[best_match_index]

            results.append(name)

        # If multiple faces are detected, return the list
        if len(results) == 1:
            return results[0]
        else:
            return results  # List of names/statuses
