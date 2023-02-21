import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

keyPair = RSA.generate(3072)
client_public_key = keyPair.publickey().exportKey()
session_key = None

def connect_to_server(host_name, port_number):
    print("\nSending connection request to server: ", host_name)

    try:
        client_socket.connect((host_name, port_number))
        server_response = client_socket.recv(1024).decode()
        
        if(server_response.lower() == "request accepted"):
            print("\nServer accepted connection request!")
            print("\nCONNECTION ESTABLISHED")
        else:
            print("\nServer declined request...")
   
    except:
        print("\nCould not connect to server...")
        #Close connection
        client_socket.close()

def receive_public_key():
    #Receive server_public_key
    print("\nWaiting to receive server_public_key")
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
print("\nSending public key")
client_socket.send(client_public_key)

#Receive encrypted session key from server
print("\nReceiving encrypted session key")
encrypted_session_key = client_socket.recv(2048)

#Decrypt session key with clients private key
print("\nDecrypting session key")
decryptor = PKCS1_OAEP.new(keyPair)
decrypted = decryptor.decrypt(encrypted_session_key)
session_key = decrypted

print("\nWaiting to receive encrypted file...")

#Receive nonce
nonce = client_socket.recv(2048)
print("\nReceived nonce")

#Send response
client_socket.send(b"OK")

#Receive tag
tag = client_socket.recv(2048)
print("\nReceived tag")

#Send response
client_socket.send(b"OK")

#Receive encrypted file
encrypted_file = client_socket.recv(2048)
print("\nReceived encrypted file")

#Decrypting
print("\nDecrypting file")
clientFile = open("ReceivedFile.txt", "wb")
cipher = AES.new(session_key, AES.MODE_EAX, nonce)
original_data = cipher.decrypt_and_verify(encrypted_file, tag)
print("\nSaving file to memory")
clientFile.write(original_data)
print("\nFILE SAVED!")

print("\nClosing connection")
client_socket.close()