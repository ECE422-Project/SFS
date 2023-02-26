# Base server code obtained from https://realpython.com/python-sockets/

import sys
import os
import socket
import threading

import pymongo
import selectors
import types
import pickle
import FileSystem

host = "127.0.0.1"
port = 8080
buffsize = 102400  # Received .txt files + header must be smaller than 10KB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["sfsdatabase"]

# Get the collection of users
users = db["users"]


# Function to create a new user
def create_user(signup_credentials):
    if not authenticate_user(signup_credentials):
        print("Creating user")
        user = {"username": signup_credentials[0], "password": signup_credentials[1]}
        result = users.insert_one(user)
        # result.inserted_id
        return True
    else:
        return False


# Function to authenticate a user
def authenticate_user(login_credentials):
    user = users.find_one({"username": login_credentials[0], "password": login_credentials[1]})
    if user is not None:
        return True
    else:
        return False


def createFile(fileName):
    # Creates a file with the specified filename in the current directory

    return True


def removeFile(fileName):
    # Remove a file with the specified filename in the current directory
    return True


def readFile(fileName):
    # Reads a file with the specified filename in the current directory
    return True


def writeFile(fileName):
    # Writes to a file with the specified filename in the current directory
    return True


def renameFile(fileName):
    # Renames a file with the specified filename in the current directory
    return True


def listDirectory():
    # Returns a list of all filenames in the current directory
    return True


def handle_client(conn, addr):
    while True:
        recv = conn.recv(1024)
        print(f"Received: {recv}")
        if not recv:
            break
        recv = pickle.loads(recv)
        print(f'Received: {recv}')
        if recv == "login":
            recv_data = conn.recv(buffsize)
            # loginCredentials is in the form of [username, hashedPassword]
            loggedIn = authenticate_user(pickle.loads(recv_data))
            conn.sendall(pickle.dumps(loggedIn))
            command_server(conn, addr)
        elif recv == "signup":
            # Receive signup information from client and check that it's valid
            recv_data = conn.recv(buffsize)
            # signupCredentials is in the form of [username, hashedPassword]
            signupSuccess = create_user(pickle.loads(recv_data))
            conn.sendall(pickle.dumps(signupSuccess))
        elif not recv:
            break


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    # Start listening for incoming connections
    server_socket.listen()

    print(f"Server listening on {host}:{port}")

    # Handle incoming connections
    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()


def command_server(conn, addr):
    while True:
        # Once login is successful, await commands (e.g change directory, add file, etc)
        # Commands arrive in the form of [command, parameters]
        sys = FileSystem.FileSystem()

        recv_data = conn.recv(buffsize)
        data = pickle.loads(recv_data)
        # create a file
        if data[0] == "cr":
            sys.create_component(data[1])
        # remove a file
        elif data[0] == "rm":
            removeFile(data[1])
        # read a file
        elif data[0] == "rd":
            file = readFile(data[1])
            conn.sendall(file)
        elif data[0] == "wr":
            writeFile(data[1])
        elif data[0] == "rn":
            renameFile(data[1])
        # list all files in the directory
        elif data[0] == "ls":
            sys.list_components()
            directoryList = listDirectory()
            conn.sendall(directoryList)


if __name__ == '__main__':
    server()
