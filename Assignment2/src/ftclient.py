import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

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
session_key = decrypted
print("\nDecrypted session key: ", decrypted)

#WORK FROM HERE

#Receive nonce
nonce = client_socket.recv(2048)

#Send response
client_socket.send(b"OK")

#Receive tag
tag = client_socket.recv(2048)

#Send response
client_socket.send(b"OK")

#Receive encrypted file
encrypted_file = client_socket.recv(2048)


#Decrypting
clientFile = open("clientFile.txt", "wb")
cipher = AES.new(session_key, AES.MODE_EAX, nonce)
original_data = cipher.decrypt_and_verify(encrypted_file, tag)
clientFile.write(original_data)

print("\nNONCE:\n", type(nonce))
print("\nTAG:\n", tag)
print("\nENCRYPTED_FILE:\n", encrypted_file)

client_socket.close()