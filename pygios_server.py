[cstanley@Minion1 scripts]$ cat pygios_server.py
#!/usr/bin/env python

import socket
import sys
import time
import datetime
from thread import *
global DEBUG
global connected

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
DEBUG = True
connected = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n> ') #send only takes string

    #infinite loop so that function do not terminate and thread does not end.
    while 1:

        #Receiving from client
        data = conn.recv(1024).rstrip()

        if "6a736f6e" in data:
            print "JSON Data String Detected..."
            reply = "JSON Received: " + data
            if DEBUG:
                print "[" + datetime.datetime.now().strftime("%m/%d/%y %H:%M") + "][DEBUG] Message Received: " + data
        elif data == "exit":
            connected = False
            if DEBUG:
                print "[" + datetime.datetime.now().strftime("%m/%d/%y %H:%M") + "][DEBUG] Client " + addr[0] + ":" + str(addr[1]) + " disconnected."
            break
        elif data == "help":
            reply = "This is the help menu\n> "
            if DEBUG:
                print "[" + datetime.datetime.now().strftime("%m/%d/%y %H:%M") + "][DEBUG] Message Received: " + data
        elif DEBUG:
            reply = "[SERVER DEBUG] Message Received: " + data + "\n> "
            print "[" + datetime.datetime.now().strftime("%m/%d/%y %H:%M") + "][DEBUG] Message Received: " + data

        if not data:
            if DEBUG:
                print "[" + datetime.datetime.now().strftime("%m/%d/%y %H:%M") + "][DEBUG] Client " + addr[0] + ":" + str(addr[1]) + " disconnected."
            break

        conn.sendall(reply)

    #came out of loop

#now keep talking with the client
while connected:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
