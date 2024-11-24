import cv2
import requests

# API endpoint
url = 'http://your-api-url.com/recognize'

# Capture image from webcam
def capture_image():
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam")
        return None

    # Read a frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame")
        return None

    # Save the frame to a file
    image_path = 'captured_image.jpg'
    cv2.imwrite(image_path, frame)

    # Release the camera
    cap.release()

    return image_path

# Send image to API
def send_image(image_path):
    with open(image_path, 'rb') as img:
        files = {'file': img}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        print("Image successfully sent to API!")
        print("Response:", response.json())
    else:
        print(f"Failed to send image. Status code: {response.status_code}")

# Interactive CLI loop
def cli_interaction():
    while True:
        user_input = input("Do you want to take a picture and send it to the API? (yes/no): ").strip().lower()

        if user_input in ['yes', 'y']:
            # Capture the image
            image_path = capture_image()

            if image_path:
                # Send the captured image to the API
                send_image(image_path)
        elif user_input in ['no', 'n']:
            print("Exiting the program.")
            break
        else:
            print("Invalid input, please type 'yes' or 'no'.")

if __name__ == "__main__":
    cli_interaction()
