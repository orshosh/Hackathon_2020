import socket
import struct
import sys



def send_group_name():
  group_name = "slow-start\n"
  TCPClientSocket.sendto(group_name.encode('UTF-8','strict'),addr)

def start_game():
  while True:
    print("instart_game")
    # tty.setcbreak(sys.stdin.fileno())
    char=sys.stdin.read(1)
    TCPClientSocket.sendto(char.encode(('UTF-8','strict'),addr))
    flag_to_stop,adress = TCPClientSocket.recvfrom(1024)
    if flag_to_stop.decode('UTF-8','strict') == False:
      break

def TCPconnect_server(port,source):
  TCPClientSocket.connect((source[0], values_message[2]))
  print('Received offer from {0}, attempting to connect...'.format(source[0]))
  send_group_name()
  while True:
    message,addr = TCPClientSocket.recvfrom(1024)
    try:
      if not message is None:
        print(message.decode('UTF-8','strict'))
        start_game()
    except:
      continue



PORT = 13117
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPClientSocket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)

print("Client started, listening for offer requests...")
UDPClientSocket.bind(("",PORT))
values_message = None
addr = None
while True:
  message,addr = UDPClientSocket.recvfrom(1024)
  try:
    values_message = struct.unpack("Ibh",message)
    if (not message is None) and (hex(values_message[0]) == '0xfeedbeef') and (hex(values_message[1]) == '0x2') :
      break
  except:
      continue

UDPClientSocket.close()
TCPconnect_server(port=values_message[2],source=addr)
