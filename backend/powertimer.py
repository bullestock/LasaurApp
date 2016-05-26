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
        self.idle_count = 0

    def reset(self):
        self.idle_count = 0
        
    def run(self):
        print "PowerTimer start"
        self.idle_count = 0
        last_left = -1
        while True:
            time.sleep(60)
            self.idle_count = self.idle_count+1
            print "PowerTimer idle count: %d" % self.idle_count
            if self.idle_count > self.WARNING_TIME:
                left = self.MAX_IDLE_TIME-self.idle_count
                plural = 's'
                if left < 2:
                    plural = ''
                if (left > 0) and (left != last_left):
                    self.callback("Shutting down in %d minute%s" % (left, plural))
                    last_left = left
            if self.idle_count > self.MAX_IDLE_TIME:
                GPIO.output(self.pin, GPIO.HIGH)
                time.sleep(60)
                
        