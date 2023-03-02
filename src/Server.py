# Base server code obtained from https://realpython.com/python-sockets/

import socket
import threading

import pymongo
import selectors
import types
import pickle
import FileSystem
from src.ComponentType import ComponentType

host = "127.0.0.1"
port = 8080
buffsize = 102400  # Received .txt files + header must be smaller than 10KB
users = None
db = None
client = None

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


def handle_client(conn, addr):
    # Initialise the file system so that it's the same for all users
    sys = FileSystem.FileSystem(client)
    while True:
        recv = conn.recv(1024)
        if not recv:
            break
        recv = pickle.loads(recv)
        print(f'Received: {recv}')
        if recv == "login":
            recv_data = conn.recv(buffsize)
            # loginCredentials is in the form of [username, hashedPassword]
            loggedIn = authenticate_user(pickle.loads(recv_data))
            send_data(conn, loggedIn)
            if not loggedIn:
                continue
            sys.make_current_user(pickle.loads(recv_data)[0])
            print(f"Logged in as {sys.user.name}, going to command server")
            command_server(conn=conn, sys=sys)
        elif recv == "signup":
            # Receive signup information from client and check that it's valid
            recv_data = conn.recv(buffsize)
            # signupCredentials is in the form of [username, hashedPassword]
            signupSuccess = create_user(pickle.loads(recv_data))
            conn.sendall(pickle.dumps(signupSuccess))
            sys.create_user(pickle.loads(recv_data)[0])
        elif not recv:
            continue


def server():
    global users, db, client
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["sfsdatabase"]

    # Get the collection of users
    users = db["users"]
    # print("Starting database")
    # cursor = users.find({})
    # for item in cursor:
    #     print(item)
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.settimeout(None)
    # Start listening for incoming connections
    server_socket.listen()
    print(f"Server listening on {host}:{port}")

    # Handle incoming connections
    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()


def send_data(s, data):
    try:
        s.sendall(pickle.dumps(data))
        print("Sent: ", data)
        return
    except:
        # recreate the socket and reconnect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendall(pickle.dumps(data))
        print("Sent: ", data)
        return



def command_server(conn, sys):
    while True:
        # Once login is successful, await commands (e.g change directory, add file, etc)
        # Commands arrive in the form of [command, parameters]
        recv_data = conn.recv(buffsize)
        data = pickle.loads(recv_data)
        print(f"Received: {data}")
        # create a file
        if data[0] == "cr":
            sys.create_component(str(data[1]), ComponentType.FILE)
            send_data(conn, "File created")
        elif data[0] == "cd":
            if ".." in data[1]:
                sys.change_prev_directory()
                send_data(s=conn, data=sys.get_current_path())
            else:
                sys.change_directory(str(data[1]))
                send_data(s=conn, data=sys.get_current_path())
        elif data[0] == "mk":
            sys.create_component(str(data[1]), ComponentType.DIR)
            send_data(conn, "Directory created")
        # remove a file
        elif data[0] == "rm":
            # removeFile(data[1])
            pass
        # read a file
        elif data[0] == "rd":
            file = sys.get_component(str(data[1])).read()
            send_data(conn, str(file))
            pass
        elif data[0] == "wr":
            sys.get_component(str(data[1][0])).write(data[1][1:])
            pass
        elif data[0] == "rn":
            # renameFile(data[1])
            pass
        # list all files in the directory
        elif data[0] == "ls":
            send_data(conn, sys.list_components())
        elif data[0] == "pwd":
            send_data(s=conn, data=sys.get_current_path())


if __name__ == '__main__':
    server()
