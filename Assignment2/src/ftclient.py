import socket
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import sys

keyPair = RSA.generate(3072)
client_public_key = keyPair.publickey().exportKey()
session_key = None

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
port_number = 5000

#Get socket instance
client_socket = socket.socket()

connect_to_server(host_name, port_number)

#send client_public_key to server
print("Sending public key...\n")
client_socket.send(client_public_key)

#Receive encrypted session key from server
print("\nReceiving encrypted session key")
encrypted_session_key = client_socket.recv(2048)

#Decrypt session key with clients private key
decryptor = PKCS1_OAEP.new(keyPair)
decrypted = decryptor.decrypt(encrypted_session_key)
print("\nDecrypted session key: ", decrypted)

#Receive list
sendlist = client_socket.recv(2048).decode()

print(sendlist)


client_socket.close()

#Receive file encrypted with AES
# encrypted_file = client_socket.recv(2048)

# #Decrypt file with session key
# iv = file_in.read()
# file_in = open("input_file.txt, rb")

# cipher = AES.new(session_key, AES.MODE_CFB, iv = iv)





# clientFile.close()



#Write file to memory