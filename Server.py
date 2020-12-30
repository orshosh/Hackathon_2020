import socket
import time
import threading
import struct
import sys
import keyword

Group1 = []
Group2 = []
PLAYERS = {}
Group1_counter = 0
Group2_counter = 0


def send_thread_interval():
    threading.Timer(interval=1.0,function=send_thread_interval).start()
    sendBraodcast()
    

def sendBraodcast():
    message = struct.pack("Ibh", 0xfeedbeef, 0x2,PORT)
    UDPServerSocket.sendto(message,("<broadcast>",13117))

def get_winner():
    if Group1_counter > Group2_counter:
        return Group1
    else:
        return Group2

def final_game():
    winner = get_winner()
    final_message = "GAME OVER!\nGroup 1 typed in"
    final_message += Group1_counter
    final_message += "characters.Group 2 typed in"
    final_message += Group2_counter
    final_message += "characters.\n"
    final_message += winner
    final_message += "wins!\n\nCongratulations to the winners:\n\n==\n"
    for group in winner:
        final_message += group

def write_msg():
    game_message = "Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n"
    for player in Group1:
        game_message += player
    game_message += "\nGroup 2:\n==\n"
    for player in Group2:
        game_message += player
    game_message += "\nStart pressing keys on your keyboard as fast as you can!!"
    return game_message

def run_game(client_socket,client_address):
    game_message = write_msg()
    client_socket.sendto(game_message.encode('UTF-8','strict'),client_address)
    start_time = time.time()
    count_char = 0
    while time.time() - start_time < 10:
        try:
            char = client_socket.recv(1024)
            if not char is None:
                count_char +=1
                print(count_char)
        except:
            pass
    return count_char
    
    
def start_game():
    for key in PLAYERS:
        # game_thread = threading.Thread(target = run_game,args=PLAYERS[key])
        game_thread = exextutor.submit(run_game,PLAYERS[key])
        counter = game_thread.result()
        if key in Group1:
            Group1_counter += counter
        else:
            Group2_counter += counter



class ClientThread(threading.Thread):

    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddress = clientAddress
        print ("New connection added: ", clientAddress)

    def run(self):
        group_name = self.csocket.recv(1024)
        PLAYERS[group_name] = (self.csocket,self.caddress)
        if len(Group1) == len(Group2):
            Group1.append(group_name.decode('UTF-8','strict'))
        elif len(Group1)>len(Group2):
            Group2.append(group_name.decode('UTF-8','strict'))
        

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
PORT = 2027
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPServerSocket.bind(('', PORT))

print("Server started,listening on IP address",local_ip)
UDPServerSocket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
broadcast_thread = threading.Thread(target=send_thread_interval)
broadcast_thread.start()

TCPServerSocket.settimeout(10.0)
try:
    while True:  
        TCPServerSocket.listen(1)
        clientsock, clientAddress = TCPServerSocket.accept()
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()
except socket.timeout as TimeOutException:
    UDPServerSocket.close()
    start_game()




        

