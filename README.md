# TCP-Multi-Client-Chat-Server

## Overview

This project is a client-server chatroom application that demonstrates basic network programming concepts using TCP and UDP sockets.
The chatroom allows multiple clients to connect to a server, authenticate with a passcode, communicate with each other, and use shortcut commands.
This project is designed to familiarize users with socket programming, client-server architecture, maintaining multiple persistent TCP connections, text parsing, and designing a simple application-layer protocol.

---

## Project Objectives

**TCP Socket Usage:** Demonstrates persistent TCP connections, reliable communication, and connection management.
**Client-Server Architecture:** Implements multi-client handling using threads and a central chatroom server.
**Application-Layer Protocol Design:** Includes username negotiation, passcode authentication, and custom text-based commands.
**Shortcut Commands:** Allows users to trigger special behaviors such as time formatting, emotions, and private messaging.
**Graceful Exit Handling:** Ensures proper cleanup and notification when clients disconnect.

---

## Features

* Multi-client chatroom
* Password-protected server access
* Username registration
* Broadcast messaging
* Private messaging
* Custom command parsing
* Time-based commands
* User listing
* Graceful disconnects

---

## Shortcut Commands

```
:)                     Display: [feeling happy]
:(                     Display: [feeling sad]
:mytime                Display the current system time
:+1hr                  Display the current system time + 1 hour
:Users                 List all active users
:Msg <user> <msg>      Send a private message to a specific user
:Exit                  Disconnect from the server
\                      Escape the next word to prevent command interpretation
```

**Time Format Example:**
`Mon Aug 13 08:23:14 2012`

---

## Running the Application

### 1. Start the Server

Run the server in its own terminal window:

```
python3 server.py -start -port <port> -passcode <passcode>
```

Example:

```
python3 server.py -start -port 65432 -passcode secret123
```

Server Output:

```
Server started on port 65432. Accepting connections...
```

---

### 2. Start a Client

Run each client in a separate terminal:

```
python3 client.py -join -host <host> -port <port> -username <username> -passcode <passcode>
```

Example:

```
python3 client.py -join -host 127.0.0.1 -port 65432 -username Alice -passcode secret123
```

Client Output:

```
Connected to 127.0.0.1 on port 65432
```

Server Output:

```
Alice joined the chatroom
```

---

### Example: When a second client joins

Command:

```
python3 client.py -join -host 127.0.0.1 -port 65432 -username Bob -passcode secret123
```

Server Output:

```
Bob joined the chatroom
```

New Client Output:

```
Connected to 127.0.0.1 on port 65432
```

All Other Clients Output:

```
Bob joined the chatroom
```

