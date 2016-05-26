import threading
import time
import RPi.GPIO as GPIO

class PowerTimer(threading.Thread):
    MAX_IDLE_TIME = 15
    WARNING_TIME = 5
    
    def __init__(self, pin, callback):
        threading.Thread.__init__(self)
        self.pin = pin
        self.callback = callback

    def run(self):
        print "PowerTimer start"
        idle_count = 0
        last_left = -1
        while True:
            time.sleep(60)
            idle_count = idle_count+1
            print "PowerTimer idle count: %d" % idle_count
            if idle_count > self.WARNING_TIME:
                left = self.MAX_IDLE_TIME-idle_count
                plural = 's'
                if left < 2:
                    plural = ''
                if (left > 0) and (left != last_left):
                    self.callback("Shutting down in %d minute%s" % (left, plural))
                    last_left = left
            if idle_count > self.MAX_IDLE_TIME:
                GPIO.output(self.pin, GPIO.HIGH)
                time.sleep(60)
                
        