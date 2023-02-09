#Client side

import socket

#Obtain the name of the client (magnus-linux)
host_name = socket.gethostname()
port_number = 5000

#Get socket instance
client_socket = socket.socket()

#Try to connect to a server
client_socket.connect((host_name, port_number))
print("Connected to server!")

#User can write a message
message = input("Write a message to server: ")

while True:
    #Send a message
    client_socket.send(message.encode())

    #Close connection if requested
    if (message.lower() == "close"):
        print("Closing the connection...")
        break
    else:
        #Wait to receive a response
        response_data = client_socket.recv(1024).decode()
        print("Response from server:", response_data)

        #User can write new message
        message = input("Write message to server: ")

#Close connection
client_socket.close()










#Create a socket object to send and receive data
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# #Make the socket connect to a server
# client_socket.connect((socket.gethostname(), 1234))

# #Receive a message that is sent to us
# message = ""

# while True:
#     msg = client_socket.recv(8)             #Receive 32 bytes at a time
#     if(len(msg) <= 0):
#         break
#     else:
#         message += msg.decode("utf-8)")     #Add received bytes to message

# print(message)