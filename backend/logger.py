import sqlite3, time
import threading

class AccessLogger(object):
    
    def __init__(self):
        self.lock = threading.Lock()
        self.conn = sqlite3.connect('/var/log/lasersaur/access.db')
        with self.conn:
            cur = self.conn.cursor()    
            cur.execute('SELECT SQLITE_VERSION()')
            data = cur.fetchone()
            print "SQLite version: %s" % data  
            query = ("CREATE TABLE IF NOT EXISTS log(user VARCHAR(80),"
                     "stamp TIMESTAMP,"
                     "action TEXT)")
            cur.execute(query)
            cur.execute('SELECT COUNT(*) FROM log')
            data = cur.fetchone()
            print "Rows: %s" % data
            
    def log(self, user, action):
        self.lock.acquire()
        with self.conn:
            cur = self.conn.cursor()    
            cur.execute(("INSERT INTO log (user, stamp, action) "
                         "VALUES ('%s', DATETIME('now'), '%s')") % (user, action))
        self.lock.release()
                         
if __name__ == "__main__":
    print "init"
    l = AccessLogger()
    l.log('mig', 'Card inserted')
    time.sleep(10)
    l.log('mig', 'Cut')
    time.sleep(10)
    l.log('mig', 'Card removed')
        
        