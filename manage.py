
import os
import sys
import requests
import PyPDF2
import re
from ftplib import FTP
import tkinter as tk
import shutil
from tkinter import messagebox
from googletrans import Translator
import ast

def call_api(url, data):
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            # If the request was successful, return the response content
            return response.json()
        else:
            # If there was an error, print the error code and message
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        # If an exception occurs, print the exception
        print(f"Exception: {e}")
def read_pdf_from_ftp(server, username, password, remote_path):
    try:
        # Connect to the FTP server
        ftp = FTP(server)
        ftp.login(username, password)
        
        # Change to the remote directory
        ftp.cwd(remote_path)
        
        # List files in the directory
        files = ftp.nlst()
        files = [file for file in files if file not in ['.', '..','.ftpquota','Thumbs.db']]
        # print(files)
        # Assuming there's only one PDF file, retrieve the first one
        if files:
            pdf_filename = files[0]
            with open(pdf_filename, 'wb') as local_file:
                print(local_file)
                ftp.retrbinary('RETR ' + pdf_filename, local_file.write)

            # Open the local file
            with open(pdf_filename, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)

                # Extract text from all pages
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()

                newdata = {'data':text,'name':pdf_filename}
                return newdata
        else:
            print("No PDF files found in the directory.")
            return None

    except Exception as e:
        print(f"Error fetching PDF from FTP: {e}")
        return None
   
    # finally:
    #     # Close the FTP connection
    #     ftp.quit()

def read_pdf(pdf_path):
    try:
        # Open the PDF file
        
        with open(pdf_path, 'rb') as pdf_file:
            # print(111)
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Extract text from all pages
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            return text

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
def local_read_pdf(directory, pdf_file):
    with open(os.path.join(directory, pdf_file), 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text
def translate_to_arabic(text):
    translator = Translator()
    translated = translator.translate(text, src='en', dest='ar')
    return translated.text
def CheckCommon():
    key = ""
    #check database connection
    
    
    #Directory path check
    directory_path = "C:\\pdf_reader"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    file_path = r"C:\pdf_reader\key.txt"
    if os.path.exists(file_path):
        try:
            with open(file_path, "a+") as f:
                f.seek(0)
                existing_content = f.read()
                if existing_content:
                    url = 'https://pdfadmin.000webhostapp.com/API/validate_code.php'
                    data = {
                            'code': existing_content,
                        }
                    result = call_api(url, data)
                    if result['Message']:
                        if result['Message']['Code'] == 200:
                            key = existing_content
                        else:
                            message = "Invalid Key"
                            errorLog('','key', message)
                            messagebox.showerror("Error Key", message)
                            root.destroy()
                            sys.exit(1)
                    else:
                        message = "Api Falied"
                        errorLog('','Api', message)
                        messagebox.showerror("Api error", message)
                        root.destroy()
                        sys.exit(1)
                else:
                    message = "Key is empty"
                    errorLog('','keyisempty', message)
                    messagebox.showerror("Key Error", message)
                    root.destroy()
                    sys.exit(1)
        except Exception as e:
            message = "Key file is missing or can't read"
            errorLog('','keyfile', message)
            messagebox.showerror("Key Err", message)
            root.destroy()
            sys.exit(1)
    return key
def errorLog(branch,error, message):
    url = 'https://pdfadmin.000webhostapp.com/API/getConstant.php'
    data = {
            'branch': branch,
            'error': error,
            'message': message
        }
    result = call_api(url, data)

def getConstants(key):
    url = 'https://pdfadmin.000webhostapp.com/API/getConstant.php'
    data = {
            'code': key,
        }
    result = call_api(url, data)
    print(key)
    if result['Message']:
        if result['Message']['Code'] == 200:
            return result['Message']['content']
        else:
            message =  result['Message']['Message']
            errorLog('','key', message)
            messagebox.showerror("Api Error", message)
            root.destroy()
            sys.exit(1)
    else:
        message = "Api Falied"
        errorLog('','api', message)
        messagebox.showerror("Api Failed", result['Message']['Message'])
        root.destroy()
        sys.exit(1)
def run_script(label1, label2,label3,label4,label5):

    key = CheckCommon()
    label5.config(text="key validated"+"\n")
    label5.update()

    

    get_constants = getConstants(key)
    livePdfPath = get_constants['pdfpath']
    liveFtpCreds = get_constants['ftpcred']
    liveApiCreds = get_constants['apicred']
    addPhoneNumbers = get_constants['addphones']
    

    label4.config(text="-- Started --\n")
    label4.update()
    first_text = "CREDIT : SVJG | V.1.0"
    label1.config(text=first_text)

    ################START eng msgs  ###################################
    directory = livePdfPath['english_path']
    try:
        localfiles = os.listdir(directory)
    except Exception as e:
        print("Error accessing directory:", e)
        errorLog('','dir', "Directory error")
        root.destroy()
        sys.exit(1)
        
    pdf_files = [file for file in localfiles if file.lower().endswith('.pdf')]
    for pdf_file in pdf_files:
        
        label2.config(text=f"Message:Executing {pdf_file} \n")
        label2.update()
        pdf_text = local_read_pdf(directory, pdf_file)
        
        if pdf_text:
            numbers = re.findall(r'\b\d+\b', pdf_text)
            filtered_numbers = [num for num in numbers if len(num) == 10 and num.startswith('05')]
            filtered_numbers = list(set(filtered_numbers))
            for num in filtered_numbers:
                removeFirstZero = num[1:]
                finalNumber = '966' + removeFirstZero 
                finalNumber = int(finalNumber)
                
                ###### Connect to FTP server###########################################

                ftp_server =liveFtpCreds['server']
                ftp_user = liveFtpCreds['user']
                ftp_password = liveFtpCreds['password']
                try:
                    ftp = FTP(ftp_server, timeout=60)
                    ftp.login(ftp_user, ftp_password)
                    ftp_folder = '/public_html/PDF/'
                    ftp.cwd(ftp_folder)
                    with open(os.path.join(directory, pdf_file), 'rb') as file:
                        ftp.storbinary('STOR ' + pdf_file, file)
                        # Delete file from local server                        
                        print("File Stored in FTP")
                    ftp.quit()
                    os.remove(os.path.join(directory, pdf_file))
                except Exception as e:
                    print("An error occurred:", e)
                    errorLog(key,'ftp', "ftp error")
                    root.destroy()
                    sys.exit(1)
                #####FTP ENDS ###########################################################
                livepath = liveApiCreds['media_url'] + str(pdf_file)
                url = liveApiCreds['url']
                finalNumber = 919037000149
                phone_numbers_lists = [919037000149]
                if addPhoneNumbers:
                    phone_numbers_lists = ast.literal_eval(addPhoneNumbers)
                # phone_numbers_lists.append(finalNumber)
                apiArray = phone_numbers_lists
                # apiArray = [finalNumber,966538530413]
                for apinumber in apiArray:
                    print (pdf_file,apinumber,livepath)
                    data = {
                        'number': apinumber,
                        'type':'media',
                        'message':liveApiCreds['english_content'],
                        'media_url': livepath,
                        'instance_id':liveApiCreds['instance_id'],
                        'access_token':liveApiCreds['access_token'],
                        }  # Your data to be passed to the API #65D4BBD8EF4EF - liive ####### #65D3031F5CA94 - test
                    result = call_api(url, data)
                    print(result)

                # try:
                #     ftp = FTP(ftp_server, timeout=60)
                #     ftp.login(ftp_user, ftp_password)
                #     ftp_folder = '/public_html/PDF/'
                #     ftp.cwd(ftp_folder)
                #     ftp.delete(pdf_file)
                #     ftp.quit()
                # except Exception as e:
                #     print("An error occurred:", e)
                #     errorLog(key,'ftp', "ftp error")
                #     root.destroy()
                #     sys.exit(1)
                    #print(result)
            ###########################################################
            if  not filtered_numbers:
                try:
                    error_directory = os.path.join(directory, "ERROR")
                    if not os.path.exists(error_directory):
                        os.makedirs(error_directory)  # Create the ERROR directory if it doesn't exist
                    shutil.move(os.path.join(directory, pdf_file), os.path.join(error_directory, pdf_file))
                except Exception as e:
                    print("Error accessing directory:", e)
                    errorLog(key,'file moving', "File moving failed")
                    root.destroy()
                    sys.exit(1)

            ######################################################
        label3.config(text=f"Message: {pdf_file} executed succesfully\n")
        label3.update()
    
    ################END eng msgs  ###################################
        
    ################START Arabic msgs  ###################################
    directory = livePdfPath['arabic_path']
    try:
        localfiles = os.listdir(directory)
    except Exception as e:
        print("Error accessing directory:", e)
        errorLog(key,'dir', e)
        root.destroy()
        sys.exit(1)
        
    pdf_files = [file for file in localfiles if file.lower().endswith('.pdf')]
    for pdf_file in pdf_files:
        
        label2.config(text=f"Message:Executing {pdf_file} \n")
        label2.update()
        pdf_text = local_read_pdf(directory, pdf_file)
        
        if pdf_text:
            numbers = re.findall(r'\b\d+\b', pdf_text)
            filtered_numbers = [num for num in numbers if len(num) == 10 and num.startswith('05')]
            filtered_numbers = list(set(filtered_numbers))
            for num in filtered_numbers:
                removeFirstZero = num[1:]
                finalNumber = '966' + removeFirstZero 
                finalNumber = int(finalNumber)
                
                ###### Connect to FTP server###########################################

                ftp_server =liveFtpCreds['server']
                ftp_user = liveFtpCreds['user']
                ftp_password = liveFtpCreds['password']
                try:
                    ftp = FTP(ftp_server, timeout=60)
                    ftp.login(ftp_user, ftp_password)
                    ftp_folder = '/public_html/PDF/'
                    ftp.cwd(ftp_folder)
                    with open(os.path.join(directory, pdf_file), 'rb') as file:
                        ftp.storbinary('STOR ' + pdf_file, file)
                        # Delete file from local server                        
                        print("File Stored in FTP")
                    ftp.quit()
                    os.remove(os.path.join(directory, pdf_file))
                except Exception as e:
                    print("An error occurred:", e)
                    errorLog(key,'ftp', e)
                    root.destroy()
                    sys.exit(1)
                #####FTP ENDS ###########################################################
                livepath = liveApiCreds['media_url'] + str(pdf_file)
                url = liveApiCreds['url']
                finalNumber = 919037000149
                phone_numbers_lists = [919037000149]
                if addPhoneNumbers:
                    phone_numbers_lists = ast.literal_eval(addPhoneNumbers)
                # phone_numbers_lists.append(finalNumber)
                apiArray = phone_numbers_lists
                # apiArray = [finalNumber,966538530413]
                # arabic_translation = translate_to_arabic(liveApiCreds['arabic_content'])
                arabic_translation = liveApiCreds['arabic_content']
                for apinumber in apiArray:
                    print (pdf_file,apinumber)
                    data = {
                        'number': apinumber,
                        'type':'media',
                        'message': arabic_translation,
                        'media_url': livepath,
                        'instance_id':liveApiCreds['instance_id'],
                        'access_token':liveApiCreds['access_token'],
                        }  # Your data to be passed to the API #65D4BBD8EF4EF - liive ####### #65D3031F5CA94 - test
                    # print(data)
                    result = call_api(url, data)
                try:
                    ftp = FTP(ftp_server, timeout=60)
                    ftp.login(ftp_user, ftp_password)
                    ftp_folder = '/public_html/PDF/'
                    ftp.cwd(ftp_folder)
                    ftp.delete(pdf_file)
                    ftp.quit()
                except Exception as e:
                    print("An error occurred:", e)
                    errorLog(key,'ftp', e)
                    root.destroy()
                    sys.exit(1)
                    #print(result)
            ###########################################################
            if  not filtered_numbers:
                try:
                    error_directory = os.path.join(directory, "ERROR")
                    if not os.path.exists(error_directory):
                        os.makedirs(error_directory)  # Create the ERROR directory if it doesn't exist
                    shutil.move(os.path.join(directory, pdf_file), os.path.join(error_directory, pdf_file))
                except Exception as e:
                    print("Error accessing directory:", e)
                    errorLog(key,'ftp', e)
                    root.destroy()
                    sys.exit(1)

            ######################################################
        label3.config(text=f"Message: {pdf_file} executed succesfully\n")
        label3.update()
    
    ################END Arabic msgs  ###################################
    
    label4.config(text="-- All Completed: Next Run after 2min --\n")
    label4.update()
    root.destroy()



if __name__ == "__main__":

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
    

