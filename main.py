import tkinter as tk
import socket
from tkinter import *
from VotingPage import votingPg
import camera_module
import cv2
import numpy as np
import iris_integration  # Import the iris_integration module

def establish_connection():
    try:
        host = socket.gethostname()
        port = 4001
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(client_socket)
        message = client_socket.recv(1024)
        if message.decode() == "Connection Established":
            return client_socket
        else:
            return 'Failed'
    except Exception as e:
        print(f"Connection Failed, check if server is running... Error: {e}")
        return 'Failed'

def failed_return(root, frame1, client_socket, message):
    for widget in frame1.winfo_children():
        widget.destroy()
    message = message + "... \nTry again..."
    Label(frame1, text=message, font=('Helvetica', 12, 'bold')).grid(row=1, column=1)
    try:
        if client_socket != 'Failed':  # only close if a socket was created.
            client_socket.close()
    except Exception as e:
        print(f"Error closing socket: {e}")

def log_server(root, frame1, client_socket, voter_ID, password):
    if not (voter_ID and password):
        voter_ID = "0"
        password = "x"
    message = voter_ID + " " + password
    try:
        client_socket.send(message.encode())
        message = client_socket.recv(1024).decode()
        if message == "Authenticate":
            camera_module.capture_iris_image("voter_iris.jpg")
            iris_verified, iris_message = iris_integration.verify_iris("voter_iris.jpg")  # Use iris_integration.verify_iris

            if iris_verified:
                votingPg(root, frame1, client_socket)
            else:
                failed_return(root, frame1, client_socket, f"Iris verification failed: {iris_message}")
        elif message == "VoteCasted":
            message = "Vote has Already been Cast"
            failed_return(root, frame1, client_socket, message)
        elif message == "InvalidVoter":
            message = "Invalid Voter"
            failed_return(root, frame1, client_socket, message)
        else:
            message = "Server Error"
            failed_return(root, frame1, client_socket, message)
    except Exception as e:
        failed_return(root, frame1, client_socket, f"Server communication error: {e}")

def voterLogin(root, frame1):
    client_socket = establish_connection()
    if client_socket == 'Failed':
        message = "Connection failed"
        failed_return(root, frame1, client_socket, message)
        return
    root.title("Voter Login")
    for widget in frame1.winfo_children():
        widget.destroy()
    Label(frame1, text="Voter Login", font=('Helvetica', 18, 'bold')).grid(row=0, column=2, rowspan=1)
    Label(frame1, text="").grid(row=1, column=0)
    Label(frame1, text="Voter ID:      ", anchor="e", justify=LEFT).grid(row=2, column=0)
    Label(frame1, text="Password:   ", anchor="e", justify=LEFT).grid(row=3, column=0)
    voter_ID = tk.StringVar()
    password = tk.StringVar()
    e1 = Entry(frame1, textvariable=voter_ID)
    e1.grid(row=2, column=2)
    e3 = Entry(frame1, textvariable=password, show='*')
    e3.grid(row=3, column=2)
    sub = Button(frame1, text="Login", width=10, command=lambda: log_server(root, frame1, client_socket, voter_ID.get(), password.get()))
    Label(frame1, text="").grid(row=4, column=0)
    sub.grid(row=5, column=3, columnspan=2)
    frame1.pack()
    root.mainloop()