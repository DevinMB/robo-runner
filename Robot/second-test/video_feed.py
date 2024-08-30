import cv2
import redis
import time
import threading


class VideoFeed(threading.Thread):
    def __init__(self, redis_host='192.168.1.250', redis_port=6379, redis_db=0):
        super(VideoFeed, self).__init__()
        self.r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.camera.set(cv2.CAP_PROP_FPS, 60)
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.camera.read()
            if not ret:
                break
                            
            move_command = self.r.get('robot_move_command')
            look_command = self.r.get('robot_look_command')
            
            print(batter_level)

            if move_command is None:
                move_command = "none"
            else:
                move_command = move_command.decode('utf-8')

            overlay_text_move = f"Movement Command: {move_command}"
            cv2.putText(frame, overlay_text_move, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5, (255, 255, 0), 1, cv2.LINE_AA)

            if look_command is None:
                look_command = "none"
            else:
                look_command = look_command.decode('utf-8')

            overlay_text_look = f"Look Command: {look_command}"
            cv2.putText(frame, overlay_text_look, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5, (255, 255, 0), 1, cv2.LINE_AA)
            

            _, buffer = cv2.imencode('.jpg', frame)

            self.r.set('video_stream', buffer.tobytes())

            # (for 60 FPS)
            time.sleep(0.01667)

    def stop(self):
        self.running = False
        self.camera.release()

