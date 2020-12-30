import socket
import struct
import time




#--------------------waiting to connect------------stage 1

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP

# Enable port reusage so we will be able to run multiple clients and servers on single (host, port). 
# Do not use socket.SO_REUSEADDR except you using linux(kernel<3.9): goto https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ for more information.
# For linux hosts all sockets that want to share the same address and port combination must belong to processes that share the same effective user ID!
# So, on linux(kernel>=3.9) you have to run multiple servers and clients under one user to share the same (host, port).
# Thanks to @stevenreddie

client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("0.0.0.0", 13117))
print("Client started, listening for offer requests... ")
#--------------------succefully connected to server------------stage 2
print(" this is the client ip  :    "+str(socket.gethostname())  )
flag=True
adrr=None
data=None
while flag:
    data, adrr= client.recvfrom(1024)
    if( len(data)==8):
        data2 = struct.unpack("Ibh",data )
        print("this is data  "+str(data2))
        port=data2[2]
        if(int(data2[0])==0xfeedbeef and int(data2[1]==0x2) and port==2028 ):
            flag=False
            print(" going on to the next stage-playing game!")
            print(" this is good meassge received message: %s"%data2[0])

  
#--------------------connect to tcp and playing------------stage 3


BUFFER_SIZE = 20 
host = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if(adrr!=None):
    s.connect((adrr[0], port))
while True:
    s.sendall(str.encode('this team client 1\n'))
    data=(s.recv(1024))
    if data:
        print(data)
        print("Welcome to Keyboard Spamming Battle Royale\n Group 1:")
        x=time.time()
        char=""
        print("press as many keys ass you can")
        while time.time()< x+10:   
            char+=input()
        print(char)   
        print("The number of keys you pressed "+str(len(char)))
s.close()