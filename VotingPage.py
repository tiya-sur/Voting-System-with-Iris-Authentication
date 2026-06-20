'''import tkinter as tk
import socket
from tkinter import *
from PIL import ImageTk, Image
import iris_integration
import camera_module

def voteCast(root, frame1, vote, client_socket):
    for widget in frame1.winfo_children():
        widget.destroy()

    client_socket.send(vote.encode())

    message = client_socket.recv(1024)
    print(message.decode())
    message = message.decode()
    if message == "Successful":
        Label(frame1, text="Vote Casted Successfully", font=('Helvetica', 18, 'bold')).grid(row=1, column=1)
    else:
        Label(frame1, text="Vote Cast Failed... \nTry again", font=('Helvetica', 18, 'bold')).grid(row=1, column=1)

    client_socket.close()

def votingPg(root, frame1, client_socket):
    root.title("Cast Vote")
    for widget in frame1.winfo_children():
        widget.destroy()

    Label(frame1, text="Cast Vote", font=('Helvetica', 18, 'bold')).grid(row=0, column=1, rowspan=1)
    Label(frame1, text="").grid(row=1, column=0)

    camera_module.capture_iris_image("voter_iris.jpg")
    iris_verified, message = iris_integration.verify_iris("voter_iris.jpg")

    if iris_verified:
        Label(frame1, text="Iris Verified. Proceeding to voting.", font=('Helvetica', 12)).grid(row=2, column=1)

        vote = StringVar(frame1, "-1")

        Radiobutton(frame1, text="BJP\n\nNarendra Modi", variable=vote, value="bjp", indicator=0, height=4, width=15,
                    command=lambda: voteCast(root, frame1, "bjp", client_socket)).grid(row=3, column=1)
        bjpLogo = ImageTk.PhotoImage((Image.open("img/bjp.png")).resize((45, 45), Image.LANCZOS))
        bjpImg = Label(frame1, image=bjpLogo).grid(row=3, column=0)

        Radiobutton(frame1, text="Congress\n\nRahul Gandhi", variable=vote, value="cong", indicator=0, height=4, width=15,
                    command=lambda: voteCast(root, frame1, "cong", client_socket)).grid(row=4, column=1)
        congLogo = ImageTk.PhotoImage((Image.open("img/cong.jpg")).resize((35, 48), Image.LANCZOS))
        congImg = Label(frame1, image=congLogo).grid(row=4, column=0)

        Radiobutton(frame1, text="Aam Aadmi Party\n\nArvind Kejriwal", variable=vote, value="aap", indicator=0, height=4,
                    width=15, command=lambda: voteCast(root, frame1, "aap", client_socket)).grid(row=5, column=1)
        aapLogo = ImageTk.PhotoImage((Image.open("img/aap.png")).resize((55, 40), Image.LANCZOS))
        aapImg = Label(frame1, image=aapLogo).grid(row=5, column=0)

        Radiobutton(frame1, text="Shiv Sena\n\nUdhav Thakrey", variable=vote, value="ss", indicator=0, height=4, width=15,
                    command=lambda: voteCast(root, frame1, "ss", client_socket)).grid(row=6, column=1)
        ssLogo = ImageTk.PhotoImage((Image.open("img/ss.png")).resize((50, 45), Image.LANCZOS))
        ssImg = Label(frame1, image=ssLogo).grid(row=6, column=0)

        Radiobutton(frame1, text="\nNOTA    \n  ", variable=vote, value="nota", indicator=0, height=4, width=15,
                    command=lambda: voteCast(root, frame1, "nota", client_socket)).grid(row=7, column=1)
        notaLogo = ImageTk.PhotoImage((Image.open("img/nota.jpg")).resize((45, 35), Image.LANCZOS))
        notaImg = Label(frame1, image=notaLogo).grid(row=7, column=0)

        frame1.pack()
        root.mainloop()

    else:
        Label(frame1, text=f"Iris verification failed: {message}", fg="red", font=('Helvetica', 12)).grid(row=2, column=1)
        frame1.pack()
        root.mainloop()
'''

'''import tkinter as tk
import socket
from tkinter import *
from PIL import ImageTk, Image
import iris_integration  # Assuming your iris integration module
import camera_module  # Assuming your camera module
import cv2
import numpy as np

# Assuming you have the following functions from your iris processing code:
# segment_iris, extract_features, match_iris_template, etc.

def voteCast(root, frame1, vote, client_socket):
    """Sends the vote to the server and handles the response."""
    for widget in frame1.winfo_children():
        widget.destroy()

    try:
        client_socket.send(vote.encode())
        message = client_socket.recv(1024).decode()
        print(message)

        if message == "Successful":
            Label(frame1, text="Vote Casted Successfully", font=('Helvetica', 18, 'bold')).grid(row=1, column=1)
        else:
            Label(frame1, text="Vote Cast Failed... \nTry again", font=('Helvetica', 18, 'bold')).grid(row=1, column=1)

    except socket.error as e:
        Label(frame1, text=f"Network Error: {e}", fg="red", font=('Helvetica', 12)).grid(row=1, column=1)
    finally:
        client_socket.close()

    frame1.pack()
    root.mainloop()

def votingPg(root, frame1, client_socket):
    """Handles the voting page logic."""
    root.title("Cast Vote")
    for widget in frame1.winfo_children():
        widget.destroy()

    Label(frame1, text="Cast Vote", font=('Helvetica', 18, 'bold')).grid(row=0, column=1, rowspan=1)
    Label(frame1, text="").grid(row=1, column=0)

    # Capture iris image using the camera module
    camera_module.capture_iris_image("voter_iris.jpg")

    # Load and process the captured iris image
    try:
        image = cv2.imread("voter_iris.jpg", cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError("Error loading iris image.")

        segmented_iris = iris_integration.segment_iris(image)
        if segmented_iris is None:
            raise ValueError("Iris segmentation failed.")

        features = iris_integration.extract_features(segmented_iris)
        if features is None:
            raise ValueError("Feature extraction failed.")

        iris_verified, message = iris_integration.match_iris_template(features)

        if iris_verified:
            Label(frame1, text="Iris Verified. Proceeding to voting.", font=('Helvetica', 12)).grid(row=2, column=1)

            vote = StringVar(frame1, "-1")

            Radiobutton(frame1, text="BJP\n\nNarendra Modi", variable=vote, value="bjp", indicator=0, height=4, width=15,
                        command=lambda: voteCast(root, frame1, "bjp", client_socket)).grid(row=3, column=1)
            bjpLogo = ImageTk.PhotoImage((Image.open("img/bjp.png")).resize((45, 45), Image.LANCZOS))
            bjpImg = Label(frame1, image=bjpLogo).grid(row=3, column=0)

            Radiobutton(frame1, text="Congress\n\nRahul Gandhi", variable=vote, value="cong", indicator=0, height=4, width=15,
                        command=lambda: voteCast(root, frame1, "cong", client_socket)).grid(row=4, column=1)
            congLogo = ImageTk.PhotoImage((Image.open("img/cong.jpg")).resize((35, 48), Image.LANCZOS))
            congImg = Label(frame1, image=congLogo).grid(row=4, column=0)

            Radiobutton(frame1, text="Aam Aadmi Party\n\nArvind Kejriwal", variable=vote, value="aap", indicator=0, height=4,
                        width=15, command=lambda: voteCast(root, frame1, "aap", client_socket)).grid(row=5, column=1)
            aapLogo = ImageTk.PhotoImage((Image.open("img/aap.png")).resize((55, 40), Image.LANCZOS))
            aapImg = Label(frame1, image=aapLogo).grid(row=5, column=0)

            Radiobutton(frame1, text="Shiv Sena\n\nUdhav Thakrey", variable=vote, value="ss", indicator=0, height=4, width=15,
                        command=lambda: voteCast(root, frame1, "ss", client_socket)).grid(row=6, column=1)
            ssLogo = ImageTk.PhotoImage((Image.open("img/ss.png")).resize((50, 45), Image.LANCZOS))
            ssImg = Label(frame1, image=ssLogo).grid(row=6, column=0)

            Radiobutton(frame1, text="\nNOTA  \n  ", variable=vote, value="nota", indicator=0, height=4, width=15,
                        command=lambda: voteCast(root, frame1, "nota", client_socket)).grid(row=7, column=1)
            notaLogo = ImageTk.PhotoImage((Image.open("img/nota.jpg")).resize((45, 35), Image.LANCZOS))
            notaImg = Label(frame1, image=notaLogo).grid(row=7, column=0)

            frame1.pack()
            root.mainloop()

        else:
            Label(frame1, text=f"Iris verification failed: {message}", fg="red", font=('Helvetica', 12)).grid(row=2, column=1)
            frame1.pack()
            root.mainloop()

    except Exception as e:
        Label(frame1, text=f"Error processing iris: {e}", fg="red", font=('Helvetica', 12)).grid(row=2, column=1)
        frame1.pack()
        root.mainloop()'''

        # VotingPage.py (or your main GUI file)

import tkinter as tk
import socket
from tkinter import *
from PIL import ImageTk, Image
import iris_integration  # Import your iris integration module
import camera_module  # Import your camera module

def voteCast(root, frame1, vote, client_socket):
    for widget in frame1.winfo_children():
        widget.destroy()

    client_socket.send(vote.encode())

    message = client_socket.recv(1024)
    print(message.decode())
    message = message.decode()
    if message == "Successful":
        Label(frame1, text="Vote Casted Successfully", font=('Helvetica', 18, 'bold')).grid(row=1, column=1)
    else:
        Label(frame1, text="Vote Cast Failed... \nTry again", font=('Helvetica', 18, 'bold')).grid(row=1, column=1)

    client_socket.close()

def votingPg(root, frame1, client_socket):
    root.title("Cast Vote")
    for widget in frame1.winfo_children():
        widget.destroy()

    Label(frame1, text="Cast Vote", font=('Helvetica', 18, 'bold')).grid(row=0, column=1, rowspan=1)
    Label(frame1, text="").grid(row=1, column=0)

    # Iris Verification Step:
    camera_module.capture_iris_image("voter_iris.jpg")  # Capture iris image
    iris_verified, message = iris_integration.verify_iris("voter_iris.jpg")  # Verify iris

    if iris_verified:
        Label(frame1, text="Iris Verified. Proceeding to voting.", font=('Helvetica', 12)).grid(row=2, column=1)

        vote = StringVar(frame1, "-1")

        Radiobutton(frame1, text="BJP\n\nNarendra Modi", variable=vote, value="bjp", indicator=0, height=4, width=15,
                    command=lambda: voteCast(root, frame1, "bjp", client_socket)).grid(row=3, column=1)
        bjpLogo = ImageTk.PhotoImage((Image.open("img/bjp.png")).resize((45, 45), Image.LANCZOS))
        bjpImg = Label(frame1, image=bjpLogo).grid(row=3, column=0)

        Radiobutton(frame1, text="Congress\n\nRahul Gandhi", variable=vote, value="cong", indicator=0, height=4, width=15,
                    command=lambda: voteCast(root, frame1, "cong", client_socket)).grid(row=4, column=1)
        congLogo = ImageTk.PhotoImage((Image.open("img/cong.jpg")).resize((35, 48), Image.LANCZOS))
        congImg = Label(frame1, image=congLogo).grid(row=4, column=0)

        Radiobutton(frame1, text="Aam Aadmi Party\n\nArvind Kejriwal", variable=vote, value="aap", indicator=0, height=4,
                    width=15, command=lambda: voteCast(root, frame1, "aap", client_socket)).grid(row=5, column=1)
        aapLogo = ImageTk.PhotoImage((Image.open("img/aap.png")).resize((55, 40), Image.LANCZOS))
        aapImg = Label(frame1, image=aapLogo).grid(row=5, column=0)

        Radiobutton(frame1, text="Shiv Sena\n\nUdhav Thakrey", variable=vote, value="ss", indicator=0, height=4, width=15,
                    command=lambda: voteCast(root, frame1, "ss", client_socket)).grid(row=6, column=1)
        ssLogo = ImageTk.PhotoImage((Image.open("img/ss.png")).resize((50, 45), Image.LANCZOS))
        ssImg = Label(frame1, image=ssLogo).grid(row=6, column=0)

        Radiobutton(frame1, text="\nNOTA    \n  ", variable=vote, value="nota", indicator=0, height=4, width=15,
                    command=lambda: voteCast(root, frame1, "nota", client_socket)).grid(row=7, column=1)
        notaLogo = ImageTk.PhotoImage((Image.open("img/nota.jpg")).resize((45, 35), Image.LANCZOS))
        notaImg = Label(frame1, image=notaLogo).grid(row=7, column=0)

        frame1.pack()
        root.mainloop()

    else:
        Label(frame1, text=f"Iris verification failed: {message}", fg="red", font=('Helvetica', 12)).grid(row=2, column=1)
        frame1.pack()
        root.mainloop()

# ---------------------------------------------------------------------

# voter.py (if you have this file, it might be the same as VotingPage.py)

# If voter.py is a separate file, you will need to add the same iris verification logic to it.
# The code would be very similar to the votingPg function.
# Example if voter.py existed as a seperate file.

# import tkinter as tk
# import socket
# from tkinter import *
# import iris_integration
# import camera_module

# def voter_main(root, frame, client_socket):
#     root.title("Voter Page")
#     for widget in frame.winfo_children():
#         widget.destroy()

#     Label(frame, text="Voter Page", font=('Helvetica', 18, 'bold')).grid(row=0, column=1)

#     camera_module.capture_iris_image("voter_iris.jpg")
#     iris_verified, message = iris_integration.verify_iris("voter_iris.jpg")

#     if iris_verified:
#         Label(frame, text="Iris Verified. Proceeding.", font=('Helvetica', 12)).grid(row=1, column=1)
#         #Add the rest of your voter page code here.
#     else:
#         Label(frame, text=f"Iris verification failed: {message}", fg="red", font=('Helvetica', 12)).grid(row=1, column=1)

#     frame.pack()
#     root.mainloop()