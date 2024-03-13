
import os
import sys
import requests
import PyPDF2
import re
from ftplib import FTP
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import zipfile
import io
# import adminpage


# Function to validate the login
def validate_login():
    url = url_entry.get()
    response = requests.get(url)

    save_path = os.path.join(os.getcwd(), "downloaded_file.zip")
    print(save_path)

    with open(save_path, 'wb') as f:
        f.write(response.content)
    
    with zipfile.ZipFile(save_path, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())

    os.remove(save_path)

    
    messagebox.showinfo("Success", "Installed")
    # API 
    

def call_api(url, data):
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            # If the request was successful, return the response content
            return response.json()
        else:
            # If there was an error, print the error code and message
            print(f"Error: {response.status_code}, {response.text}")
            messagebox.showerror("Failed", f"Error: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        # If an exception occurs, print the exception
        print(f"Exception: {e}")
        messagebox.showerror("Failed", f"Exception: {e}")
        return False
        
def run_script():    

    userid = url_entry.get()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("UPDATE FORM")

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

    url_label = tk.Label(frame, text="Update URL:")
    url_label.pack()

    url_entry = tk.Entry(frame)
    url_entry.pack()


    login_button = tk.Button(frame, text="Add", command=validate_login)
    login_button.pack()

    run_script()

    # Update the canvas scroll region when the frame size changes
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox(tk.ALL))

    root.mainloop()
    

