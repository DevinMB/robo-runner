import redis
import cv2
import numpy as np
from pynput import keyboard

r = redis.Redis(host='192.168.1.250', port=6379, db=0)

input_timeout = 1

move_command = "none"
look_command = "none"

def on_press(key):
    global move_command
    try:
        if key.char == 'w':
            move_command = 'forward'
        elif key.char == 's':
            move_command = 'backward'
        elif key.char == 'a':
            move_command = 'left'
        elif key.char == 'd':
            move_command = 'right'
    except AttributeError:
        pass

    try:
        if key.char == 'o':
            look_command = 'look_up'
        elif key.char == 'l':
            look_command = 'look_down'
        elif key.char == 'k':
            look_command = 'look_left'
        elif key.char == ';':
            look_command = 'look_right'
    except AttributeError:
        pass

def on_release(key):
    global move_command
    global look_command

    move_command = 'none'
    look_command = 'none'
    if key == keyboard.Key.esc:
        return False 

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

while True:
    try:

        frame_data = r.get('video_stream')


        if frame_data:

            np_arr = np.frombuffer(frame_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            cv2.imshow('Video Stream', frame)

            r.set('robot_move_command', move_command, ex=input_timeout)
            r.set('robot_look_command', look_command, ex=input_timeout)

            print(cv2.waitKey())

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            print("No frame received.")

    except Exception as e:
        print(f"Error retrieving frame: {e}")
        break

cv2.destroyAllWindows()
listener.stop()
