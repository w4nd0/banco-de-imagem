from app import app


def app_client():
    return app.test_client()


def test_request_wrong_filename_download():
    client = app_client()

    response = client.get("/download/fail.gif")
    
    assert response.status_code == 404


def test_request_no_files_of_the_type_to_download():
    client = app_client()

    response = client.get("/download-zip?file_type=png")
    
    assert response.status_code == 404
