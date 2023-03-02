#pip install pycryptodome
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

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

#Open file, read lines and convert to bytes
# serverFile = open("serverFile.txt", "r")
print("\nOBS!   By default one file is available ->      'serverFile.txt'")
serverFile = open(input("Name of file to send: "), "r")
fileLines = serverFile.read()
serverFile.close()

#Encrypt serverFile with AES and session key
print("\nEncrypting file")
cipher = AES.new(session_key, AES.MODE_EAX)
nonce = cipher.nonce
encrypted_file, tag = cipher.encrypt_and_digest(fileLines.encode("utf-8"))

print("\nCiphertext:\n", encrypted_file)

#send nonce
print("\nSending nonce")
connection.send(nonce)

#wait for response
connection.recv(1024)

#send tag
print("\nSending tag")
connection.send(tag)

#wait for response
connection.recv(1024)

#send encrypted file
print("\nSending encrypted file")
connection.send(encrypted_file)