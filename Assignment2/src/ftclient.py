import socket
import time

client_public_key = "cl13nt pu8l1c k3y"
client_private_key = "cl13nt pr1v4t3 k3y"
server_public_key = ""

#Obtain the name of the client (magnus-linux)
host_name = socket.gethostname()
port_number = 5000

#Get socket instance
client_socket = socket.socket()

#Try to connect to a server
print("Sending connection request to server: ", host_name, "\n")
try:
    client_socket.connect((host_name, port_number))
    server_response = client_socket.recv(1024).decode()
    if(server_response.lower() == "request accepted"):
        print("Server accepted connection request!\n")
        print("CONNECTION ESTABLISHED\n")
    else:
        print("Server declined request...\n")
except:
    print("Could not connect to server...\n")
    #Close connection
    client_socket.close()

#send client_public_key to server
print("Sending public key...\n")
message = client_public_key
client_socket.send(message.encode())

#Receive server_public_key
print("Waiting to receive server_public_key\n")
server_response = client_socket.recv(1024).decode()
print("Got server_public_key: ", server_response, "\n")
server_public_key = server_response

#Send and receive data
while True:
    #User can write a message
    message = input("Response to server: ")
    #Send a message
    client_socket.send(message.encode())
    
    #Close connection if requested
    if (message.lower() == "close"):
        print("Closing connection...")
        break
    
    #Receive response from server
    print("Waiting for server to respond...")
    response_data = client_socket.recv(1024).decode()
    print("Response from server: ", response_data, "\n")


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