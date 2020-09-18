import socket
import time
from threading import RLock

WAIT_TIME_UNIT=0.01

class VCU_protocol:
    def __init__(self, host, port):
        self.connected = False        
        self.port = int(port)
        self.host = host
        self.commlock = RLock()        
        self.connect()
    
    def reconnect(self):
        try:
            self.sock.close()
            self.connected = False
        except socket.error:
            pass
        self.connect()
        
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.last_comm_timeout = False
        print ("Connecting to Host", self.host, ", Port", self.port)
        try:
            self.sock.setblocking(1)
        except:
            pass
        try:
            self.sock.connect((self.host, self.port))
        except Exception as e:
            print ("Exception occured while connecting")
            print (e.__class__)
            print (e)
            self.connected = False
        else:
            print ("Success.")
            resp = ""
            try:
                resp += self.sock.recv(10000)
            except socket.error:
                pass
            print ("resp = ",resp)
            self.connected = True
        self.sock.setblocking(0)
      
    def vacuum(self):
        resp = self.communicate("RPV1")
        #print resp
        _,value=resp.split("\t")
        vacuum=float(value) 
        return (vacuum)
        
    def OnOff(self,state):
        resp=self.communicate("SHV1,"+str(state))
        
 
    def communicate(self, command, timeout=2.0):
        # send command
        with self.commlock:
            #print "communicate called"
            try:
                self.sock.send(command+"\r")
            except socket.error:
                self.connected = False
            # get an answer
            time.sleep(0.1)
            resp = ""
            try:
                resp += self.sock.recv(10000)
            except socket.error:
                pass
            return resp

"""
    def communicate(self, command, timeout=2.0):
        # send command
        with self.commlock:
            #print "communicate called"
            try:
                self.sock.send(command)
            except socket.error:
                self.connected = False
            # get an answer
            resp = ""
            try:
                resp += self.sock.recv(10000)
            except socket.error:
                pass
            tstart = time.time()
            tend = tstart
            # really wait (block!) until end-of-line character is reached
            while( (len(resp)==0 or resp[-1]!='\n') and tend-tstart<timeout):
                #print "Delay!"
                try:
                    resp += self.sock.recv(10000)
                except socket.error:
                    pass
                time.sleep(WAIT_TIME_UNIT)
                tend = time.time()
            self.last_comm_timeout = (tend-tstart>=timeout)
            #print resp
            return resp
"""
