
import os
import sys
import requests
import PyPDF2
import re
from ftplib import FTP
import tkinter as tk
from tkinter import messagebox
from tkinter import *
# import adminpage
import mysql.connector

# Function to validate the login
def validate_login():
    userid = username_entry.get()
    # password = password_entry.get()

    # API 
    if userid :
        url = 'http://192.168.43.187/pdfadmin/API/create_branch.php'
        data = {
                'branch': userid,
            }
        result = call_api(url, data)
        if result['Message']:
            if result['Message']['Code'] == 200:
                code = result['Message']['key']
                file_path = r"C:\pdf_reader\key.txt"
                if os.path.exists(file_path):
                    try:
                        with open(file_path, "a+") as f:
                            f.seek(0)  # Move the cursor to the beginning of the file
                            existing_content = f.read()
                            if existing_content:
                                f.truncate(0)
                                f.write(code)
                            else:
                                f.write(code)
                    except Exception as e:
                        messagebox.showerror("Failed", f"Error occurred while creating or updating file: {e}")
                else:
                    try:
                        with open(file_path, "w") as f:
                            f.write(code)
                    except Exception as e:
                        messagebox.showerror("Failed", f"Error occurred while creating or updating file: {e}")
                messagebox.showinfo("Success", "Successfully registered..")
                root.destroy()
            else:
                messagebox.showerror("Failed", result['Message']['Message'])
            
        else:
            messagebox.showerror("Failed", "Api Filed! Please try again")

        # root.destroy()
        # adminpage.welcomepage()
    else:
        messagebox.showerror("Failed", "Please fill branch name")

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
    

    userid = username_entry.get()
    # password = password_entry.get()

    

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

    username_label = tk.Label(frame, text="Branch Name:")
    username_label.pack()

    username_entry = tk.Entry(frame)
    username_entry.pack()

    # password_label = tk.Label(frame, text="Password:")
    # password_label.pack()

    # password_entry = tk.Entry(frame, show="*")
    # password_entry.pack()

    login_button = tk.Button(frame, text="Add", command=validate_login)
    login_button.pack()

    run_script()

    # Update the canvas scroll region when the frame size changes
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox(tk.ALL))

    root.mainloop()
    

