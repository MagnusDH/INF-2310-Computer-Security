#pip install pycryptodome
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
# from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

keyPair = RSA.generate(3072)
server_private_key = keyPair.exportKey() 
server_public_key = keyPair.publickey()#.exportKey()
client_public_key = None
session_key = b"ThisIsSessionKey"


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
        print("\nGot connection request. Establishing connection with: ", address)
        message = "request accepted"
        connection.send(message.encode())
        print("\nCONNECTION ESTABLISHED!")
        return connection, address

    except:
        print("\nCould not establish connection with client...")

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
server_socket = create_socket(5000)

#Listen for connections
print("\nWaiting for clients to connect...")
server_socket.listen(5)

#Connect to client
connection, address = connect_to_client()

#Receive client_public_key
print("\nReceiving client public key...")
client_public_key = RSA.importKey(connection.recv(2048))

#Encrypt session key with RSA
print("\nEncrypting session key")
encryptor = PKCS1_OAEP.new(client_public_key)
encrypted_session_key = encryptor.encrypt(session_key)

#Send session key
print("\nSending encrypted session key")
connection.send(encrypted_session_key)



#WORK FROM HERE
#Open file, read lines and convert to bytes
serverFile = open("serverFile.txt", "r")
fileLines = serverFile.read()
serverFile.close()
# connection.send(fileLines.encode("utf-8"))

#Encrypt serverFile with AES and session key
cipher = AES.new(session_key, AES.MODE_EAX)
ciphered_data, tag = cipher.encrypt_and_digest(fileLines)
# cipher.nonce
# print("\nChipered data type: ", type(ciphered_data))

# #Send encrypted file
# connection.send(ciphered_data)





        #FLOW OF PROGRAM
#client -> server: connection request
#client <- server: accept request
#Client -> server: send public key
#Client <- server: encrypt and send session key
#client <- server: encrypted file































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