import socket
import select
import errno
import sys
import threading

header_len = 10

def receive_messages(sock):
    while True:
        try:
            while True:
                user_header = sock.recv(header_len)

                # Server closed
                if not len(user_header):
                    print('Connection closed')
                    sys.exit()

                # Getting user name
                user_len = int(user_header.decode('utf-8').strip())
                user_name = sock.recv(user_len).decode('utf-8')

                # Getting message
                msg_header = sock.recv(header_len)
                msg_len = int(msg_header.decode('utf-8').strip())
                msg = sock.recv(msg_len).decode('utf-8')

                # Output message
                print(f'{user_name} > {msg}')

        # IO errors
        except IOError as e:
            # No more messages to receive
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Receiving Error:', str(e))
                sys.exit()
            continue

        # InterruptedError
        except InterruptedError as e:
            continue

        # General errors
        except Exception as e:
            print('Error:', str(e))
            sys.exit()


def main():
    user = input('User Name: ')

    # Creating a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecting to server
    sock.connect(('127.0.0.1', 1234))
    sock.setblocking(False)

    # Prepares header for user
    user_encoded = user.encode('utf-8')
    user_header = f'{len(user_encoded):<{header_len}}'.encode('utf-8')
    sock.send(user_header + user_encoded)

    # Start the thread to receive messages
    recv_thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
    recv_thread.start()

    while True:
        # Getting message
        msg = input(f'')

        # Message entered and sent
        if msg:
            msg = msg.encode('utf-8')
            msg_header = f'{len(msg):<{header_len}}'.encode('utf-8')
            sock.send(msg_header + msg)

main()