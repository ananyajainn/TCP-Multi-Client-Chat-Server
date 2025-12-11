import socket
import threading
import sys
import argparse


# TODO: Implement a client that connects to your server to chat with other clients here
  

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b"Hello, world")
#     data = s.recv(1024)

# print(f"Received {data!r}")

# HOST = "127.0.0.1"
# PORT = 65431 

parser = argparse.ArgumentParser(prog='TCP Chatroom Client')
parser.add_argument("-join", action="store_true")
parser.add_argument("-host")
parser.add_argument("-port", type=int)
parser.add_argument("-username")
parser.add_argument("-passcode")
args = parser.parse_args()
host, port, username, passcode = args.host, args.port, args.username, args.passcode


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

connected = False

def authenticate():
    global connected
    # send passcode
    client.send(passcode.encode("ascii"))
    response = client.recv(1024).decode("ascii")
    print(response)
    sys.stdout.flush()

    if "Incorrect" in response:
        client.close()
        sys.exit()
    
    # successful so send user
    client.send(username.encode("ascii"))
    connected = True


def receive():
    # accept messages from server
    while True: 
        if not connected:
            break
        try:
            message = client.recv(1024).decode("ascii")

            print(message)
            sys.stdout.flush()
        except:
            print("client error")
            client.close()
            break

def write():
    # write message to server
    global connected
    while True:
        if not connected:
            break
        message = input()
        if message == ":Exit":
            client.send(message.encode("ascii"))
            client.close()
            connected = False
            break
        else:
            #msg = f"{username}: {message}"
            client.send(message.encode("ascii"))
            

def start_client():
    authenticate()

    # set up two threads
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()

start_client()