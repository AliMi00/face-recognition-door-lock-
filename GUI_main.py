import sys
import cv2
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QTimer, Qt


# API endpoint
url_recognition = 'http://172.30.216.123:5000/recognize'
url_add_person = 'http://172.30.216.123:5000/add_person'


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Recognition GUI")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

        # Initialize camera and timer
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            QMessageBox.critical(self, "Error", "Could not open webcam")
            sys.exit(1)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30ms for ~30 FPS

    def init_ui(self):
        # Widgets
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.capture_recognize_button = QPushButton("Capture & Recognize")
        self.capture_add_button = QPushButton("Capture & Add Person")
        self.result_label = QLabel("Result:")
        self.result_display = QLabel()
        self.result_display.setStyleSheet("font-size: 18px; color: white;")
        self.result_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_label = QLabel("Live Video Feed")
        self.image_label.setFixedSize(640, 480)  # Set a fixed size for the video feed
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")

        # Layouts
        form_layout = QHBoxLayout()
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.capture_recognize_button)
        button_layout.addWidget(self.capture_add_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.image_label, stretch=2)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.result_display, stretch=1)

        self.setLayout(main_layout)

        # Connections
        self.capture_recognize_button.clicked.connect(self.capture_and_recognize)
        self.capture_add_button.clicked.connect(self.capture_and_add_person)

    def update_frame(self):
        """Continuously update the live video feed."""
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to QImage
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width = frame_rgb.shape[:2]
            height, width, channel = frame_rgb.shape
            qimg = QImage(frame_rgb.data, width, height, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)

            # Display the QImage on the label
            self.image_label.setPixmap(
                pixmap.scaled(
                    self.image_label.width(), self.image_label.height(), Qt.AspectRatioMode.KeepAspectRatio
                )
            )

    def capture_frame(self):
        """Capture the current frame from the live feed."""
        ret, frame = self.cap.read()
        if ret:
            # Save the frame as an image file
            image_path = 'captured_image.jpg'
            cv2.imwrite(image_path, frame)
            return image_path
        else:
            QMessageBox.critical(self, "Error", "Failed to capture image")
            return None

    def send_image(self, image_path):
        with open(image_path, 'rb') as img:
            files = {'image': img}
            response = requests.post(url_recognition, files=files)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to send image. Status code: {response.status_code}"}

    def add_person(self, name, image_path):
        try:
            with open(image_path, 'rb') as img:
                data = {'name': name}
                files = {'image': img}
                response = requests.post(url_add_person, data=data, files=files)

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to add person. Status code: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    def capture_and_recognize(self):
        image_path = self.capture_frame()
        if image_path:
            response = self.send_image(image_path)
            self.display_result(response)

    def capture_and_add_person(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter a name.")
            return

        image_path = self.capture_frame()
        if image_path:
            response = self.add_person(name, image_path)
            self.display_result(response)

    def display_result(self, response):
        if "result" in response:
            self.result_display.setText(f"Recognition Result: {response['result']}")
        elif "error" in response:
            self.result_display.setText(f"Error: {response['error']}")
        else:
            self.result_display.setText("Unexpected response format.")

    def closeEvent(self, event):
        """Release the camera when the application closes."""
        self.cap.release()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
