import socket
import time
import threading
import struct

Group1 = []
Group2 = []
PLAYERS = []
def send_thread_interval():
    threading.Timer(interval=1.0,function=send_thread_interval).start()
    sendBraodcast()
    

def sendBraodcast():
    message = struct.pack("Ibh", 0xfeedbeef, 0x2,PORT)
    UDPServerSocket.sendto(message,("<broadcast>",13117))

# def run_game(ip,host):
#     print(ip,host)
#     # game_message = "Welcome to Keyboard Spamming Battle Royale.\n Group 1:\n ==\n "
#     # TCPServerSocket.sendto(game_message.encode(),(ip,host))
#     # print("send")


def start_game(number_of_players):
    game_message = "Welcome to Keyboard Spamming Battle Royale.\n Group 1:\n ==\n {0} ".format(Group1)
    print(game_message)
    
    # for i in Group1:
    #     game_thread = threading.Thread(target=run_game,args=i[1])
    #     game_thread.start()


class ClientThread(threading.Thread):

    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddress = clientAddress
        print ("New connection added: ", clientAddress)

    def run(self):
        group_name = self.csocket.recv(1024)
        PLAYERS.append(self.caddress)
        if len(Group1) == len(Group2):
            Group1.append(group_name.decode("utf-8"))
        elif len(Group1)>len(Group2):
            Group2.append(group_name.decode("utf-8"))
        

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
number_of_players =0

TCPServerSocket.settimeout(10.0)
try:
    while True:  
        TCPServerSocket.listen(1)
        clientsock, clientAddress = TCPServerSocket.accept()
        newthread = ClientThread(clientAddress, clientsock)
        number_of_players += 1
        newthread.start()
except socket.timeout as TimeOutException:
    start_game(number_of_players)

# while True:  
#     TCPServerSocket.listen(1)
#     clientsock, clientAddress = TCPServerSocket.accept()
#     newthread = ClientThread(clientAddress, clientsock)
#     number_of_players += 1
#     newthread.start()





        

