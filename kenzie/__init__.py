import os

create_folder = os.system('ls | grep -q upload')
if create_folder:
    os.mkdir('upload/')
    os.system("/bin/bash -c 'mkdir -p image_bank/{jpg,png,gif}'")
