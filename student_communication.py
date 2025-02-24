import threading
import time
import database
import socket
import json
from datetime import datetime, timedelta, timezone

def seconds_since_midnight():
    timeZone = timezone(timedelta(hours=0))
    currentTime = datetime.now(timeZone)
    secondsSinceMidnight = currentTime.hour * 3600 + currentTime.minute * 60 + currentTime.second 
    return secondsSinceMidnight

def send_heartbeat(uniqueID, port, accountKey):
    host = socket.gethostbyname(socket.gethostname())  # Server address
    while True:
        try:
            questionData = database.questions_for_communication(accountKey)
            clientSocket = socket.socket()
            clientSocket.connect((host, port))  # Reconnect to server
            heartbeatData = json.dumps({"uniqueID": uniqueID, "ping": True, 'questionData':questionData})
            clientSocket.send(heartbeatData.encode('utf-8'))
            clientSocket.close()

        except Exception as e:
            print(f"Failed to send heartbeat: {e}")
        time.sleep(60)  # Wait for 60 seconds

def first_connection(port, studentName, characterName, accountKey):
    host = socket.gethostbyname(socket.gethostname())

    clientSocket = socket.socket()
    try:
        clientSocket.connect((host, port))
    except:
        return False, ''

    data = {
        "student_name": studentName,
        "character_name": characterName,
        "last_connected": time.time()
    }
    dataJSON = json.dumps(data)

    clientSocket.send(dataJSON.encode('utf-8'))

    # Receive unique ID
    uniqueID = clientSocket.recv(1024).decode()
    clientSocket.close()  # Close initial connection

    # Start heartbeat thread
    heartbeat_thread = threading.Thread(target=send_heartbeat, args=(uniqueID, port, accountKey), daemon=True)
    heartbeat_thread.start()

    return True, uniqueID