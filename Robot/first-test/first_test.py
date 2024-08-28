import time
import Board as Board
from video_feed import VideoFeed
import redis

# Set up Redis connection
r = redis.Redis(host='192.168.1.250', port=6379, db=0)

# Set Home Position
servo1_home_position = 1050  # Default neutral position
servo2_home_position = 1600  # Default neutral position

# Initialize the current servo positions
servo1_position = servo1_home_position  
servo2_position = servo2_home_position  

# Define the step size for each movement
servo_step = 50

# Define the limits for the servo positions
vertical_servo_min = 500  
vertical_servo_max = 1500

horizontal_servo_min = 500  
horizontal_servo_max = 2500



# Create and start the video feed thread
video_feed = VideoFeed()
video_feed.start()

try:

    Board.setPWMServoPulse(1, servo1_position, 300)
    time.sleep(1)
    Board.setPWMServoPulse(2, servo2_position, 300)
    time.sleep(1)

    while True:
        # Fetch the current command from Redis
        move_command = r.get('robot_move_command')
        look_command = r.get('robot_look_command')

        if look_command is not None: 
            look_command = look_command.decode('utf-8')

            if look_command == 'look_down':
                # Increment the servo1 position
                servo1_position = min(servo1_position + servo_step, vertical_servo_max)
                Board.setPWMServoPulse(1, servo1_position, 300)
            elif look_command == 'look_up':
                # Decrement the servo1 position
                servo1_position = max(servo1_position - servo_step, vertical_servo_min)
                Board.setPWMServoPulse(1, servo1_position, 300)
            elif look_command == 'look_right':
                # Decrement the servo2 position
                servo2_position = max(servo2_position - servo_step, horizontal_servo_min)
                Board.setPWMServoPulse(2, servo2_position, 300)
            elif look_command == 'look_left':
                # Increment the servo2 position
                servo2_position = min(servo2_position + servo_step, horizontal_servo_max)
                Board.setPWMServoPulse(2, servo2_position, 300)
            elif look_command == 'look_home':
                Board.setPWMServoPulse(1, servo1_position, 300)
                time.sleep(1)
                Board.setPWMServoPulse(2, servo2_position, 300)
                time.sleep(1)

        if move_command is not None:
            move_command = move_command.decode('utf-8')

            if move_command == 'forward':
                # Move all motors forward
                Board.setMotor(1, 100)
                Board.setMotor(2, 100)
                Board.setMotor(3, 100)
                Board.setMotor(4, 100)

            elif move_command == 'backward':
                # Move all motors backward
                Board.setMotor(1, -100)
                Board.setMotor(2, -100)
                Board.setMotor(3, -100)
                Board.setMotor(4, -100)

            elif move_command == 'turn_left':
                # Turn left (motors 1 and 3 backward, motors 2 and 4 forward)
                Board.setMotor(1, -60)
                Board.setMotor(2, 60)
                Board.setMotor(3, -60)
                Board.setMotor(4, 60)

            elif move_command == 'turn_right':
                # Turn right (motors 1 and 3 forward, motors 2 and 4 backward)
                Board.setMotor(1, 60)
                Board.setMotor(2, -60)
                Board.setMotor(3, 60)
                Board.setMotor(4, -60)

            elif move_command == 'strafe_left':
                # Turn left (motors 1 and 3 backward, motors 2 and 4 forward)
                Board.setMotor(1, -60)
                Board.setMotor(2, 60)
                Board.setMotor(3, 60)
                Board.setMotor(4, -60)

            elif move_command == 'strafe_right':
                # Turn right (motors 1 and 3 forward, motors 2 and 4 backward)
                Board.setMotor(1, 60)
                Board.setMotor(2, -60)
                Board.setMotor(3, -60)
                Board.setMotor(4, 60)
            
            elif move_command == 'none':
                # Stop all motors
                Board.setMotor(1, 0)
                Board.setMotor(2, 0)
                Board.setMotor(3, 0)
                Board.setMotor(4, 0)
        # print(f"servo1-p: {servo1_position} servo2-p: {servo2_position}")
        # Sleep for a short time to avoid overwhelming the Redis server
        time.sleep(0.1)

finally:
    # Ensure that all motors are stopped and the video feed thread is properly terminated
    Board.setMotor(1, 0)
    Board.setMotor(2, 0)
    Board.setMotor(3, 0)
    Board.setMotor(4, 0)

    video_feed.stop()
    video_feed.join()
