import socket
import time
import threading
import struct

def send_thread_interval():
    threading.Timer(interval=1.0,function=sendBraodcast).start()

def sendBraodcast():
    message = struct.pack("Ibh", 0xfeedbeef, 0x2,PORT)
    UDPServerSocket.sendto(message,("<broadcast>",13117))
    
class ClientThread(threading.Thread):

    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)

    def run(self):
        print ("Connection from : ", clientAddress)
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg=='bye':
              break
            print ("from client", msg)
            self.csocket.send(bytes(msg,'UTF-8'))
        print ("Client at ", clientAddress , " disconnected...")

HOST = "127.0.0.1"
PORT   = 2027
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# Bind to address and ip
TCPServerSocket.bind((HOST, PORT))
print("Server started,listening on IP address",HOST)
UDPServerSocket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
send_thread_interval()

# Listen for incoming datagrams
while(True):
    TCPServerSocket.listen(1)
    clientsock, clientAddress = TCPServerSocket.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()