import os
from os import environ

FILES_DIRECTORY = environ.get('FILES_DIRECTORY')

if not os.path.exists(FILES_DIRECTORY):
    os.system("/bin/bash -c 'mkdir -p image_bank/{jpeg,png,gif}'")
