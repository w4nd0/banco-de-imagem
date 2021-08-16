from flask import Flask, request, jsonify, send_from_directory
from environs import Env
from os import environ
import os
from urllib.error import HTTPError

env = Env()
env.read_env()

FILES_DIRECTORY = environ.get('FILES_DIRECTORY')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'gif'}

app = Flask(__name__)

def upload_file():
    """Faz o upload da image verificando: o tamanho máximo (1MB), a extensão (JPG, PNG e GIF)
     e a existencia de uma imagem a ser enviada.

    Returns:
        dict: Retorna uma mensagem de sucesso caso o envio seja realizado, juntamente com código
        de status de resposta.
    """
    try:
        key_file_name = list(request.files.keys())[0]
        img = request.files[key_file_name] 
        name_file = img.filename.replace(' ', '_')
        list_upload = os.listdir('upload/') 
        
        if name_file in list_upload:
            raise FileExistsError

        if img.content_type.split('/')[1] in ALLOWED_EXTENSIONS:
            img.save(f"upload/{name_file}")
            return {"message": "Upload realizado com sucesso!"}, 201
        else:
            raise TypeError

    except IndexError:
        return {"message": "Selecione um arquivo para o upload"}, 418

    except TypeError:
        return {"message": "Formato não suportado"}, 415

    except FileExistsError:
        return {"message": "Arquivo já se encontra no banco de imagens"}, 409

def get_files():
    """Faz uma requisição para receber uma lista com todas as imagens contidos no banco de imagem.

    Returns:
        tuple: Retorna uma lista com todas as imagens na pasta image_bank, juntamente com código
        de status de resposta.
    """
    files = [filenames for _, _, filenames in os.walk(f'{FILES_DIRECTORY}')]
    flat_list = [item for sublist in files for item in sublist]
    dict_list = {}
    dict_list['files'] = flat_list
    return jsonify(dict_list), 200



def get_files_by_type(type):
    """Faz uma requisição para receber uma lista com todas as imagens com a extensão solicitada 
    pelo usuário.

    Args: 
        type (str): O tipo de extensão solicitada pelo usuário.

    Returns:
        tuple: Retorna uma lista com todas as imagens na pasta image_bank que são da extensão solicitada
        pelo usuário (no caso da extensão existir no bando), juntamente com código de status de resposta.
    """    
    try:
        files = os.listdir(f"{FILES_DIRECTORY}{type}")
        dict_list = {}
        dict_list[type] = files
        return jsonify(dict_list), 200
    except FileNotFoundError:
        return {"message": f"Opção de extensão {type} não existente"}, 404

def download_filename(file_name):
    """Baixa a imagem solicitada pelo usuário.

    Args: 
        file_name (str): O nome da imagem solicitada pelo usuário.

     Returns:
        tuple: Caso encontrada retorna a imagem solicitada, juntamente com código de status de resposta.
    """   
    try:
        return send_from_directory(directory=f"../{FILES_DIRECTORY}{file_name.split('.')[1]}", path=file_name, as_attachment=True), 200   
    except Exception:
        return {"message": "Arquivo não existente"}, 404

def download_zip():
    """Baixa um arquivo zip com todas as imagens com a extensão passada pelo usuario

    Returns:
        tuple: Caso encontrado retorna o arquivo zipado solicitado, juntamente com código
         de status de resposta.
    """  
    file_type = request.args.get("file_type")
    compression_rate = request.args.get("compression_rate" , 6)

    try:
        files = os.listdir(f'./{FILES_DIRECTORY}{file_type}/')
        if len(files) == 0:
            raise FileNotFoundError

        os.system(f"zip -{compression_rate} -r /tmp/files.zip ./{FILES_DIRECTORY}{file_type}/*")

        return send_from_directory(directory='/tmp', path='files.zip', as_attachment=True), 200

    except FileNotFoundError:
        return {"message": "Não existem imagens com a extensão solicitada"}, 404