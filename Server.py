import socket
import time
import threading
import struct

PLAYERS = []
def send_thread_interval():
    threading.Timer(interval=1.0,function=send_thread_interval).start()
    sendBraodcast()

def sendBraodcast():
    message = struct.pack("Ibh", 0xfeedbeef, 0x2,PORT)
    UDPServerSocket.sendto(message,("<broadcast>",13117))
    
class ClientThread(threading.Thread):

    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)

    def run(self):
        group_name= self.csocket.recvfrom(1024)
        print(repr(group_name[0]))
        PLAYERS.append(group_name)
        

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

PORT = 2027
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# Bind to address and ip
TCPServerSocket.bind((local_ip, PORT))

print("Server started,listening on IP address",local_ip)
UDPServerSocket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
send_thread_interval()

# Listen for incoming datagrams
while(True):
    TCPServerSocket.listen(1)
    clientsock, clientAddress = TCPServerSocket.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
