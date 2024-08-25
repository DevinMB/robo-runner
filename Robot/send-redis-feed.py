import cv2
import redis
import time

r = redis.Redis(host='192.168.1.250', port=6379, db=0)

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
camera.set(cv2.CAP_PROP_FPS, 60) 

while True:
    ret, frame = camera.read()
    if not ret:
        break

    current_command = r.get('robot_command')

    if current_command is None:
        current_command = "none"
    else:
        current_command = current_command.decode('utf-8')  

    overlay_text = f"Current Command: {current_command}"
    cv2.putText(frame, overlay_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, (255, 0, 0), 1, cv2.LINE_AA)

    _, buffer = cv2.imencode('.jpg', frame)

    r.set('video_stream', buffer.tobytes())

    # (for 60 FPS)
    time.sleep(0.01667)

camera.release()
