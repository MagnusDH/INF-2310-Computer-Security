#pip install pycryptodome
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

key = RSA.generate(2048)
server_private_key = key.exportKey() 
server_public_key = key.publickey().exportKey()
client_public_key = None
session_key = None


def create_socket(port_number):
    """
    -Create socket instance\n
    -Obtain name of host\n
    -bind host and given number"""
    server_host_name = socket.gethostname()

    server_socket = socket.socket()

    server_socket.bind((server_host_name, port_number))

    return server_socket

def connect_to_client(): 
    """
   -Accept an incomming connection\n
   -Send accept message back to client"""
    try:
        connection, address = server_socket.accept()
        print("Got connection request. Establishing connection with: ", address, "\n")
        message = "request accepted"
        connection.send(message.encode())
        print("CONNECTION ESTABLISHED!\n")
        return connection, address

    except:
        print("Could not establish connection with client...")

def receive_and_send_data():

    while True:
        #Receive data
        print("Waiting for client to respond...\n")
        receive_data = connection.recv(1024).decode()
        print("Response from client: ", receive_data, "\n")
        
        if receive_data.lower() == "close":
            print("Closing connection...")
            connection.close()

        else:
            #Send data from server
            response = input("Response to client: ")
            connection.send(response.encode())
    
    
#START

#Create socket
server_socket = create_socket(5001)

#Listen for connections
print("\nWaiting for clients to connect...")
server_socket.listen(5)

#Connect to client
connection, address = connect_to_client()

#Receive client_public_key
print("\nReceiving client public key...")
client_public_key = connection.recv(1024)

#send server_public_key
print("\nSending server_public_key...")
connection.send(server_public_key)

#receive and decrypt session key
print("TEST MAFAKKA")

encrypted_session_key = connection.recv(2048)
print("ENCRYPTED SESSION KEY: ", encrypted_session_key)

# cipher_rsa = PKCS1_OAEP.new(server_private_key)
# session_key = cipher_rsa.decrypt(encrypted_session_key)
# print("\nSESSION KEY: ", session_key)







        #FLOW OF PROGRAM
#client -> server: connection request
#client <- server: accept request
#Client -> server: send public key
#client <- server: send public key
#client -> server: session key
#client <_ server: file






























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