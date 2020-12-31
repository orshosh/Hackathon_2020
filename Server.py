import socket
import time
import threading
import struct
import sys
import keyword
import executor

Group1 = []
Group2 = []
PLAYERS = {}
Group1_counter = 0
Group2_counter = 0
buffer_size = 1024  
kill_thread = True



#send a broadcast every set time.
def send_thread_interval(port,UDPServerSocket):
    global kill_thread
    if kill_thread:
        threading.Timer(interval=1.0,function=send_thread_interval,args=(port,UDPServerSocket)).start()
        sendBraodcast(port,UDPServerSocket)

# build the message and sent to all available using UDP socket boradcast     
def sendBraodcast(port,UDPServerSocket):
    print("send")
    message = struct.pack("Ibh", 0xfeedbeef, 0x2,port)
    UDPServerSocket.sendto(message,("<broadcast>",13117))

def get_winner():
    if Group1_counter > Group2_counter:
        return Group1,"Group 1"
    else:
        return Group2,"Group 2"

#welcome msg
def write_msg():
    game_message = "Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n"
    for player in Group1:
        game_message += player
    game_message += "\nGroup 2:\n==\n"
    if len(Group2)>0:
        for player in Group2:
            game_message += player
    game_message += "\nStart pressing keys on your keyboard as fast as you can!!"
    return game_message


#Function recive a group name and count, updates the relevant score
def insret_count(count,client_name):
    if client_name in Group1:
        global Group1_counter
        Group1_counter += count
    else:
        global Group2_counter
        Group2_counter += count
    

 # Once the server finished collecting all players, initialize a game thread for each player
 # by calling  the "run_game()" method.
 # after all players returnd, finish the game.   
def start_game():
    for key in PLAYERS:
        game_thread = threading.Thread(target=run_game,args=(PLAYERS[key][0],PLAYERS[key][1],key))
        game_thread.start()
    game_thread.join()
    finish_game()


 #Function send the game message to the client via the relevant socket
 # server recives packets for 10 seconds, then updates the count for each group via "insert_count()"
def run_game(client_socket,client_address,client_name):
    game_message = write_msg()
    client_socket.sendto(game_message.encode('UTF-8','strict'),client_address)
    start_time = time.time()
    count_char = 0
    while time.time() - start_time < 10:
        try:
            char = client_socket.recv(buffer_size)
            if not char is None:
                count_char +=1
        except:
            pass
    insret_count(count_char,client_name)
       
#when game is finished, the function creates the final message and sends it to each player
def finish_game():
    winner_list, winner = get_winner()
    message = final_msg(winner_list,winner)
    print(message)
    for key in PLAYERS:
        client_socket = PLAYERS[key][0]
        client_address = PLAYERS[key][1]
        print("Game over, sending out offer requests...")
        client_socket.close()

# modular funtion to build final message according to the winner
def final_msg(winner_list, winner):
    global Group1_counter
    global Group2_counter
    final_message = "GAME OVER!\nGroup 1 typed in "
    final_message += str(Group1_counter)
    final_message += "characters.Group 2 typed in "
    final_message += str(Group2_counter)
    final_message += " characters.\n"
    final_message += winner
    final_message += " wins!\n\nCongratulations to the winners:\n\n==\n"
    for group in winner_list:
        final_message += group
    return final_message 


##the server creates a thread for each client it is communicating with
#this class makes holds all clientTreads methods
class ClientThread(threading.Thread):
    #each client has a unique address and socket to communicate with
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddress = clientAddress
        print ("New connection added: ", clientAddress)

    def run(self):
        group_name = self.csocket.recv(1024)
        g_name_code = group_name.decode('UTF-8','strict')
        PLAYERS[g_name_code] = (self.csocket,self.caddress)
        if len(Group1) == len(Group2):
            Group1.append(g_name_code)
        elif len(Group1)>len(Group2):
            Group2.append(g_name_code)
        
def main_server():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname) #ip of local machine running the code
    PORT = 2027
    #creating needed sockets for server
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    TCPServerSocket.bind(('', PORT))
    TCPServerSocket.listen(1)

    print("Server started,listening on IP address",local_ip)
    UDPServerSocket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    send_thread_interval(PORT,UDPServerSocket)
    # broadcast_thread = threading.Thread(target=send_thread_interval)
    # broadcast_thread.start()

    tmp_timp = time.time()
    while len(PLAYERS) == 0: #wait for at least one player to join game.
        while time.time() - tmp_timp < 10:  #when 10 seconds are finished , the game will start
            try:
                TCPServerSocket.settimeout(0.5)
                clientsock, clientAddress = TCPServerSocket.accept()
                newthread = ClientThread(clientAddress, clientsock)#new thread foe each client connected
                newthread.start()
            except:
                continue
    global kill_thread
    kill_thread = False
    start_game()

if __name__ == "__main__":
    # execute only if run as a script
    main_server()



        

