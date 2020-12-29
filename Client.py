import socket
import struct

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
  host  = addr[0]
  values_message = struct.unpack("Ibh",message)
  if hex(values_message[0]) == '0xfeedbeef' and hex(values_message[1]) == '0x2' :
    break

TCPClientSocket.connect((host, values_message[2]))
print('Received offer from {0}, attempting to connect...'.format(addr[0]))
TCPClientSocket.sendto('game_over'.encode(),addr)