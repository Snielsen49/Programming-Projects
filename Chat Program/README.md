# Overview
Server Program Overview:

Initialization: It sets up a socket to listen for incoming connections on a specified IP address and port.

Connection Handling: It continuously accepts incoming connections and adds clients to a list, displaying their IP addresses and usernames.

Message Handling: It receives messages from clients, broadcasts them to all other connected clients, and removes clients when they disconnect.

Client Crogram Overview
Initialization: It prompts the user to input their username and establishes a connection with the server.

Message Reception Thread: It continuously receives messages from the server in a separate thread, allowing concurrent handling of incoming messages.

Message Sending: It prompts the user to input messages and sends them to the server.

Interaction:

Start the server then start the clients. The server program listens for connections and handles message broadcasting among clients. The client program connects to the server, sends the user's username, and starts a thread to receive messages. Users can input messages in their client interface, which are then sent to the server and broadcasted to other clients by the server.

[Software Demo Video](https://youtu.be/hbUlDRpbzdQ)

# Network Communication

Architecture: This is a client/server aplication

This is a TCP or (Transmission Control Protocol) program and the port used is 1234 but can be changed in the code.

The messages being sent and recived are in this fortmat: header for user-name (number of characters in the user name), user-name, header for message (number of characters in the message), message

# Development Environment

I used VScode for this project 

libraries

Server:
socket
select 

Client:
socket
select
errno
sys
threading

# Useful Websites

* [Youtube](https://www.youtube.com/)
For research purposes
* [Chat GPT](https://chat.openai.com/)
For asking questions and getting help understanding sockets and threding 


# Future Work

* User interface
* A way to join and leave other servers
* Message saving and loading 