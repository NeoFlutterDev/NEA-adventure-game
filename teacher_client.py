import socket
import threading
import random
import pygame
import json
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt
import numpy as np

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
            data = conn.recv(4096).decode()  # Increased buffer size for larger messages
            if not data:
                break  # Client disconnected

            try:
                data = json.loads(data)

                # Handle heartbeat (ping)
                if "ping" in data and "uniqueID" in data:
                    studentData[studentNumber][2] = seconds_since_midnight()

                    # Store question data
                    if "questionData" in data:
                        for question in data["questionData"]:
                            questionKey = question["questionKey"]
                            correct = question["correct"]
                            incorrect = question["incorrect"]

                            # Store/update student performance
                            if questionKey not in studentData[studentNumber][1]:
                                studentData[studentNumber][1][questionKey] = {"correct": correct, "incorrect": incorrect}
                            else:
                                studentData[studentNumber][1][questionKey]["correct"] = correct
                                studentData[studentNumber][1][questionKey]["incorrect"] = incorrect

                    continue  # No need to send a response for a ping

                # Handle first-time connection (assign uniqueID)
                if "uniqueID" not in data:

                    uniqueID = ''.join([characters[random.randint(0, 93)] for _ in range(16)])
                    conn.send(uniqueID.encode())

                    # Update student data
                    studentName = data['student_name']
                    studentData[uniqueID] = [studentName, {}, seconds_since_midnight()]
                    #response = f"Server received: {data}"
                    #conn.send(response.encode())
            
            except Exception as e:
                print(f"Error with student {address}: {e}")
                break

        except Exception as e:
            print(f"Error with student {address}: {e}")
            break

    print(f"Connection closed from: {address}")

    # Only remove if conn is still in activeStudents
    if conn in activeStudents:
        activeStudents.remove(conn)
    else:
        print(f"Warning: Connection {conn} was not found in activeStudents.")

    try:
        conn.close()
    except Exception as e:
        print(f"Error closing connection: {e}")

# Update scores in the server's display window
def update_scores():
    while True:
        pass  # Placeholder function for updating scores periodically

def show_graph():
    questionIds = sorted({q for data in studentData.values() for q in data[1].keys()})

    correct_counts = [sum(data[1].get(q, {}).get("correct", 0) for data in studentData.values()) for q in questionIds]
    incorrect_counts = [sum(data[1].get(q, {}).get("incorrect", 0) for data in studentData.values()) for q in questionIds]

    x = np.arange(len(questionIds))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width/2, correct_counts, width, label='Correct', color='green')
    ax.bar(x + width/2, incorrect_counts, width, label='Incorrect', color='red')

    ax.set_xlabel("Question ID")
    ax.set_ylabel("Number of Responses")
    ax.set_title("Student Performance Per Question")
    ax.set_xticks(x)
    ax.set_xticklabels([f"Q{q}" for q in questionIds])
    ax.legend()

    plt.show(block=True)
    #scrape the question data from all the students and place it into a matplotlib graph

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

            question_id = i + 1  # Ensure the question number matches stored data

            correct_answers = sum(
                [data[1].get(question_id, {}).get("correct", 0) for key, data in studentData.items()]
            )
            incorrect_answers = sum(
                [data[1].get(question_id, {}).get("incorrect", 0) for key, data in studentData.items()]
            )

            scoreText1 = font.render(f"{correct_answers}", True, (255, 255, 255))
            scoreText2 = font.render(f"{incorrect_answers}", True, (255, 255, 255))

            window.blit(scoreText1, (startX1, yOffset1))
            window.blit(scoreText2, (startX2, yOffset2))

        # Render and blit each student's name and online/offline status
        baseY = 50
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
            window.blit(studentStatus, (0, baseY))
            baseY += incrementY

        window.blit(pygame.image.load('sprites/buttons/graph.png'), (1490, 950))

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            if (mouseX >= 1490 and mouseX <= 1790) and (mouseY >= 950 and mouseY <= 1070):
                print("Graph button clicked!")
                threading.Thread(target=show_graph).start()

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
