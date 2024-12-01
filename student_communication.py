import socket
import json
import datetime
import pytz

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
        message = input('Enter message to send (type "exit" to disconnect): ')  

        # Send the message to the server
        client_socket.send(message.encode())

        # Receive the server's response
        data = client_socket.recv(1024).decode()
        print(f'Response from server: {data}')

        # Option to close the connection
        if message.lower() == 'exit':
            print('Closing connection.')
            break

    # Close the client connection
    client_socket.close()

#client_program()

def first_connection(port, student_name, character_name):

    host = socket.gethostbyname(socket.gethostname())
    port = int(port)

    # Create a socket object
    client_socket = socket.socket()

    # Connect to the server using the LAN IP
    try:
        client_socket.connect((host, port))
    except:
        return False, ''
    
    #find time after midnight in seconds
    current_timezone = pytz.timezone('Europe/London')
    current_time = datetime.datetime.now(current_timezone)
    seconds_since_midnight = current_time.hour * 3600 + current_time.minute * 60 + current_time.second 
    
    #make a JSON string to send
    data = {
        'student_name': student_name,
        'character_name': character_name,
        'last_connected': seconds_since_midnight
    }

    data_JSON = json.dumps(data)

    client_socket.send()
    