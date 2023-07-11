import subprocess

while True:
    print()
    print("Which operation do you want to perform?")
    print()
    print("\t(0) VOICE")
    print("\t(1) GitHub")
    print("\t(2) Docker")
    print("\t(3) Quit")
    operation = input("Enter your choice [0-3]: ")

    if operation == "0":
        print("Initializing VOICE")
        subprocess.run(["python", "voice_commands.py"])

    elif operation == "1":
        while True:
            print()
            print("Which Git operation do you want to perform?")
            print()
            print(f"GitHub username: {username}")
            print(f"Local repository name: {local_repo}")
            print(f"Remote repository name: {remote}")
            print(f"The default branch you want to work with: {branch}")
            print(f"GPG key value: {GPG}")
            print()
            print("\t(0) Configure (configures the script for continuous use)")
            print("\t(1) Clone")
            print("\t(2) Pull")
            print("\t(3) Push")
            print("\t(4) Generate Patch")
            print("\t(5) Send Email")
            print("\t(6) Return to Main Menu")
            choice = input("Enter your choice [0-6]: ")

            if choice == "0":
                print("Enter the values for future use of the script...")
                print()
                username = input("Enter GitHub username: ")
                local_repo = input("Local repository name: ")
                remote = input("Remote repository name: ")
                branch = input("The default branch you want to work with: ")
                GPG = input("GPG key value: ")

            elif choice == "1":
                print("Cloning from GitHub")
                clone_url = input("Enter the repository https url: ")
                subprocess.run(["git", "clone", clone_url])

            elif choice == "2":
                print("Pulling from GitHub")
                pull_url = input("Enter the repository https url: ")
                print()
                print(pull_url)
                print()
                while True:
                    print("Which type of Git Pull do you want?")
                    print("\t(1) Merge (the default strategy)")
                    print("\t(2) Rebase")
                    print("\t(3) Fast-forward only")
                    print("\t(4) Return to main menu")
                    pull_choice = input("Enter your choice [1-4]: ")

                    if pull_choice == "1":
                        subprocess.run(["git", "config", "pull.rebase", "false"])
                        subprocess.run(["git", "pull", pull_url])

                    elif pull_choice == "2":
                        subprocess.run(["git", "config", "pull.rebase", "true"])
                        subprocess.run(["git", "pull", pull_url])

                    elif pull_choice == "3":
                        subprocess.run(["git", "config", "pull.ff", "only"])
                        subprocess.run(["git", "pull", pull_url])

                    elif pull_choice == "4":
                        break

                    else:
                        print("Invalid operation")

            elif choice == "3":
                print("Pushing to GitHub")
                while True:
                    print("Which type of Git Push do you want?")
                    print("\t(0) LFS (if git lfs is already installed into the system)")
                    print("\t(1) Normal")
                    print("\t(2) Return to main menu")
                    push_choice = input("Enter your choice [0-2]: ")

                    if push_choice == "0":
                        map = {local_repo: remote}

                        subprocess.run(["git", "config", "--global", "user.name", username])
                        subprocess.run(["git", "config", "--global", "user.signingkey", GPG])
                        subprocess.run(["git", "init"])
                        subprocess.run(["git", "lfs", "install"])

                        extension = input("Enter the file extension without dot: ")
                        subprocess.run(["git", "lfs", "track", f"*.{extension}"])
                        subprocess.run(["git", "add", ".gitattributes"])
                        subprocess.run(["git", "add", "."])

                        message = input("Enter Commit message: ")
                        subprocess.run(["git", "commit", "-m", message])

                        tag = input("Enter Tag name (Press enter to skip): ")
                        tag_message = input("Enter Tag message (Press enter to skip): ")
                        if tag:
                            subprocess.run(["git", "tag", "-a", tag, "-m", tag_message])
                        subprocess.run(["git", "tag", "-n"])

                        for i in map:
                            subprocess.run(["git", "remote", "add", i, f"https://github.com/{username}/{map[i]}.git"])
                            subprocess.run(["git", "push", "-u", i, branch])

                        subprocess.run(["git", "push"])

                    elif push_choice == "1":
                        map = {local_repo: remote}

                        subprocess.run(["git", "config", "--global", "user.name", username])
                        subprocess.run(["git", "config", "--global", "user.signingkey", GPG])
                        subprocess.run(["git", "init"])
                        subprocess.run(["git", "add", "."])

                        message = input("Enter Commit message: ")
                        subprocess.run(["git", "commit", "-m", message])

                        tag = input("Enter Tag name (Press enter to skip): ")
                        tag_message = input("Enter Tag message (Press enter to skip): ")
                        if tag:
                            subprocess.run(["git", "tag", "-a", tag, "-m", tag_message])
                        subprocess.run(["git", "tag", "-n"])

                        for i in map:
                            subprocess.run(["git", "remote", "add", i, f"https://github.com/{username}/{map[i]}.git"])
                            subprocess.run(["git", "push", "-u", i, branch])

                        subprocess.run(["git", "push"])

                    elif push_choice == "2":
                        break

                    else:
                        print("Invalid operation")

            elif choice == "4":
                print("Generate Patch")
                fileone = input("Enter file 1: ")
                filetwo = input("Enter file 2: ")
                subprocess.run(["diff", fileone, filetwo, "-staged"])
                file_diff = input("Enter the file name created using diff: ")
                subprocess.run(["git", "patch", file_diff])

            elif choice == "5":
                print("Send Email")
                receiver = input("Enter the receiver: ")
                filename = input("File you want to mail: ")
                subprocess.run(["git", "send-email", f"--to={receiver}", filename])

            elif choice == "6":
                break

            else:
                print("Invalid operation")

    elif operation == "2":
        while True:
            print("Which type of Docker operation do you want to perform?")
            print("\t(0) Login to the Docker Hub Repository")
            print("\t(1) Pull an Image from Docker Hub")
            print("\t(2) Build an Image")
            print("\t(3) Run a Docker Image")
            print("\t(4) Access the running container")
            print("\t(5) Remove a Docker Container")
            print("\t(6) Remove a Docker Image")
            print("\t(7) Push an Image to the Docker Hub Repository")
            print("\t(8) Return to main menu")
            dchoice = input("Enter your choice [0-8]: ")

            if dchoice == "0":
                subprocess.run(["docker", "login"])

            elif dchoice == "1":
                pull_username = input("Enter Username: ")
                image_name = input("Enter Image name: ")
                pull_tag_name = input("Enter tag if specific: ")
                subprocess.run(["docker", "pull", f"{pull_username}/{image_name}:{pull_tag_name}"])

            elif dchoice == "2":
                while True:
                    print("Which docker build do you want?")
                    print("\t(0) Build from working directory")
                    print("\t(1) Build from URL")
                    print("\t(2) Return to main menu")
                    build_choice = input("Enter your choice [0-2]: ")

                    if build_choice == "0":
                        subprocess.run(["docker", "build", "."])

                    elif build_choice == "1":
                        build_url = input("Enter the URL without 'https://': ")
                        subprocess.run(["docker", "build", build_url])

                    elif build_choice == "2":
                        break

                    else:
                        print("Invalid operation")

            elif dchoice == "3":
                run_image = input("Enter image name you want to run: ")
                subprocess.run(["docker", "run", "-it", "-d", run_image])

            elif dchoice == "4":
                subprocess.run(["docker", "login"])

            elif dchoice == "5":
                container_id = input("Enter Container ID to remove: ")
                subprocess.run(["docker", "rm", container_id])

            elif dchoice == "6":
                image_id = input("Enter Image ID to remove: ")
                subprocess.run(["docker", "rmi", image_id])

            elif dchoice == "7":
                subprocess.run(["docker", "login"])
                docker_username = input("Enter Docker username: ")
                push_image_name = input("Enter docker image name you want to push: ")
                subprocess.run(["docker", "push", f"{docker_username}/{push_image_name}"])

            elif dchoice == "8":
                break

            else:
                print("Invalid operation")

    elif operation == "3":
        print("Quitting...")
        break

    else:
        print("Invalid operation")
