import socket
import struct
import msvcrt
import keyboard

def send_group_name():
  group_name = "gogogo\n"
  TCPClientSocket.sendto(group_name.encode('UTF-8','strict'),addr)

# sends a message to server via the open TCP connection for every key press.
def start_game():
  print("instart_game")
  while True:
    key = keyboard.read_key()
    if key:
        send_key = bytes(key, 'utf-8')
        TCPClientSocket.sendall(send_key)
        print(key)

#sends the group name back to server via "send_group_name()"
#wait for game start message to return and then starts playing 
def TCPconnect_server(port,source):
  print(source[0],port)
  TCPClientSocket.connect((source[0], port))
  print('Received offer from {0}, attempting to connect...'.format(source[0]))
  send_group_name()
  while True:
    TCPClientSocket.settimeout(0.2)
    try:
      message,addr = TCPClientSocket.recvfrom(1024)
      if not message is None:
        print(message.decode('UTF-8','strict'))
        start_game()
    except:
      continue
    

buffer_size = 1024
PORT = 13117 #hard coded for hackathon porpous.

#client has both TCP and UDP sockets
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPClientSocket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)

print("Client started, listening for offer requests...")
UDPClientSocket.bind(('',PORT)) #bind all incoming packets to hackathon port
values_message = None
addr = None
while True:
    TCPClientSocket.settimeout(0.2) #set time to avoid "busy wait"
    message,addr = UDPClientSocket.recvfrom(buffer_size)
    #translate and validate message
    values_message = struct.unpack("Ibh",message) 
    if (not message is None) and (hex(values_message[0]) == '0xfeedbeef') and (hex(values_message[1]) == '0x2') :
      break

UDPClientSocket.close() #no need to keep listening to UDP port while game is in play
TCPconnect_server(port=2027,source=addr)


