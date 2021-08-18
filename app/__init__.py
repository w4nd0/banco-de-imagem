from flask import Flask
from os import environ
from kenzie import image


MAX_CONTENT_LENGTH = eval(environ.get('MAX_CONTENT_LENGTH'))

app = Flask(__name__)


@app.route('/upload', methods=["POST"])
def post_file():
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    return image.upload_file()


@app.route('/files', methods=["GET"])
def list_files():
    return image.get_files()


@app.route('/files/<type>', methods=["GET"])
def list_files_by_type(type):
    return image.get_files_by_type(type)


@app.route('/download/<file_name>', methods=["GET"])
def download(file_name):
    return image.download_filename(file_name)


@app.route('/download-zip', methods=["GET"])
def download_dir_as_zip():
    return image.download_zip()
