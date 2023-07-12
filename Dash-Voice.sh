#!/bin/bash

### Dev Automation Script for automating git and docker ###
### Created by PIYUSH-MISHRA-00 ###

# Install SoX and CMU Sphinx
sudo apt-get install sox
sudo apt-get install pocketsphinx

# Function to process voice command
process_voice_command() {
    echo "Processing voice command: $1"
    # Add your logic to handle the voice command here
}

# Record audio using microphone
record_audio() {
    # Set the audio file path
    audio_file="audio.wav"

    # Use rec command from SoX to record audio from the default microphone
    rec -q -c 1 -r 16000 "$audio_file" silence 1 0.1 5% 1 1.5 5%

    # Process the recorded audio file
    process_audio "$audio_file"
}

# Process the recorded audio file
process_audio() {
    # Use pocketsphinx_continuous command for speech recognition
    command=$(pocketsphinx_continuous -infile "$1" 2>/dev/null)

    # Process the recognized command
    process_voice_command "$command"
}

while :
do
    echo
    echo "Which operation do you want to perform?"
    echo
    echo -e "\t(0) Voice Command"
    echo -e "\t(1) GitHub"
    echo -e "\t(2) Docker"
    echo -e "\t(3) Quit"
    echo -n "Enter your choice [0-3]: "

    read operation
    export operation

    case $operation in
        0) echo "Recording voice command..."
           record_audio
           ;;
        1) while :
           do
               echo
               echo "Which Git operation do you want to perform?"
               echo
               echo "GitHub username: $username"
               echo "Local repository name: $local_repo"
               echo "Remote repository name: $remote"
               echo "The default branch you want to work with: $branch"
               echo "GPG key value: $GPG"
               echo
               echo -e "\t(0) Configure (configures the script for continuous use)"
               echo -e "\t(1) Clone"
               echo -e "\t(2) Pull"
               echo -e "\t(3) Push"
               echo -e "\t(4) Generate Patch"
               echo -e "\t(5) Send Email"
               echo -e "\t(6) Return to Main Menu"
               echo -n "Enter your choice [0-6]: "
               read choice

               case $choice in
                   0) echo "Enter the values for future use of the script..."
                      echo
                      echo "Enter GitHub username: "
                      read username
                      export username
                      echo "Your username is: $username"
                      echo
                      echo "Local repository name: "
                      read local_repo
                      export local_repo
                      echo "Your local repository name is: $local_repo"
                      echo
                      echo "Remote repository name: "
                      read remote
                      export remote
                      echo "Remote repository name is: $remote"
                      echo
                      echo "The default branch you want to work with: "
                      read branch
                      export branch
                      echo "The default branch you want to work with: $branch"
                      echo
                      echo "GPG key value is: $GPG"
                      echo
                      echo "GPG key id for signed commits (leave blank if you don't want signed commits)"
                      read GPG
                      export GPG
                      echo "GPG key value is: $GPG"
                      echo
                      ;;
                   1) echo "Cloning from GitHub"
                      echo
                      echo "Enter the repository https url: "
                      read clone_url
                      git clone "$clone_url"
                      ;;
                   2) echo "Pulling from GitHub"
                      echo
                      echo "Enter the repository https url: "
                      read pull_url
                      echo
                      echo "$pull_url"
                      echo
                      while :
                      do
                          echo "Which type of Git Pull do you want?"
                          echo -e "\t(1) Merge (the default strategy)"
                          echo -e "\t(2) Rebase"
                          echo -e "\t(3) Fast-forward only"
                          echo -e "\t(4) Return to main menu"
                          echo -n "Enter your choice [1-4]: "
                          read pull_choice
                          case $pull_choice in
                              1) git config pull.rebase false
                                 git pull "$pull_url"
                                 ;;
                              2) git config pull.rebase true
                                 git pull "$pull_url"
                                 ;;
                              3) git config pull.ff only
                                 git pull "$pull_url"
                                 ;;
                              4) break
                                 ;;
                              *) echo "Invalid operation"
                                 ;;
                          esac
                      done
                      ;;
                   3) echo "Pushing to GitHub"
                      echo
                      while :
                      do
                          echo "Which type of Git Push do you want?"
                          echo -e "\t(0) LFS (if git lfs is already installed into the system)"
                          echo -e "\t(1) Normal"
                          echo -e "\t(2) Return to main menu"
                          echo -n "Enter your choice [0-2]: "
                          read push_choice
                          case $push_choice in
                              0) declare -A map
                                 map[$local_repo]="$remote"
                                 git config --global user.name "$username"
                                 git config --global user.signingkey "$GPG"
                                 git init
                                 git lfs install
                                 echo
                                 echo "Enter the file extension without dot"
                                 read extension
                                 export extension
                                 git lfs track "*.$extension"
                                 git add .gitattributes
                                 git add .
                                 echo "Enter Commit message: "
                                 read message
                                 git commit -m "$message"
                                 echo "Enter Tag name: (Press enter if you want to skip the tag name)"
                                 read tag
                                 echo "Enter Tag message: (Press enter if you want to skip the tag message)"
                                 read tag_message
                                 git tag -a "$tag" -m "$tag_message"
                                 git tag -n
                                 for i in "${!map[@]}"
                                 do
                                     git remote add "$i" "https://github.com/$username/${map[$i]}.git"
                                     git push -u "$i" "$branch"
                                 done
                                 git push
                                 ;;
                              1) declare -A map
                                 map[$local_repo]="$remote"
                                 git config --global user.name "$username"
                                 git config --global user.signingkey "$GPG"
                                 git init
                                 git add .
                                 echo "Enter Commit message: "
                                 read message
                                 git commit -m "$message"
                                 echo "Enter Tag name: (Press enter if you want to skip the tag name)"
                                 read tag
                                 echo "Enter Tag message: (Press enter if you want to skip the tag message)"
                                 read tag_message
                                 git tag -a "$tag" -m "$tag_message"
                                 git tag -n
                                 for i in "${!map[@]}"
                                 do
                                     git remote add "$i" "https://github.com/$username/${map[$i]}.git"
                                     git push -u "$i" "$branch"
                                 done
                                 git push
                                 ;;
                              2) break
                                 ;;
                              *) echo "Invalid operation"
                                 ;;
                          esac
                      done
                      ;;
                   4) echo "Generate Patch"
                      echo "Enter file 1"
                      read fileone
                      export fileone
                      echo "Enter file 2"
                      read filetwo
                      export filetwo
                      diff "$fileone" "$filetwo" --staged
                      echo "Enter the file name created using diff"
                      read file_diff
                      export file_diff
                      git patch "$file_diff"
                      ;;
                   5) echo "Send Email"
                      echo "Enter the receiver: "
                      read receiver
                      echo "File you want to mail: "
                      read filename
                      git send-email --to="$receiver" "$filename"
                      ;;
                   6) break
                      ;;
                   *) echo "Invalid operation"
                      ;;
               esac
           done
           ;;
        2) while :
           do
               echo "Which type of Docker operation do you want to perform?"
               echo -e "\t(0) Login to the Docker Hub Repository"
               echo -e "\t(1) Pull an Image from Docker Hub"
               echo -e "\t(2) Build an Image"
               echo -e "\t(3) Run a Docker Image"
               echo -e "\t(4) Access the running container"
               echo -e "\t(5) Remove a Docker Container"
               echo -e "\t(6) Remove a Docker Image"
               echo -e "\t(7) Push an Image to the Docker Hub Repository"
               echo -e "\t(8) Return to main menu"
               echo -n "Enter your choice [0-8]: "
               read dchoice
               case $dchoice in
                   0) docker login
                      ;;
                   1) echo "Enter Username: "
                      read pull_username
                      export pull_username
                      echo "Enter Image name: "
                      read image_name
                      export image_name
                      echo "Enter tag if specific: "
                      read pull_tag_name
                      export pull_tag_name
                      docker pull "$pull_username/$image_name:$pull_tag_name"
                      ;;
                   2) while :
                      do
                          echo "Which docker build option do you want?"
                          echo -e "\t(0) Build from working directory"
                          echo -e "\t(1) Build from URL"
                          echo -e "\t(2) Return to main menu"
                          echo -n "Enter your choice [0-2]: "
                          read build_choice
                          export build_choice
                          case $build_choice in
                              0) docker build .
                                 ;;
                              1) echo "Enter the URL without 'https://'"
                                 read build_url
                                 export build_url
                                 docker build "$build_url"
                                 ;;
                              2) break
                                 ;;
                              *) echo "Invalid operation"
                                 ;;
                          esac
                      done
                      ;;
                   3) echo "Enter image name you want to run: "
                      read run_image
                      export run_image
                      docker run -it -d "$run_image"
                      ;;
                   4) docker login
                      ;;
                   5) echo "Enter Container ID to remove: "
                      read container_id
                      export container_id
                      docker rm "$container_id"
                      ;;
                   6) echo "Enter Image ID to remove: "
                      read image_id
                      export image_id
                      docker rmi "$image_id"
                      ;;
                   7) docker login
                      echo "Enter Docker username: "
                      read docker_username
                      export docker_username
                      echo "Enter docker image name you want to push: "
                      read push_image_name
                      export push_image_name
                      docker push "$docker_username/$push_image_name"
                      ;;
                   8) break
                      ;;
                   *) echo "Invalid operation"
                      ;;
               esac
           done
           ;;
        3) echo "Quitting..."
           exit
           ;;
        *) echo "Invalid operation"
           ;;
    esac
done