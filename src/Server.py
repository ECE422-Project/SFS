#Base server code obtained from https://realpython.com/python-sockets/

import sys
import os
import socket
import selectors
import types
import pickle

host = "127.0.0.1"  
port = 8080
buffsize = 102400 #Received .txt files + header must be smaller than 10KB

def checkCredentials(loginCredentials):
    #Returns True if user exists in the system and that the password matches, False otherwise
    return True    

def createFile(fileName):
    #Creates a file with the specified filename in the current directory
    return True 

def removeFile(fileName):
    #Remove a file with the specified filename in the current directory
    return True 

def readFile(fileName):
    #Reads a file with the specified filename in the current directory
    return True 

def writeFile(fileName):
    #Writes to a file with the specified filename in the current directory
    return True

def renameFile(fileName):
    #Renames a file with the specified filename in the current directory
    return True 

def listDirectory():
    #Returns a list of all filenames in the current directory
    return True 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(3)
    conn, addr = s.accept()
    with conn:
        while True:
            loggedIn = False
            while not loggedIn:
                #Receive login information from client and check that it's valid
                recv_data = conn.recv(buffsize)
                if not recv_data:
                    break
                #loginCredentials is in the form of [username, hashedPassword]
                loginCredentials = pickle.loads(recv_data)
                loggedIn = checkCredentials(loginCredentials)
                conn.sendall(pickle.dumps(loggedIn))

            while True:
                #Once login is successful, await commands (e.g change directory, add file, etc)
                #Commands arrive in the form of [command, parameters]
                recv_data = conn.recv(buffsize)
                data = pickle.loads(recv_data)
                if (data[0] == "cr"):
                    createFile(data[1])
                elif (data[0] == "rm"):
                    removeFile(data[1])
                elif (data[0] == "rd"):
                    file = readFile(data[1])
                    conn.sendall(file)
                elif (data[0] == "wr"):
                    writeFile(data[1])
                elif (data[0] == "rn"):
                    renameFile(data[1])
                elif (data[0] == "ls"):
                    directoryList = listDirectory()
                    conn.sendall(directoryList)