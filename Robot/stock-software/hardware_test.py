import sys
import time
import Board as Board

Board.setPWMServoPulse(1, 1800, 300) 
time.sleep(0.3)
Board.setPWMServoPulse(1, 1500, 300) 
time.sleep(0.3)
Board.setPWMServoPulse(1, 1200, 300) 
time.sleep(0.3)
Board.setPWMServoPulse(1, 1500, 300) 
time.sleep(1.5)

Board.setPWMServoPulse(2, 1200, 300) 
time.sleep(0.3)
Board.setPWMServoPulse(2, 1500, 300) 
time.sleep(0.3)
Board.setPWMServoPulse(2, 1800, 300)
time.sleep(0.3)
Board.setPWMServoPulse(2, 1500, 300) 
time.sleep(1.5)

Board.setMotor(1, 45)
time.sleep(0.5)
# Board.setMotor(1, 0)
time.sleep(1)
        
Board.setMotor(2, 45)
time.sleep(0.5)
# Board.setMotor(2, 0)
time.sleep(1)

Board.setMotor(3, 45)
time.sleep(0.5)
# Board.setMotor(3, 0)
time.sleep(1)

Board.setMotor(4, 45)
time.sleep(0.5)
# Board.setMotor(4, 0)
time.sleep(1)
