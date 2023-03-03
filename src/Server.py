# Base server code obtained from https://realpython.com/python-sockets/

import socket
import threading

import pymongo
import pickle
import FileSystem
from ComponentType import ComponentType

host = "127.0.0.1"
port = 8080
buffsize = 102400  # Received .txt files + header must be smaller than 10KB
users = None
db = None
client = None
filesystems = None
groups = None
close = False


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
    global close
    # Initialise the file system so that it's the same for all users
    signup_sys = FileSystem.FileSystem(client)
    while True:
        recv = conn.recv(1024)
        if not recv:
            break
        recv = pickle.loads(recv)
        print(f'Command received: {recv}')
        if recv == "login":
            recv_data = conn.recv(buffsize)
            print(f'Data received: {recv_data}')
            # loginCredentials is in the form of [username, hashedPassword]
            loggedIn = authenticate_user(pickle.loads(recv_data))
            send_data(conn, loggedIn)
            if not loggedIn:
                continue
            client_username = pickle.loads(recv_data)[0]
            fs = filesystems.find_one({"username": client_username})
            # print(f"fs is {fs}")
            if fs is None:
                sys = FileSystem.FileSystem(client)
                sys.make_current_user(client_username)
            else:
                sys = pickle.loads(fs["filesystem"])
            add_to_groups(sys)
            print(f"Logged in as {sys.user.name}, going to command server")
            # If the user is an admin, go to the admin command server
            if sys.user.name == "admin":
                command_server(conn=conn, sys=sys, admin=True)
            else:
                command_server(conn=conn, sys=sys, admin=False)
        elif recv == "signup":
            # Receive signup information from client and check that it's valid
            recv_data = conn.recv(buffsize)
            # signupCredentials is in the form of [username, hashedPassword]
            signupSuccess = create_user(pickle.loads(recv_data))
            conn.sendall(pickle.dumps(signupSuccess))
            signup_sys.create_user(pickle.loads(recv_data)[0])
        elif recv == "exit":
            conn.close()
            close = True
            break
        elif not recv:
            continue


def server():
    global users, db, client, filesystems, groups
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["sfsdatabase"]

    # Get the collection of users
    users = db["users"]
    filesystems = db["filesystems"]
    groups = db["groups"]
    # filesystems.delete_many({})
    # users.delete_many({})
    # groups.delete_many({})
    # print("Starting database")
    # cursor = filesystems.find({})
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
    while not close:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
        client_thread.join()
    server_socket.close()
    exit()


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


def save_system(sys):
    # Save the file system to the database
    if filesystems.find_one({"username": sys.user.name}) is not None:
        filesystems.delete_one({"username": sys.user.name})
    result = filesystems.insert_one({"username": sys.user.name, "filesystem": pickle.dumps(sys)})
    print("Saved system")


def create_group(group_name, usernames):
    global users, groups
    # check if group already exists
    if groups.find_one({"groupname": group_name}) is not None:
        return False
    # check if all users exist
    for user in usernames:
        if users.find_one({"username": user}) is None:
            return False
    # create group
    groups.insert_one({"groupname": group_name, "users": usernames})
    return True


def update_group(group_name, usernames):
    if groups.find_one({"groupname": group_name}) is None:
        return False
    groups.delete_one({"groupname": group_name})
    groups.insert_one({"groupname": group_name, "users": usernames})


def delete_group(group_name):
    if groups.find_one({"groupname": group_name}) is None:
        return False
    groups.delete_one({"groupname": group_name})
    return True


def add_to_groups(sys):
    # cursor = users.find({})
    # for item in cursor:
    #     print(item)
    cursor = groups.find({"users": sys.user.name})
    for item in cursor:
        sys.user.add_group(item["groupname"])


def command_server(conn, sys, admin=False):
    fullPrivilege = True
    actualUsername = sys.user.name
    while True:
        # Once login is successful, await commands (e.g change directory, add file, etc)
        # Commands arrive in the form of [command, parameters]
        recv_data = conn.recv(buffsize)
        data = pickle.loads(recv_data)
        print(f"Received in command server: {data}")
        # create a file
        if data[0] == "cr":
            if (fullPrivilege == True) or (admin == True):
                sys.create_component(str(data[1]), ComponentType.FILE)
                send_data(conn, "File created")
            else:
                send_data(conn, "Insufficient privileges")
        elif data[0] == "cd":
            if ".." in data[1]:
                result = sys.change_prev_directory()
                if result == True:
                    send_data(s=conn, data=sys.get_current_path())
                else:
                    send_data(s=conn, data="Error: Invalid path provided")
            elif "home\\" in data[1]:
                newuser = data[1].split('\\')[1]
                # if the user isn't changing to another user's directory
                if (newuser == sys.user.name) and (newuser == actualUsername):
                    result = sys.change_directory(str(data[1]))
                    if result == True:
                        send_data(s=conn, data=sys.get_current_path())
                    else:
                        send_data(s=conn, data="Error: Invalid path provided")
                else:
                    newfs = filesystems.find_one({"username": newuser})
                    newfs = pickle.loads(newfs["filesystem"])
                    inSameGroup = False
                    for grp in sys.user.groups:
                        if grp in newfs.user.groups:
                            inSameGroup = True
                    if inSameGroup:                
                        # if the user is changing back to his original directory    
                        if (newuser != sys.user.name) and (newuser == actualUsername):
                            save_system(sys)
                            sys = newfs
                            send_data(s=conn, data=sys.get_current_path())
                            fullPrivilege = True
                        # if the user is changing to another user's directory
                        else:
                            save_system(sys)
                            sys = newfs
                            send_data(s=conn, data=sys.get_current_path_lp())
                            fullPrivilege = False
                    else:
                        send_data(s=conn, data="Insufficient privileges - Not in same group")
            else:
                result = sys.change_directory(str(data[1]))
                if result == True:
                    send_data(s=conn, data=sys.get_current_path())
                else:
                    send_data(s=conn, data="Error: Invalid path provided")
        elif data[0] == "mk":
            if (fullPrivilege == True) or (admin == True):
                sys.create_component(str(data[1]), ComponentType.DIR)
                send_data(conn, "Directory created")
            else:
                send_data(conn, "Insufficient privileges")
        # remove a file
        elif data[0] == "rm":
            if (fullPrivilege == True) or (admin == True):
                sys.remove_component(str(data[1]))
                send_data(conn, f"{str(data[1])} deleted")
            else:
                send_data(conn, "Insufficient privileges")
        # read a file
        elif data[0] == "lg":
            save_system(sys)
            return
        elif data[0] == "rd":
            if (fullPrivilege == True) or (admin == True):
                file = sys.get_component(str(data[1])).read()
                send_data(conn, str(file))
            else:
                send_data(conn, "Insufficient privileges")
        elif data[0] == "wr":
            if (fullPrivilege == True) or (admin == True):
                sys.get_component(str(data[1][0])).write(data[1][1:])
                send_data(conn, "File updated")
            else:
                send_data(conn, "Insufficient privileges")
        elif data[0] == "rn":
            if (fullPrivilege == True) or (admin == True):
                sys.get_component(str(data[1][0])).rename(data[1][1])
                send_data(conn, f"File renamed to {str(data[1][1])}")
            else:
                send_data(conn, "Insufficient privileges")
        # list all files in the directory
        elif data[0] == "ls":
            if (fullPrivilege == True) or (admin == True):
                send_data(conn, sys.list_components())
            else:
                send_data(conn, sys.list_components_lp())
        elif data[0] == "shg":
            send_data(conn, sys.user.groups)
        elif data[0] == "pwd":
            if (fullPrivilege == True) or (admin == True):
                send_data(s=conn, data=sys.get_current_path())
            else:
                send_data(s=conn, data=sys.get_current_path_lp())
        # admin commands
        elif data[0] == "crg":
            if admin:
                send_data(conn, create_group(data[1][0], data[1][1:]))
            else:
                send_data(conn, "You are not an admin")
        elif data[0] == "dlg":
            if admin:
                send_data(conn, delete_group(data[1]))
            else:
                send_data(conn, "You are not an admin")
        elif data[0] == "upg":
            if admin:
                send_data(conn, update_group(data[1], data[1:]))
            else:
                send_data(conn, "You are not an admin")
        elif data[0] == "lsg":
            if admin:
                li = []
                cursor = groups.find({})
                for document in cursor:
                    li.append([document["groupname"], document["users"]])
                send_data(conn, li)
            else:
                send_data(conn, "You are not an admin")


if __name__ == '__main__':
    server()
