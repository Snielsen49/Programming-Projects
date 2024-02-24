# Overview

I decided to try and learn a little more with threading and sockets by pushing myself to make a LAN capable chess game. This project implements a network-based chess game using Python. It consists of a server that manages the game state and client connections, and a client application that players use to make moves and interact with the game. The game supports two players, with each player's moves being updated in real-time on the opponent's screen. It uses the same game code as my las chess project with a few tweaks to fit the server. To start the application, one must first run the server the start the two clients to play agent each other. 

[Software Demo Video](https://youtu.be/-_gjhiLxYZQ)

# Network Communication

This is a server/client aplication

This project uses TCP (Transmission Control Protocol) for communication between the client and the server.
it uses ports 5555 and 4092

When the client first connects it receives a pickled string of the color it will have for the game. (white or black) then it will receive and send the game_state dictionary that looks like this:

game_state: 

turnstep: 0  

white_pieces:['rook','knight','bishop','king','queen','bishop','knight','rook','pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']

black_pieces': ['rook','knight','bishop','king','queen','bishop','knight','rook','pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']

white_loc: []

black_loc: []

captured_pieces_wht: []

captured_pieces_blk: [],

winner: None

turn_color: 'white'

# Development Environment

I used VS code to program this. The libraries are: 
server:
socket
threading
pickle

client:
socket
pygame
pickle
queue
threading

# Useful Websites

* [Chat GPT](https://openai.com/)
For asking and answering questions as I went

# Future Work

* A way to join and leave other servers
* Add pawn promotion
* Add castling
* more fluid of a waiting window for the player who isn't playing 
