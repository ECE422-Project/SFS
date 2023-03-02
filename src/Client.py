# Basic client that allows users to log in, change directories, read/store text files and log out.
# User passwords are encrypted before transmission to the server

import socket
import pickle
import hashlib

host = "127.0.0.1"
port = 8080
buffsize = 102400  # Received .txt files + header must be smaller than 100KB
validCommands = ["lg", "ls", "cr", "rm", "rd", "wr", "rn"]


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.settimeout(None)
        main_menu(s)


def main_menu(s):
    print("-------Main Menu-------")
    print("1. Log In")
    print("2. Sign Up")
    print("3. Exit")
    choice = input("Enter choice: ")
    if choice == "1":
        login(s)
    elif choice == "2":
        signup(s)
    elif choice == "3":
        exit()
    else:
        print("Invalid choice")
        main_menu(s)


def login(s):
    try:
        s.send(pickle.dumps("login"))
    except:
        # recreate the socket and reconnect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(pickle.dumps("login"))
    while True:
        print("-------Login-------")
        username = input("Please enter username:")
        password = input("Please enter password:")
        hashedPassword = hashlib.sha256(password.encode('UTF-8'))

        loginCredentials = pickle.dumps([username, hashedPassword.hexdigest()])
        s.sendall(loginCredentials)

        loginCheck = s.recv(buffsize)

        loggedIn = pickle.loads(loginCheck)
        if loggedIn:
            print("Log in successful")
            command(s)
        else:
            while True:
                print("Invalid username or password")
                print("1. Re-try Log In")
                print("2. Exit to Main Menu")
                choice = input("Enter choice: ")
                if choice == "1":
                    login(s)
                elif choice == "2":
                    main_menu(s)
                else:
                    print("Invalid choice")
                    continue


def signup(s):
    try:
        s.send(pickle.dumps("signup"))
    except:
        # recreate the socket and reconnect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(pickle.dumps("signup"))
    while True:
        print("-------Sign Up-------")
        username = input("Please enter username:")
        password = input("Please enter password:")
        hashedPassword = hashlib.sha256(password.encode('UTF-8'))

        signupCredentials = pickle.dumps([username, hashedPassword.hexdigest()])
        s.send(signupCredentials)

        signupCheck = s.recv(buffsize)
        signedUp = pickle.loads(signupCheck)
        if signedUp:
            print("Sign up successful")
            login(s)
        else:
            while True:
                print("Username already exists")
                print("1. Re-try Signup")
                print("2. Exit to Main Menu")
                choice = input("Enter choice: ")
                if choice == "1":
                    signup(s)
                elif choice == "2":
                    main_menu(s)
                else:
                    print("Invalid choice")
                    continue


def command(s):
    while True:
        userInput = input("Enter commands:")
        if len(userInput.split()) == 1:
            if userInput == "lg":
                s.send(pickle.dumps([userInput]))
                main_menu(s)
            elif userInput == "ls":
                s.send(pickle.dumps([userInput]))
                print(*pickle.loads(s.recv(buffsize)))
            elif userInput == "pwd":
                s.send(pickle.dumps([userInput]))
                response = pickle.loads(s.recv(buffsize))
                print(*response)
            elif userInput == "..":
                s.send(pickle.dumps([userInput]))
                print(pickle.loads(s.recv(buffsize)))
        else:
            userInput = userInput.split()
            if userInput[0] == "cr":
                s.send(pickle.dumps([userInput[0], *userInput[1:]]))
                print(pickle.loads(s.recv(buffsize)))
            elif userInput[0] == "mk":
                s.send(pickle.dumps([userInput[0], *userInput[1:]]))
                print(pickle.loads(s.recv(buffsize)))
            elif userInput[0] == "cd":
                s.send(pickle.dumps([userInput[0], *userInput[1:]]))
                print("Now in directory: ")
                print(*pickle.loads(s.recv(buffsize)))
            elif userInput[0] == "rm":
                s.send(pickle.dumps([userInput[0], *userInput[1:]]))
                print(pickle.loads(s.recv(buffsize)))
            elif userInput[0] == "rd":
                s.send(pickle.dumps([userInput[0], *userInput[1:]]))
                print(pickle.loads(s.recv(buffsize)))
            elif userInput[0] == "wr":
                s.send(pickle.dumps([userInput[0], userInput[1:]]))
            elif (len(userInput.split()) > 3) and (userInput.split()[:2] in validCommands) and (userInput.split()[2] == " ") and (
                    not userInput[3:].isspace()):
                s.send(pickle.dumps([userInput[:2], userInput[3:]]))
            else:
                print("Invalid Input")


if __name__ == '__main__':
    main()
