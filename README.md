![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white) ![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
# Dev-Automation-Script

A successor to Git-Automation-Script.
A script for every developer build to automate work with Git and Docker.

Script to automate Git and Docker from project working directory with a menu to choose from, you just have configure once and the script can be used for the following operations.

```
Which operation you want to perform ?"
(0) VOICE
(1) GitHub
(2) Docker
(3) Quit
Enter your choice [0-3]:

```
#GitHub

```
Which Git operations you want to perform ?
(0) Configure (configures the script for continuous uses)
(1) Clone
(2) Pull
(3) Push
```

```
Which type of Git Push you want ?
LFS (if git lfs is already installed into the system)
Normal
Return to main menu
Enter your choice [0-2]:

```
```
(4) Generate Patch
(5) Send Email
(6) VOICE
(7) Exit
Enter your choice [0-7]:
```

# Docker

```

Which type of Docker operation you want to perform ?

(0) Login to the Docker Hub Repository
(1) Pull an Image from Docker Hub
(2) Build an Image
(3) Run a Docker Image
(4) Access the running container
(5) Remove a Docker Container
(6) Remove a Docker Image
(7) Push an Image to the docker hub repository
(8) Return to main menu
Enter your choice [0-8]:

```

# About

* Use the script **"dash.sh"** file inside your project working directory to automate git procedures by **just configuring the script once and use it any number of times.** 
* You just have to use the configure option once and if you wish to change the working directory you just have to use the configure option to start working with the new project.

* Just give the file write access and use the script by running:

```
$./dash.sh
```

# For Windows User

* Use the Windows Subsystem for Linux (WSL) with a valid linux distribution and run the following command in the terminal

```
wsl
```
* Then run the following command and press Y

```
$sudo apt install git
```

# How prepare the file

Use the file as super user or admin acces and provide the file with write access by :
```
$ chmod +x dash.sh
```
inside the terminal, in the project working directory.

# How to use the script

Keep working on project files and run :
``` 
$ ./dash.sh
```
in the project working directory's terminal, while the **"dash.sh"** file is present and provided with **write access** and you will be able to handle your project files with git operations using a simple menu driven approach.

