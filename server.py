import socket
import threading
import sys
import argparse
from datetime import datetime, timedelta

#TODO: Implement all code for your server here

HOST = "127.0.0.1" #local client 

# handle args and save port # and passcode
parser = argparse.ArgumentParser(prog='TCP Chatroom Server')
parser.add_argument("-start", action="store_true")
parser.add_argument("-port", type=int)
parser.add_argument("-passcode")
args = parser.parse_args()
port, passcode = args.port, args.passcode

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, port))
server.listen()

clients = []
usernames = []

def broadcast(message, sender):
    # print(message)
    # sys.stdout.flush()
    # send message to all connected clients
    for client in clients:
        if client != sender:
            client.send(message)

def authenticate(client):
    # authenticate client
    client_password = client.recv(1024).decode("ascii")

    if client_password != passcode:
        client.send("Incorrect passcode".encode("ascii"))
        client.close()
        return False
    
    # client authenticated print success message
    auth_msg = f"Connected to {HOST} on port {port}" 
    client.send(auth_msg.encode("ascii"))
    return True

def handle_user(client):
    # add username (2nd message sent by client)
    user = client.recv(1024).decode("ascii")

    #join message
    join_msg = f"{user} joined the chatroom"
    print(join_msg)
    sys.stdout.flush()
    broadcast(join_msg.encode("ascii"), client)

    # add to clients
    usernames.append(user)
    clients.append(client)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            index = clients.index(client) 
            username = usernames[index]

            if message.decode("ascii") == ":Exit":
                kick_user(client)
                break

            elif message.decode("ascii") == ":Users":
                # print out who requested this 
                print(f"{username}: searched up active users")
                sys.stdout.flush()

                # send out active users to requester
                active_users = 'Active Users: ' + ', '.join(usernames)
                client.send(active_users.encode("ascii"))

            elif message.decode("ascii") == ":mytime":
                now = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
                current_time = f"{username}: {now}"
                client.send(current_time.encode("ascii"))
                print(current_time)
                sys.stdout.flush()
                broadcast(current_time.encode("ascii"), client)

            elif message.decode("ascii") == ":+1hr":
                future = (datetime.now() + timedelta(hours=1)).strftime("%a %b %d %H:%M:%S %Y")
                future_time = f"{username}: {future}"
                client.send(future_time.encode("ascii"))
                print(future_time)
                sys.stdout.flush()
                broadcast(future_time.encode("ascii"), client)
            
            elif ":Msg" in message.decode("ascii"):
                msg = message.decode("ascii")
                parts = msg.split(" ", 2)
                if len(parts) < 3:
                    client.send("bad format for private message".encode("ascii"))
                else:
                    _, username_2, p_message = parts
                    u2_index = usernames.index(username_2)
                    user2 = clients[u2_index]   

                    private_message = f"[Message from {username}]: {p_message}"
                    user2.send(private_message.encode("ascii"))

                    print(f"{username}: send message to {username_2}")
                    sys.stdout.flush()

            else:
                msg = message.decode("ascii")
                msg = msg.replace(":)", "[feeling happy]").replace(":(", "[feeling sad]")
                final_message = f"{username}: {msg}"
                print(final_message) 
                sys.stdout.flush()  
                broadcast(final_message.encode("ascii"), client)

        except Exception as e:
            print(f"Server exception: {e}")
            kick_user(client)
            break

def receive():
    # accept clients all the time
    while True:
        client, address = server.accept()

        if authenticate(client):
            handle_user(client)

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

def kick_user(client):
    if client in clients:
        index = clients.index(client) 
        user = usernames[index] 
        clients.remove(client)
        client.close()
        usernames.remove(user)
        message = f"{user} left the chatroom"
        print(message)
        sys.stdout.flush()
        broadcast(message.encode("ascii"), True)

def send_message(client):
    sender_idx = clients.index(client) 
    sender = usernames[index]
    receiver_idx = usernames.index()

    

   
print(f"Server started on port {port}. Accepting connections")
sys.stdout.flush()
receive()
