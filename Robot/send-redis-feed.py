import cv2
import redis
import time

# Initialize Redis connection
r = redis.Redis(host='192.168.1.250', port=6379, db=0)

# Initialize camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
camera.set(cv2.CAP_PROP_FPS, 60)  # Optional: Attempt to set FPS to 60

while True:
    ret, frame = camera.read()
    if not ret:
        break

    # Fetch the current command from Redis
    current_command = r.get('robot_command')

    if current_command is None:
        current_command = "none"
    else:
        current_command = current_command.decode('utf-8')  # Decode byte to string

    # Add overlay text to the frame with the current command from Redis
    overlay_text = f"Current Command: {current_command}"
    cv2.putText(frame, overlay_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, (255, 0, 0), 1, cv2.LINE_AA)

    # Encode frame as JPEGaaaaa
    _, buffer = cv2.imencode('.jpg', frame)

    # Send frame to Redis stream
    r.set('video_stream', buffer.tobytes())

    # Optional sleep for frame rate control (e.g., for 60 FPS)
    time.sleep(0.01667)

# Release the camera when done
camera.release()
