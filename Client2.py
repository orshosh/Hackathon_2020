import socket
import struct
import msvcrt
import keyboard

def send_group_name():
  group_name = "gogogo\n"
  TCPClientSocket.sendto(group_name.encode('UTF-8','strict'),addr)

def start_game():
  print("instart_game")
  while True:
    key = keyboard.read_key()
    if key:
        send_key = bytes(key, 'utf-8')
        TCPClientSocket.sendall(send_key)
        print(key)


def TCPconnect_server(port,source):
  print(source[0],port)
  TCPClientSocket.connect((source[0], port))
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
UDPClientSocket.bind(('',PORT))
values_message = None
addr = None
while True:
  message,addr = UDPClientSocket.recvfrom(1024)
  values_message = struct.unpack("Ibh",message)
  if (not message is None) and (hex(values_message[0]) == '0xfeedbeef') and (hex(values_message[1]) == '0x2') :
    
    break

UDPClientSocket.close()
# TCPconnect_server(port=values_message[2],source=addr)
TCPconnect_server(port=2027,source=addr)


