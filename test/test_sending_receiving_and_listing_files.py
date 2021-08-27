from app import app
import filecmp


def app_client():
    return app.test_client()


def test_file_upload_using_form_return_status_code_201_if_success():
    from werkzeug.datastructures import FileStorage
    client = app_client()

    FILE_PATH = './test/upload_test/kenzie.gif'
    with open(FILE_PATH, 'rb') as file:
        my_file = FileStorage(stream=file, filename='test.gif', content_type='image/gif')

        response = client.post('/upload', data={"files": my_file}, content_type="multipart/form-data")

        assert response.status_code == 201


def test_list_all_files():
    client = app_client()
    response = client.get("/files")
    except_response = {'files': ['test.gif']}
    assert response.get_json() == except_response, "Retorno incorreto"


def test_list_files_by_type():
    client = app_client()
    response = client.get("/files/gif")
    except_response = {'gif': ['test.gif']}
    assert response.get_json() == except_response, "Retorno incorreto"


def test_request_file_download():
    client = app_client()
    response = client.get("/download/test.gif")
    with open('./test/download_test/test.gif', 'wb') as f:
        f.write(response.data)
    file_was_downloaded = filecmp.cmp('./test/download_test/test.gif', './test/upload_test/kenzie.gif')

    assert response.status_code == 200, 'Download falhou'
    assert file_was_downloaded, 'Download falhou'


def test_request_type_zipfiles_download():
    client = app_client()

    response = client.get("/download-zip?file_type=gif")
    with open('./test/download_test/test.zip', 'wb') as f:
        f.write(response.data)
    
    assert response.status_code == 200
