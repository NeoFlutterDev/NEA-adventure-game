import socket
import threading
import random
import pygame
import json
from datetime import datetime, timedelta, timezone

pygame.init()

# Global variables
characters = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_{|}~")
activeStudents = []  # Tracks all current students connected
studentData = {}  # To store student info (name, scores, last message time)

# Function to calculate seconds since midnight
def seconds_since_midnight():
    timeZone = timezone(timedelta(hours=0))
    currentTime = datetime.now(timeZone)
    secondsSinceMidnight = currentTime.hour * 3600 + currentTime.minute * 60 + currentTime.second
    return secondsSinceMidnight

# Handle student connections
def handle_client(conn, address, studentNumber):
    print(f"New connection from: {address}")
    activeStudents.append(conn)

    while True:
        try:
            # Receive data from the client
            data = conn.recv(1024).decode()
            if not data:
                break  # Student disconnected and leaves the queue

            try:
                data = json.loads(data)
                data['uniqueID']
            except:
                data = json.loads(data)
                uniqueID = ''.join([characters[random.randint(0, 93)] for _ in range(16)])
                conn.send(uniqueID.encode())

            # Update student data
            studentName = f"Student {studentNumber}"
            studentData[studentNumber] = [studentName, {"correct": 0, "incorrect": 0}, seconds_since_midnight()]
            response = f"Server received: {data}"
            conn.send(response.encode())

        except Exception as e:
            print(f"Error with student {address}: {e}")
            break

    # Remove connection and close
    print(f"Connection closed from: {address}")
    activeStudents.remove(conn)
    conn.close()

# Update scores in the server's display window
def update_scores():
    while True:
        pass  # Placeholder function for updating scores periodically

# Server program to manage connections, pygame window, and data display
def server_program():
    host = '0.0.0.0'  # Bind to all available interfaces allowing for easier server creation
    port = random.randint(49125, 65535)  # Create a random port for students to join

    students = int(input("How many students are in the class\n-> "))

    # Initialize the game window after getting the number of students
    infoObject = pygame.display.Info()
    screenScale = [infoObject.current_w / 1920, infoObject.current_h / 1080]
    window = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption('Teacher Display')

    # Load and scale the background image
    backgroundImage = pygame.image.load('sprites/backdrops/teacher screen.png')
    backgroundImage = pygame.transform.scale(
        backgroundImage, (int(backgroundImage.get_width() * screenScale[0]), int(backgroundImage.get_height() * screenScale[1]))
    )

    # Create a socket object
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))

    # Server listens for incoming connections
    serverSocket.listen(students)  # Allow enough connections in the queue for all the students
    print(f"Server is listening on port {port}...")

    # Start the score update thread
    scoreThread = threading.Thread(target=update_scores, daemon=True)
    scoreThread.start()

    studentNumber = 1
    running = True
    while running:
        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop if the user quits

        # Draw the background image
        window.blit(backgroundImage, (0, 0))

        # Render and blit the pin code
        font = pygame.font.Font(None, 74)
        pinCodeText = font.render(f'{port}', True, (255, 255, 255))
        window.blit(pinCodeText, (1650, 15))

        # Render and blit the score data
        question_id = 1  # Change this to the specific question you want to track
        startX1, startY1 = 1500, 210  # Start position
        startX2, startY2 = 1700, 210  # Start position
        incrementY = 75  # Moves the text down by 75 pixels per iteration

        for i in range(10):
            yOffset1 = startY1 + (i * incrementY)
            yOffset2 = startY2 + (i * incrementY)
            
            scoreText1 = font.render(
                f"{sum([data[1].get('correct', 0) for key, data in studentData.items() if key == question_id])} ",
                True, (255, 255, 255)
            )
            scoreText2 = font.render(
                f"{sum([data[1].get('incorrect', 0) for key, data in studentData.items() if key == question_id])}",
                True, (255, 255, 255)
            )
            window.blit(scoreText1, (startX1, yOffset1))
            window.blit(scoreText2, (startX2, yOffset2))

        # Render and blit each student's name and online/offline status
        baseY = 10
        incrementY = 50  # Spacing between student entries
        for studentNumber, data in studentData.items():
            if data:
                name, scores, lastMessageTime = data
                secondsNow = seconds_since_midnight()
                status = "Online" if secondsNow - lastMessageTime <= 60 else "Offline"
                studentText = f"{name}: {status}"
            else:
                studentText = f"Student {studentNumber}: Offline"

            studentStatus = font.render(studentText, True, (255, 255, 255))
            window.blit(studentStatus, (30, baseY))
            baseY += incrementY

        pygame.display.flip()

        # Accept new connections if there's space
        if len(activeStudents) < students:
            try:
                # Accept a new student connection
                serverSocket.settimeout(0.5)  # Non-blocking accept with timeout
                try:
                    conn, address = serverSocket.accept()
                    # Start a new thread for each student to allow for all of them to be connected at the same time
                    clientThread = threading.Thread(target=handle_client, args=(conn, address, studentNumber))
                    clientThread.start()
                    studentNumber += 1
                except socket.timeout:
                    pass  # Continue the loop if no connection is made during the timeout
            except Exception as e:
                print(f"Server error: {e}")
        else:
            print(f"Server has reached the maximum number of {students} active connections.")
            running = False

    shutdown_server()

# Function to shut down the server
def shutdown_server():
    print("Shutting down server...")
    for conn in activeStudents:
        conn.close()  # Close all active students
    pygame.quit()
    exit()  # Close the program

server_program()
