import tkinter as tk
from tkinter import messagebox
from tkinter import *

def run_script(label1, label2,label3,label4,label5):
    label4.config(text="-- Started --\n")
    label4.update()
    first_text = "CREDIT : SVJG"    
    label1.config(text=first_text)

def welcomepage():
    messagebox.showinfo("Login Successful", "Welcome, Admin!")


    root = tk.Tk()
    root.title("PDF Reader")
    # Set the window size and position
    window_width = 400
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2  # Center the window horizontally
    y = (screen_height - window_height) // 2  # Center the window vertically
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    # Create labels, buttons, or any other widgets here

    title_label = tk.Label(root, text="PDF Reader", font=("Helvetica", 16))
    title_label.pack()
    credential_label1 = tk.Label(root, text="", font=("Helvetica", 12))  # Empty label to display first credential
    credential_label1.pack()
    credential_label2 = tk.Label(root, text="", font=("Helvetica", 12))  # Empty label to display second credential
    credential_label2.pack()
    credential_label3 = tk.Label(root, text="", font=("Helvetica", 12))
    credential_label3.pack()

    credential_label4 = tk.Label(root, text="", font=("Helvetica", 12))
    credential_label4.pack()
    credential_label5 = tk.Label(root, text="", font=("Helvetica", 12))
    credential_label5.pack()
    run_script(credential_label1, credential_label2, credential_label3, credential_label4,credential_label5)
    # run_script_periodically() 
    root.mainloop()