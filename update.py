import tkinter as tk
from tkinter import ttk,Canvas, Scrollbar, messagebox
import requests
import os
import zipfile
import threading

def download_and_extract(url):
    response = requests.get(url, stream=True)
    total_length = response.headers.get('content-length')

    if total_length is None:
        total_length = 0

    save_path = os.path.join(os.getcwd(), "file.rar")

    with open(save_path, 'wb') as f:
        dl = 0
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            f.write(data)
            percentage = int((dl / int(total_length)) * 100)
            progress_bar['value'] = percentage
            progress_label.config(text=f"Downloading: {percentage}%")
            root.update_idletasks()
    
    # unzipFile(save_path)

    # os.remove(save_path)
    progress_label.config(text="Completed!")
    messagebox.showinfo("Success", "Installation Completed!")
def unzipFile(save_path):
    progress_label.config(text="Extracting...")
    root.update_idletasks()
    with zipfile.ZipFile(save_path, 'r') as zip_ref:
        total_files = len(zip_ref.filelist)
        extracted_files = 0
        for file_info in zip_ref.filelist:
            filename = file_info.filename
            extracted_files += 1

            # Construct the full path of the extracted file
            extracted_file_path = os.path.join(os.getcwd(), filename)

            # Check if the file already exists in the directory
            if os.path.exists(extracted_file_path):
                # Check if the extracted file is newer than the existing one
                if os.path.getmtime(extracted_file_path) < file_info.date_time:
                    # Delete the older file
                    os.remove(extracted_file_path)
                else:
                    # If the existing file is newer, skip extraction
                    continue

            # Extract the file
            zip_ref.extract(filename, os.getcwd())

            # Update progress
            percentage = int((extracted_files / total_files) * 50) + 50  # Extraction progress from 50% to 100%
            progress_bar['value'] = percentage
            progress_label.config(text=f"Extracting: {percentage}%")
            root.update_idletasks()
    return True

def validate_login():
    url = url_entry.get()
    threading.Thread(target=download_and_extract, args=(url,)).start()

def run_script():
    # Add your script here
    pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("UPDATE FORM")

    # Set the window size and position
    window_width = 400
    window_height = 250
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

    login_button = tk.Button(frame, text="Download", command=validate_login)
    login_button.pack()

    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")
    progress_bar.pack()

    progress_label = tk.Label(frame, text="")
    progress_label.pack()

    run_script()

    # Update the canvas scroll region when the frame size changes
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox(tk.ALL))

    root.mainloop()
