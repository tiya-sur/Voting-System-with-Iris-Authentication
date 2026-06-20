# eye_status.py
import tkinter as tk

def show_eye_status(is_open):
    root = tk.Tk()
    root.title("Eye Status")
    
    if is_open:
        message = "Eyes are Open"
    else:
        message = "Eyes are Closed"
    
    label = tk.Label(root, text=message, font=('Helvetica', 18, 'bold'))
    label.pack(pady=20)
    
    button = tk.Button(root, text="Close", command=root.destroy)
    button.pack(pady=10)
    
    root.mainloop()