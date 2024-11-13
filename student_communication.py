import socket

def client_program(attempted_port):
    
    host = socket.gethostbyname(socket.gethostname())
    port = int(attempted_port)  # The port the server is listening on

    # Create a socket object
    client_socket = socket.socket()

    # Connect to the server using the LAN IP
    try:
        client_socket.connect((host, port))
    except:
        print('incorrect port')
    
    while True:
        # Input message to send to the server
        message = input("Enter message to send (type 'exit' to disconnect): ")

        # Send the message to the server
        client_socket.send(message.encode())

        # Receive the server's response
        data = client_socket.recv(1024).decode()
        print(f"Response from server: {data}")

        # Option to close the connection
        if message.lower() == 'exit':
            print("Closing connection.")
            break

    # Close the client connection
    client_socket.close()

#client_program()

def first_connection(port):

    host = socket.gethostbyname(socket.gethostname())
    port = int(port)

    # Create a socket object
    client_socket = socket.socket()

    # Connect to the server using the LAN IP
    try:
        client_socket.connect((host, port))
    except:
        return False, ''

    client_socket.send()
    