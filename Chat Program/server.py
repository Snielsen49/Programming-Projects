import socket
import select 

header_len = 10

#creating a socket 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#reuse address
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#binding the sock to a IP and port
sock.bind(('127.0.0.1', 1234))
sock.listen()

#setting up lists 
sock_list = [sock]
client_dict = {}

#receiving a message 
def receive_msg(client_sock):
    try:
        header = client_sock.recv(header_len)

        #error handling
        if not len(header):
            return False
        
        #returns msg
        else:
            msg_len = int(header.decode('UTF-8').strip())
            return {'header': header, 'data': client_sock.recv(msg_len)}
        
    #error handling
    except socket.error as e:
        print(f"Socket error: {e}")
        return False

#main loop 
while True:
    read_sockets, _, exception_sockets = select.select(sock_list, [], sock_list)

    for connected_sock in read_sockets:
        #new connection
        if connected_sock == sock:
            client_sock, client_add = sock.accept()

            #creates new client
            client = receive_msg(client_sock)

            #error
            if client is False:
                continue

            #adding new client to list and displaying info
            sock_list.append(client_sock)
            client_dict[client_sock] = client
            print(f'New connection from {client_add[0]}, {client_add[1]}')
            print(f"User Name: {client['data'].decode('UTF-8')}")
        
        #receiving a msg
        else:
            msg = receive_msg(connected_sock)

            #client leaving chat room
            if msg is False:
                client = client_dict[connected_sock]
                print(f'Closed connection from {client["data"].decode("UTF-8")}')

                #removing from lists 
                sock_list.remove(connected_sock)
                client_dict.pop(connected_sock)
                continue

            #printing msg
            client = client_dict[connected_sock]
            print(f'Received message from {client["data"].decode("UTF-8")}:')
            print(msg['data'].decode('UTF-8'))

            #sending msg to everyone 
            for client_sock in client_dict:
                #not sending msg to sender 
                if client_sock != connected_sock:
                    #sending msg 
                    client_sock.send(client['header'] + client['data'] + msg['header'] + msg['data'])

    #handling exceptions
    for connected_sock in exception_sockets:
        sock_list.remove(connected_sock)
        client_dict.pop(connected_sock)