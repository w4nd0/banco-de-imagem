import os
from os import environ
from environs import Env

env = Env()
env.read_env()

FILES_DIRECTORY = environ.get('FILES_DIRECTORY')

if not os.path.exists(FILES_DIRECTORY):
    os.system("/bin/bash -c 'mkdir -p image_bank/{jpeg,png,gif}'")
