import socket
import json
from datetime import datetime, timedelta, timezone

def seconds_since_midnight():
    timeZone = timezone(timedelta(hours=0))
    currentTime = datetime.now(timeZone)
    secondsSinceMidnight = currentTime.hour * 3600 + currentTime.minute * 60 + currentTime.second 
    return secondsSinceMidnight

def connect_to_server(attempted_port):
    
    host = socket.gethostbyname(socket.gethostname())
    port = int(attempted_port)  # The port the server is listening on

    # Create a socket object
    client_socket = socket.socket()

    # Connect to the server using the LAN IP
    try:
        client_socket.connect((host, port))
    except:
        print('incorrect port')

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

    secondsSinceMidnight = seconds_since_midnight()
    
    #make a JSON string to send
    data = {
        'student_name': student_name,
        'character_name': character_name,
        'last_connected': seconds_since_midnight
    }

    data_JSON = json.dumps(data)

    client_socket.send()
    
print(seconds_since_midnight())