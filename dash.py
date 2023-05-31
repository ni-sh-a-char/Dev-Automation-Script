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
import tkinter as tk
from tkinter import filedialog
import os
from tkinter import ttk
import seedir as sd
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from time import sleep
import subprocess
import openai

openai.api_key = ""

def chat_with_chatgpt(prompt, model="gpt-3.5-turbo"):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

def main():

    #image = Image.open('logo.png')

    #st.image(image, use_column_width=True)

    st.title("Dev-Automation-Script(dash)")

    menu = ["Intro","Directory Visualizer", "GitHub", "Generate Patch", "Send-Mail", "Docker", "E.T.E.R.GPT"]
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

    elif choice == "GitHub":
        st.subheader == "Work with Github"
        menu = ["Clone From GitHub","Pull from GitHub", "Push to GitHub"]
        choice = st.sidebar.selectbox("Select Activity", menu)
        if choice == "Clone From GitHub":
            st.subheader("Please select a destination to Clone")
            root = tk.Tk()
            root.withdraw()
        # Make folder picker dialog appear on top of other windows
            root.wm_attributes('-topmost', 1)
        # Folder picker button
            clone_url = st.text_input('Github URL')
            clone = st.button("Select destination and start cloning")
            if clone:
                dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
                os.chdir(dirname)
                process = subprocess.Popen (['git', 'clone', clone_url],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                result = process.communicate( )
                st.write(result)
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
                    
        elif choice == "Pull from GitHub":
            st.subheader("Pull from GitHub")
            root = tk.Tk()
            root.withdraw()
        # Make folder picker dialog appear on top of other windows
            root.wm_attributes('-topmost', 1)
        # Folder picker button

            pull_url = st.text_input("Enter the Pull URL you want to fetch")
            menu = ["Merge (the default strategy)","Rebase", "Fast-forward only"]
            choice = st.selectbox("Select Activity", menu)
            if choice == "Merge (the default strategy)":
                pull_select = st.button("Select Destination to pull")
                if pull_select:
                    dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
                    os.chdir(dirname)
                    process = subprocess.Popen (['git', 'config', 'pull.rebase', 'false'],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    result = process.communicate( )
                    st.write(result)
                    process = subprocess.Popen (['git', 'pull', pull_url],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    result = process.communicate( )
                    st.write(result)
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

            elif choice == "Rebase":
                pull_select = st.button("Select Destination to pull")
                if pull_select:
                    dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
                    os.chdir(dirname)
                    process = subprocess.Popen (['git', 'config', 'pull.rebase', 'true'],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    result = process.communicate( )
                    st.write(result)
                    process = subprocess.Popen (['git', 'pull', pull_url],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    result = process.communicate( )
                    st.write(result)
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

            elif choice == "Fast-forward only":
                pull_select = st.button("Select Destination to pull")
                if pull_select:
                    dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
                    os.chdir(dirname)
                    process = subprocess.Popen (['git', 'config', 'pull.ff', 'only'],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    result = process.communicate( )
                    st.write(result)
                    process = subprocess.Popen (['git', 'pull', pull_url],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    result = process.communicate( )
                    st.write(result)
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
                

        elif choice == "Push to GitHub":
            st.subheader("Push to GitHub")
            # Set up tkinter
            root = tk.Tk()
            root.withdraw()
            # Make folder picker dialog appear on top of other windows
            root.wm_attributes('-topmost', 1)
            # Folder picker button
            commit_message = st.text_input("Enter commit message")
            push = st.button('Select Destination to Push')
            if push:
                dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
                process = subprocess.Popen (['git', 'init'],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                result = process.communicate( )
                st.write(result)
                process = subprocess.Popen (['git', 'add', '.'],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                result = process.communicate( )
                st.write(result)
                process = subprocess.Popen (['git', 'commit', '-m', commit_message],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                result = process.communicate( )
                st.write(result)
                process = subprocess.Popen (['git', 'push'],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                result = process.communicate( )
                st.write(result)
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


    elif choice == "Send-Mail":
        st.subheader("Send-Mail")
        select = st.button("Choose Directory")
        if select:
            root = tk.Tk()
            root.withdraw()
            # Make folder picker dialog appear on top of other windows
            root.wm_attributes('-topmost', 1)
            # Folder picker button
            dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
            # dirname = os.getcwd()
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
        send = st.button('Send')
        if send:
            process = subprocess.Popen (['git', 'send-email', '--to=', receiver, filename ],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            result = process.communicate( )
            st.write(result)
        
    elif choice == "Generate Patch":
        st.subheader("Generate Patch")
        select = st.button("Select Destination")
        if select:
            # Set up tkinter
            root = tk.Tk()
            root.withdraw()
            # Make folder picker dialog appear on top of other windows
            root.wm_attributes('-topmost', 1)
            # Folder picker button
            dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
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
        root = tk.Tk()
        root.withdraw()

        # Make folder picker dialog appear on top of other windows
        root.wm_attributes('-topmost', 1)

        # Folder picker button
        clicked = st.button("View Files")
        if clicked:
            dirname = os.getcwd()
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
            click = st.button("Docker Build")
            if click:
                process = subprocess.Popen (['docker','build', '.'],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                result = process.communicate( )
                st.write(result)

    elif choice == "E.T.E.R.GPT":
        st.title("E.T.E.R.GPT")
        st.subheader("Create Code With GPT")
        user_prompt = st.text_area("Enter Your Query")
        click = st.button("Generate Response")
        if click:
            chatbot_response = chat_with_chatgpt(user_prompt)
            st.write(chatbot_response)    
        

if __name__ == '__main__':
    main()