import redis
import time
import Board as Board
import threading


class BatteryFeed(threading.Thread):
    def __init__(self, redis_host='192.168.1.250', redis_port=6379, redis_db=0):
        super(BatteryFeed, self).__init__()
        self.r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        self.running = True

    def run(self):
        while self.running:
            
            check_count = 0
            sum_of_levels = 0
            while check_count <= 10:
                battery_level =Board.getBattery()
                sum_of_levels += battery_level
                
            avg_level = sum_of_levels / check_count
            self.r.set('battery_level', avg_level)

            check_count = 0
            sum_of_levels = 0
        
            time.sleep(5)

    def stop(self):
        self.running = False