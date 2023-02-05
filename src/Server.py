#Base server code obtained from https://realpython.com/python-sockets/

import sys
import os
import socket
import selectors
import types

host = "127.0.0.1"  
port = 8080
buffsize = 10240 #Received .txt files + header must be smaller than 10MB

sel = selectors.DefaultSelector()

def accept(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def read_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(buffsize)  
        if recv_data:
            ServerConn(key, sock, data, mask) #Assuming we follow the provided class diagram, feel free to change
        else:
            #If no return, client must have disconnected. Close the connection
            sel.unregister(sock)
            sock.close()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept(key.fileobj)
            else:
                read_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
