import serial
import threading
import time

class RfidReader(threading.Thread):
    
    def __init__(self, serial_port = "/dev/ttyUSB0"):
        threading.Thread.__init__(self)
        self.daemon = True
        self.lock = threading.Lock()
        self.tag_id = ''
        # Open port with default baud rate
        self.ser = serial.Serial(serial_port)
        # Reset Arduino
        self.ser.setDTR(False)
        time.sleep(1)
        self.ser.flushInput()
        self.ser.setDTR(True)
        # Reopen with proper baud rate
        self.ser = serial.Serial(port = serial_port,
            baudrate = 57600,
            timeout = 1.0,
            rtscts = 1,
            dsrdtr = False)
            
    def getid(self):
        self.lock.acquire()
        id = self.tag_id
        self.lock.release()
        return id
    
    def read_id(self):
        line = self.ser.readline()
        line = line.strip()
        if len(line) == 10:
            return line
        return ''

    def run(self):
        print("run")
        while True:
            i = self.read_id()
            self.lock.acquire()
            self.tag_id = i
            self.lock.release()
            time.sleep(0.1)
            
if __name__ == "__main__":
    print "init"
    l = RfidReader()
    l.start()
    
    for x in range(0, 20):
        print("ID %s" % l.getid())
        time.sleep(2)
        
        