import redis
import cv2
import numpy as np

r = redis.Redis(host='192.168.1.250', port=6379, db=0)

while True:
    try:
        frame_data = r.get('video_stream')

        if frame_data:
            # Convert bytes to numpy array
            np_arr = np.frombuffer(frame_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                       
            cv2.imshow('Video Stream', frame)

            # Break loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("No frame received.")
    except Exception as e:
        print(f"Error retrieving frame: {e}")
        break

cv2.destroyAllWindows()
