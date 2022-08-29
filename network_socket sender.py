# Exchange data between two endpoints

# Program bind to specific address and port and listens for incoming TCP traffic

from multiprocessing import connection
import socket

SRV_ADDR = input("Type the server IP address: ")
SRV_PORT = int(input("Type the server port: "))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SRV_ADDR, SRV_PORT))
print("Connection Established")

message = input("Message to send: ")
s.sendall(message.encode())
s.close()
