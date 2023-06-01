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
import streamlit.components.v1 as stc
import sqlite3

conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()

def create_admin_table():
    c.execute('CREATE TABLE IF NOT EXISTS admintable(username TEXT, email TEXT, password TEXT)')

def edit_admin(new_username,new_email,new_password):
	c.execute("UPDATE admintable SET username =?,email=?,password=? WHERE username=? and email=? and password=? ",(new_username,new_email,new_password))
	conn.commit()
	data = c.fetchall()
	return data

def get_admin(username):
	c.execute('SELECT * FROM admintable WHERE username="{}"'.format(username))
	data = c.fetchall()
	return data

def view_admin():
	c.execute('SELECT * FROM admintable')
	data = c.fetchall()
	return data

def create_user_table():
	c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT,email TEXT,password TEXT,github_username TEXT,github_password TEXT,docker_username TEXT,docker_password TEXT,open_ai_api TEXT,activity TEXT, time TIMESTAMP)')


def add_user(username,email,password,github_username,github_password,docker_username,docker_password,open_ai_api,activity, time):
	c.execute('INSERT INTO usertable(username,email,password,github_username,github_password,docker_username,docker_password,open_ai_api,activity,time) VALUES (?,?,?,?,?,?,?,?,?,?)',(username,email,password,github_username,github_password,docker_username,docker_password,open_ai_api,activity,time))
	conn.commit()


def view_all_user():
	c.execute('SELECT username AND email AND github_username AND docker_username AND time FROM usertable')
	data = c.fetchall()
	return data

def view_all_user_activity():
	c.execute('SELECT DISTINCT username AND activity AND time FROM usertable')
	data = c.fetchall()
	return data

def get_task(task):
	c.execute('SELECT * FROM taskstable WHERE task="{}"'.format(task))
	data = c.fetchall()
	return data

def get_task_by_status(task_status):
	c.execute('SELECT * FROM taskstable WHERE task_status="{}"'.format(task_status))
	data = c.fetchall()


def edit_task_data(new_task,new_task_status,new_task_date,task,task_status,task_due_date):
	c.execute("UPDATE taskstable SET task =?,task_status=?,task_due_date=? WHERE task=? and task_status=? and task_due_date=? ",(new_task,new_task_status,new_task_date,task,task_status,task_due_date))
	conn.commit()
	data = c.fetchall()
	return data

def delete_data(task):
	c.execute('DELETE FROM taskstable WHERE task="{}"'.format(task))
	conn.commit()

openai.api_key = ""

HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Dev-Automation-Script(dash)</h1>
    <p style="color:white;text-align:center;">Automate Development</p>
    </div>
    """

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

    stc.html(HTML_BANNER)

    #image = Image.open('logo.png')

    #st.image(image, use_column_width=True)

    menu = ["Intro", "Admin Panel", "Sign-Up", "Sign-In"]
    choice = st.sidebar.selectbox("Select Activity", menu)
    if choice == "Intro":
        st.subheader("Intro")

    elif choice == "Admin Panel":
        st.subheader("Admin Panel")
        menu = ["Edit Admin Details", "View User", "Delete User"]
        choice = st.sidebar.selectbox("Select Activity", menu)
        if choice == "Edit Admin Details":
            create_admin_table()
            st.subheader("Edit Admin Details")
            with st.expander("Current Details"):
                result = view_admin()
                # st.write(result)
                clean_df = pd.DataFrame(result,columns=["username","email"])
                st.dataframe(clean_df)
            new_username = st.text_input("Enter new username")
            new_email = st.text_input("Enter new email-address")
            new_password = st.text_input("Enter new password")
            if st.button("Update Admin Credentials"):
                edit_admin(new_username,new_email,new_password)
                st.success("Updated ::To {}".format(new_username))

            elif choice == "View User":
                with st.expander("View All"):
                    create_user_table()
                    result = view_all_user()
			        # st.write(result)
                    clean_df = pd.DataFrame(result,columns=["username","email","github_username","docker_username","time"])
                    st.dataframe(clean_df)

                with st.expander("User Status"):
                    task_df = clean_df["username", "email", "time"].value_counts().to_frame()
			        # st.dataframe(task_df)
                    task_df = task_df.reset_index()
                    st.dataframe(task_df)

                    p1 = px.pie(task_df,names='index',values='Status')
                    st.plotly_chart(p1,use_container_width=True)

        elif choice == "Delete User":
            st.subheader("Delete User")
            with st.expander("View User"):
                result = view_all_user()
                # st.write(result)
                clean_df = pd.DataFrame(result,columns=["username","email","github_username","docker_username","time"])
                st.dataframe(clean_df)

            unique_list = [i[0] for i in view_all_user()]
            delete_by_user_name =  st.selectbox("Select User",unique_list)
            if st.button("Delete"):
                delete_data(delete_by_user_name)
                st.warning("Deleted: '{}'".format(delete_by_user_name))

            with st.expander("Updated User"):
                result = view_all_user()
                # st.write(result)
                clean_df = pd.DataFrame(result,columns=["username","email","github_username","docker_username","time"])
                st.dataframe(clean_df)

    elif choice == "Sign-Up":
        st.subheader("Sign-Up using credentials")

    elif choice == "Sign-In":

        menu = ["Intro", "Directory Visualizer", "GitHub", "Generate Patch", "Send-Mail", "Docker", "E.T.E.R.GPT"]
        choice = st.sidebar.selectbox("Select Activity", menu)
        if choice == "Intro":
            st.subheader("Intro")

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

