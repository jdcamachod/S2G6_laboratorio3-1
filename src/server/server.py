﻿import socket
import tqdm
import os

# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 9898
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# create the server socket
# TCP socket
s = socket.socket()

# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))
filename = "Media1.mp4"
filesize = os.path.getsize(filename)
# enabling our server to accept connections
# 25 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(25)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# accept connection if there is any
client_socket, address = s.accept() 
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")

client_socket.recv()
# receive the file infos
# receive using client socket, not server socket
client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
#received = client_socket.recv(BUFFER_SIZE).decode()
#filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
#filename = os.path.basename(filename)
# convert to integer
#filesize = int(filesize)

# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    for _ in progress:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in 
        # busy networks
        client_socket.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
# start receiving the file from the socket
# and writing to the file stream

# close the client socket
client_socket.close()
# close the server socket
s.close()