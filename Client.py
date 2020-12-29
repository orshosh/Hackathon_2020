import socket
import struct

PORT = 13117
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPClientSocket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)

print("Client started, listening for offer requests...")
UDPClientSocket.bind(("",PORT))
values_message = None
while True:
  message,addr = UDPClientSocket.recvfrom(1024)
  values_message = struct.unpack("Ibh",message)
  print(addr)
  if hex(values_message[0]) == '0xfeedbeef' and hex(values_message[1]) == '0x2' :
    break

print('Received offer from 172.1.0.4, attempting to connect...')

  
  
  
  

  

# client.connect((SERVER, PORT))
# client.sendall(bytes("This is from Client",'UTF-8'))
# while True:
  
#   print("From Server :" ,in_data.decode())
#   out_data = input()
#   client.sendall(bytes(out_data,'UTF-8'))
#   if out_data=='bye':
#       break
# client.close()