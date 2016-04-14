import serial
import threading
import time

class RfidReader(threading.Thread):
    
    def __init__(self, serial_port = "/dev/ttyUSB0"):
        threading.Thread.__init__(self)
        self.daemon = True
        self.lock = threading.Lock()
        self.tag_id = ''
        self.ser = serial.Serial(
            port = serial_port,
            baudrate = 9600,
            timeout = 1.0)
            
    def getid(self):
        self.lock.acquire()
        id = self.tag_id
        self.lock.release()
        return id
    
    def read_id(self):
        STX = 2
        ETX = 3
        b = bytearray()
        gotStart = False
        self.ser.flushInput()
        while True:
            d = self.ser.read(1)
            if len(d) == 0:
                return b
            c = bytearray(d)[0]
            if c == STX:
                gotStart = True
            elif c == ETX:
                return b.decode()
            elif gotStart and c >= 32 and c < 127:
                b.append(c)

    def run(self):
        bad_reads = 0
        while True:
            i = self.read_id()
            if len(i) == 12:
                self.lock.acquire()
                self.tag_id = i
                self.lock.release()
                bad_reads = 0
            else:
                bad_reads = bad_reads+1
            if bad_reads >= 10:
                # No card found for a while, clear ID
                self.lock.acquire()
                self.tag_id = ''
                self.lock.release()
                
            time.sleep(1)
            
if __name__ == "__main__":
    print "init"
    l = RfidReader()
    l.start()
    
    for x in range(0, 20):
        print l.getid()
        time.sleep(2)
        
        