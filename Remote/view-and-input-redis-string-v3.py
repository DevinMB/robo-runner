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
    global look_command
    try:
        if key.char == 'w':
            move_command = 'forward'
        elif key.char == 's':
            move_command = 'backward'
        elif key.char == 'a':
            move_command = 'turn_left'
        elif key.char == 'd':
            move_command = 'turn_right'
        elif key.char == 'q':
            move_command = 'strafe_left'
        elif key.char == 'e':
            move_command = 'strafe_right'
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
        elif key.char == '0':
            look_command = 'look_home'
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
        battery_level = r.get('battery_level').decode('utf-8')


        if frame_data:

            np_arr = np.frombuffer(frame_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            overlay_text_look = f"Battery Level: {battery_level}"
            cv2.putText(frame, overlay_text_look, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.4, (255, 255, 0), 1, cv2.LINE_AA)
            
            overlay_text_look = f"Don't go below: 6600"
            cv2.putText(frame, overlay_text_look, (10, 105), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.4, (255, 255, 0), 1, cv2.LINE_AA)
            
            cv2.imshow('Video Stream', frame)

            r.set('robot_move_command', move_command, ex=input_timeout)
            r.set('robot_look_command', look_command, ex=input_timeout)

            if cv2.waitKey(1) & 0xFF == ord('1'):
                break

        else:
            print("No frame received.")

    except Exception as e:
        print(f"Error retrieving frame: {e}")
        break

cv2.destroyAllWindows()
listener.stop()
