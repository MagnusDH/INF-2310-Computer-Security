import socket
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

key = RSA.generate(2048)
client_private_key = key.exportKey() 
client_public_key = key.publickey().exportKey()
server_public_key = None
session_key = get_random_bytes(16)
print("\nSESSION KEY: ", session_key)

def connect_to_server(host_name, port_number):
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

def receive_public_key():
    #Receive server_public_key
    print("Waiting to receive server_public_key\n")
    server_response = client_socket.recv(1024)
    server_public_key = server_response

def send_and_receive_data():
    while True:
        #User can write a message
        message = input("Response to server: ")
        #Send a message
        client_socket.send(message.encode())
        
        #Close connection if requested
        if (message.lower() == "close"):
            print("Closing connection...")
            client_socket.close()
            break
        
        #Receive response from server
        print("Waiting for server to respond...")
        response_data = client_socket.recv(1024).decode()
        print("Response from server: ", response_data, "\n")

#START

#Obtain the name of the client (magnus-linux)
host_name = socket.gethostname()
port_number = 5001

#Get socket instance
client_socket = socket.socket()

connect_to_server(host_name, port_number)

#send client_public_key to server
print("Sending public key...\n")
client_socket.send(client_public_key)

#Receive server_public_key
print("\nReceiving server_public_key")
server_public_key = client_socket.recv(2048)


#Encrypt session key with server_public_key and send
cipher_rsa = PKCS1_OAEP.new(server_public_key)
encrypted_session_key = cipher_rsa.encrypt(session_key)
client_socket.send(encrypted_session_key)
print("ENCRYPTED SESSION KEY:   ", encrypted_session_key)

# #receive file via AES



























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