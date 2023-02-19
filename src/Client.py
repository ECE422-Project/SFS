#Basic client that allows users to log in, change directories, read/store text files and log out.
#User passwords are encrypted before transmission to the server

import socket
import pickle
import hashlib

host = "127.0.0.1"  
port = 8080
buffsize = 102400 #Received .txt files + header must be smaller than 100KB
validCommands = ["lg", "ls", "cr", "rm", "rd", "wr", "rn"]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    loggedIn = False
    while True:
        #Have the user log in
        while(loggedIn == False):
            username = input("Please enter username:")
            password = input("Please enter password:")
            hashedPassword = hashlib.sha256(password.encode('UTF-8'))

            loginCredentials = pickle.dumps([username, hashedPassword.hexdigest()])
            s.send(loginCredentials)

            loginCheck = s.recv(1024)
            loggedIn = pickle.loads(loginCheck)
            if loggedIn:
                print("Log in successful")
            else:
                print("Invalid username or password")

        #Once user is logged in, check the input and send to server in the form of [command, parameters]
        #Valid inputs must start with a 2-letter command followed by a space and then its parameters
        userInput = input("Enter commands:")
        if userInput == "lg":
            loggedIn = False
        elif userInput == "ls":
            s.send(pickle.dumps(["ls", " "]))
        elif (len(userInput) > 3) and (userInput[:2] in validCommands) and (userInput[2] == " ") and (not userInput[3:].isspace()):
            s.send(pickle.dumps([userInput[:2], userInput[3:]]))
        else:
            print("Invalid Input")
