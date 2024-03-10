
import os
import sys
import requests
import PyPDF2
import re
from ftplib import FTP
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import adminpage


# Function to validate the login
def validate_login():
    userid = username_entry.get()
    password = password_entry.get()

    # You can add your own validation logic here
    if userid == "123" and password == "123":
        root.destroy()
        adminpage.welcomepage()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def run_script():
    

    userid = username_entry.get()
    password = password_entry.get()

    

    # current_directory = os.path.dirname(__file__)
    # os.chmod("D:/2024/PDF/", 0o755)
    # txt_file_path = os.path.join(current_directory, 'localpath.txt')
    # with open("D:/2024/PDF/", 'r') as dire:
    #     directory = dire.read()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login Form")

    # Set the window size and position
    window_width = 400
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2  # Center the window horizontally
    y = (screen_height - window_height) // 2  # Center the window vertically
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a canvas widget with scrollbars
    canvas = Canvas(root)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a vertical scrollbar
    v_scrollbar = Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=v_scrollbar.set)

    # Add a horizontal scrollbar
    h_scrollbar = Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
    h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.configure(xscrollcommand=h_scrollbar.set)

    # Create a frame to contain the widgets
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    # Add labels, entries, buttons, etc., to the frame
    title_label = tk.Label(frame, text="PDF Reader | CREDIT : SVJG", font=("Helvetica", 16))
    title_label.pack()

    username_label = tk.Label(frame, text="Userid:")
    username_label.pack()

    username_entry = tk.Entry(frame)
    username_entry.pack()

    password_label = tk.Label(frame, text="Password:")
    password_label.pack()

    password_entry = tk.Entry(frame, show="*")
    password_entry.pack()

    login_button = tk.Button(frame, text="Login", command=validate_login)
    login_button.pack()

    run_script()

    # Update the canvas scroll region when the frame size changes
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox(tk.ALL))

    root.mainloop()
    

