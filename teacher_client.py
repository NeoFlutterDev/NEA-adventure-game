import socket
import threading
import random
import pygame 

pygame.init()

active_students = []
#tracks all current students connected

#get display information and set up screenScale
infoObject = pygame.display.Info()
screenScale = [infoObject.current_w / 1920, infoObject.current_h / 1080]

#initialize the game window
window = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
pygame.display.set_caption('Teacher Display')

def handle_client(conn, address):
    print(f"New connection from: {address}")
    active_students.append(conn)

    while True:
        try:
            # Receive data from the client
            data = conn.recv(1024).decode()
            if not data:
                break  # Student disconnected and leaves the queue

            print(f"Received from {address}: {data}")

            # Send a response to the student
            response = f"Server received: {data}"
            conn.send(response.encode())

        except Exception as e:
            print(f"Error with student {address}: {e}")
            break

    # Remove connection and close
    print(f"Connection closed from: {address}")
    active_students.remove(conn)
    conn.close()


def server_program():
    host = '0.0.0.0'  # Bind to all available interfaces allowing for easier server creation
    port = random.randint(2000, 9999) #creates a random port for students to join to

    students = int(input("How many students are in the class\n-> "))

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    # Server listens for incoming connections
    server_socket.listen(students)  # Allow enough connections in the queue for all the students
    print(f"Server is listening on port {port}...")

    # Main server loop to accept clients
    while True:
        if len(active_students) < students:
            # Accept a new student connection
            conn, address = server_socket.accept()
            # Start a new thread for each student to allow for all of them to be connected at the same time
            client_thread = threading.Thread(target=handle_client, args=(conn, address))
            client_thread.start()
        else:
            print("Server has reached the maximum number of {students} active connections.")
            break


def shutdown_server():
    print("Shutting down server...")
    for conn in active_students:
        conn.close()  # Close all active students
    exit()  # Close the program


server_program()
