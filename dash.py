from calendar import different_locale
from mimetypes import init
import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
from PIL import Image
import numpy as np # np mean, np random 
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts
import streamlit as st
import tkinter as tk
from tkinter import filedialog
import os
from tkinter import ttk
import seedir as sd
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from time import sleep
import streamlit as st
import subprocess 

def main():

    #image = Image.open('logo.png')

    #st.image(image, use_column_width=True)

    st.title("Dev-Automation-Script(dash)")

    menu = ["Intro","Directory Visualizer","Clone from GitHub", "Generate Patch", "Send-Mail", "Docker"]
    choice = st.sidebar.selectbox("Select Activity", menu)
    if choice == "Intro":
        st.subheader("Automate Development")

    elif choice == "Directory Visualizer":
        # Set up tkinter
        root = tk.Tk()
        root.withdraw()

        # Make folder picker dialog appear on top of other windows
        root.wm_attributes('-topmost', 1)

        # Folder picker button
        st.title('Folder Picker')
        st.write('Please select a folder:')
        clicked = st.button('Folder Picker')
        if clicked:
            dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
            #entries = os.listdir('C:/Users/Piyush Mishra/Documents/Blogs')
            #for entry in entries:
            #   st.write(entry)
            @contextmanager
            def st_capture(output_func):
                with StringIO() as stdout, redirect_stdout(stdout):
                    old_write = stdout.write

                    def new_write(string):
                        ret = old_write(string)
                        output_func(stdout.getvalue())
                        return ret
                    
                    stdout.write = new_write
                    yield


            output = st.empty()
            with st_capture(output.code):
                print(sd.seedir(dirname, style='emoji'))

    elif choice == "Clone from GitHub":
       # root = tk.Tk()
       # root.withdraw()
       # root.wm_attributes('-topmost', 1)
        st.subheader("Clone from GitHub")
        st.write('Please select a destination to clone the repo into:')
        clone_url = st.text_input('Github URL')
        clicked = st.button('Start Cloning')
        if clicked:
            process = subprocess.Popen (['git', 'clone', clone_url],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            result = process.communicate( )
            st.write(result)
        

    elif choice == "Send-Mail":
        st.subheader("Send-Mail")
        # Set up tkinter
        root = tk.Tk()
        root.withdraw()

        # Make folder picker dialog appear on top of other windows
        root.wm_attributes('-topmost', 1)

        # Folder picker button
        clicked = st.button('View')
        if clicked:
            dirname = os.getcwd()
            #entries = os.listdir('C:/Users/Piyush Mishra/Documents/Blogs')
            #for entry in entries:
            #   st.write(entry)
            @contextmanager
            def st_capture(output_func):
                with StringIO() as stdout, redirect_stdout(stdout):
                    old_write = stdout.write

                    def new_write(string):
                        ret = old_write(string)
                        output_func(stdout.getvalue())
                        return ret
                    
                    stdout.write = new_write
                    yield


            output = st.empty()
            with st_capture(output.code):
                print(sd.seedir(dirname, style='emoji'))
            receiver = st.text_input('Enter the receiver mail address')
            filename = st.text_input('Enter First file name')
            clicked = st.button('Send')
            if clicked:
                process = subprocess.Popen (['git', 'send-email', '--to=', receiver, filename ],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                result = process.communicate( )
                st.write(result)
        
    elif choice == "Generate Patch":
        st.subheader("Generate Patch")
        # Set up tkinter
        root = tk.Tk()
        root.withdraw()

        # Make folder picker dialog appear on top of other windows
        root.wm_attributes('-topmost', 1)

        # Folder picker button
        clicked = st.button('View')
        if clicked:
            dirname = os.getcwd()
            #entries = os.listdir('C:/Users/Piyush Mishra/Documents/Blogs')
            #for entry in entries:
            #   st.write(entry)
            @contextmanager
            def st_capture(output_func):
                with StringIO() as stdout, redirect_stdout(stdout):
                    old_write = stdout.write

                    def new_write(string):
                        ret = old_write(string)
                        output_func(stdout.getvalue())
                        return ret
                    
                    stdout.write = new_write
                    yield


            output = st.empty()
            with st_capture(output.code):
                print(sd.seedir(dirname, style='emoji'))

            filename1 = st.text_input('Enter First file name')
            filename2 = st.text_input('Enter Second file name')
            click1 = st.button('Get Diff')
            if click1:
                process = subprocess.Popen (['diff', filename1, filename2, '-staged'],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                result = process.communicate( )
                st.write(result)

            filename3 = st.text_input('Enter File name you want to generate patch for')
            click2 = st.button('Generate Patch')
            if click2:
                process = subprocess.Popen (['git', 'patch', filename3],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                result = process.communicate( )
                st.write(result)

    elif choice == "Docker":
        st.subheader("Docker")
        

if __name__ == '__main__':
    main()