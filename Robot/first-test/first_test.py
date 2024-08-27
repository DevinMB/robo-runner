import time
import Board as Board
from video_feed import VideoFeed
import redis

# Set up Redis connection
r = redis.Redis(host='192.168.1.250', port=6379, db=0)

# Create and start the video feed thread
video_feed = VideoFeed()
video_feed.start()

try:
    while True:
        # Fetch the current command from Redis
        current_command = r.get('robot_command')

        if current_command is not None:
            current_command = current_command.decode('utf-8')

            if current_command == 'forward':
                # Move all motors forward
                Board.setMotor(1, 45)
                Board.setMotor(2, 45)
                Board.setMotor(3, 45)
                Board.setMotor(4, 45)

            elif current_command == 'backward':
                # Move all motors backward
                Board.setMotor(1, -45)
                Board.setMotor(2, -45)
                Board.setMotor(3, -45)
                Board.setMotor(4, -45)

            elif current_command == 'left':
                # Turn left (motors 1 and 3 backward, motors 2 and 4 forward)
                Board.setMotor(1, -45)
                Board.setMotor(2, 45)
                Board.setMotor(3, -45)
                Board.setMotor(4, 45)

            elif current_command == 'right':
                # Turn right (motors 1 and 3 forward, motors 2 and 4 backward)
                Board.setMotor(1, 45)
                Board.setMotor(2, -45)
                Board.setMotor(3, 45)
                Board.setMotor(4, -45)

            elif current_command == 'none':
                # Stop all motors
                Board.setMotor(1, 0)
                Board.setMotor(2, 0)
                Board.setMotor(3, 0)
                Board.setMotor(4, 0)

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
