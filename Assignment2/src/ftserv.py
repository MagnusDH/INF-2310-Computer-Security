#Server side

import socket

#Obtain the name of the host (magnus-linux)
server_host_name = socket.gethostname()
port_number = 5000

#Get socket instance
server_socket = socket.socket()

#Bind host address and port numer together
server_socket.bind((server_host_name, port_number))

#Listen for 5 connections
server_socket.listen(5)

#When connection request is recieved, connect to client
connection, address = server_socket.accept()
print("Made connection with address:", address, "\n")

#Receive or send data
while True:
    #Receive data
    print("Waiting to receive data...")
    receive_data = connection.recv(1024).decode()
    print("Received data:    ", receive_data, "\n")
    
    if receive_data.lower() == "close":
        print("Closing connection...")
        break

    else:
        #Send data from server
        response = "Got your message"
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