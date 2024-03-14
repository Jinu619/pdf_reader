

import os
import sys
import requests
import PyPDF2
import re
from ftplib import FTP
import tkinter as tk
import shutil
from tkinter import messagebox
import ast

ftp_server ='ftpupload.net'
ftp_user = 'if0_36159057'
ftp_password = 'w6oqyTRMMZ'
try:
    ftp = FTP(ftp_server, timeout=60)
    ftp.login(ftp_user, ftp_password)
    directory = "D:\\2024\\PDF\\"
    pdf_file = "BDB-S-123189.PDF"
    with open(os.path.join(directory, pdf_file), 'rb') as file:
        ftp.mkd('/PDF/')
        ftp.cwd('/PDF/')
        ftp.storbinary('STOR ' + pdf_file, file)                   
        print("FTP Connected")
    ftp.quit()
except Exception as e:
    print("An error occurred:", e)