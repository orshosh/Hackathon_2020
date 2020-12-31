import socket
import struct
import msvcrt
import keyboard

buffer_size = 1024

def send_group_name(socket,source):
  group_name = "startSlow\n"
  socket.sendto(group_name.encode('UTF-8','strict'),source)

def finish_game(socket):
  print("Server disconnected, listening for offer requests...")
  socket.close()
  main_client()

# sends a message to server via the open TCP connection for every key press.
def start_game(socket, loop_stop):
  print("start typing:")
  while loop_stop:
    key = keyboard.read_key()
    if key:
        send_key = bytes(key, 'utf-8')
        socket.sendall(send_key)
        print(key)
        try:
          message,addr = socket.recvfrom(buffer_size)
          if not message is None:
            print(message.decode('UTF-8','strict'))
            loop_stop = False
        except:
          pass 
  return True     


#sends the group name back to server via "send_group_name()"
#wait for game start message to return and then starts playing 
def TCPconnect_server(port,source,socket):
  socket.connect((source[0], port))
  print('Received offer from {0}, attempting to connect...'.format(source[0]))
  send_group_name(socket,source)
  loop_status = True
  while loop_status:
    socket.settimeout(0.2)
    try:
      message,addr = socket.recvfrom(buffer_size)
      if not message is None:
        print(message.decode('UTF-8','strict'))
        finish_status = start_game(socket,True)
        if finish_status:
          loop_status = False
    except:
      continue
  finish_game(socket)

    
def main_client():
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
  TCPconnect_server(port=2027,source=addr,socket=TCPClientSocket)


if __name__ == "__main__":
    # execute only if run as a script
    main_client()