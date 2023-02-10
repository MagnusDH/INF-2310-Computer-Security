import socket
import time
from Crypto.Cipher import AES


server_public_key = "53rv3r Pu8l1c k3y"
server_private_key = "53rv3r pr1v4t3 k3y"
client_public_key = ""

#Obtain the name of the host (magnus-linux)
server_host_name = socket.gethostname()
port_number = 5000

#Get socket instance
server_socket = socket.socket()

#Bind host address and port numer together
server_socket.bind((server_host_name, port_number))

#Listen for 5 connections
print("Waiting for clients to connect...\n")
server_socket.listen(5)

#When connection request is recieved, connect to client
try:
    connection, address = server_socket.accept()
    print("Got connection request. Establishing connection with: ", address, "\n")
    message = "request accepted"
    connection.send(message.encode())
    print("CONNECTION ESTABLISHED!\n")
except:
    print("Could not establish connection with client...")

#Receive client_public_key
print("Waiting to receive public key...\n")
client_response = connection.recv(1024).decode()
print("Got client pulic key: ", client_response, "\n")
client_public_key = client_response

#send server_public_key
print("Sending server_public_key...\n")
message = server_public_key
connection.send(message.encode())

#Receive and send data
while True:
    #Receive data
    print("Waiting for client to respond...\n")
    receive_data = connection.recv(1024).decode()
    print("Response from client: ", receive_data, "\n")
    
    if receive_data.lower() == "close":
        print("Closing connection...")
        break

    else:
        #Send data from server
        response = input("Response to client: ")
        connection.send(response.encode())

#Close the connection
connection.close()




# #Create a socket object to send and receive data
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# #Bind the socket in order to receive and send data
# server_socket.bind((server_host_name, 1234))    #bind((IP-address, port number))

# #Listen for connections and establish connection if recieved 
# server_socket.listen(5)
# while True:
#     client_socket, address = server_socket.accept()                                  #Accept an incomming connection
#     print("Connection from", address, "has been established!")
    
#     client_socket.send(bytes("This is a message sent from the server!\n", "utf-8"))    #Send information to the client socket
#     client_socket.close()