from app import app


def app_client():
    return app.test_client()


def test_app_accepts_post_request():
    client = app_client()
    assert 'POST' in (client.options('/upload').headers['Allow'])


def test_app_accepts_get_files_request():
    client = app_client()
    assert 'GET' in (client.options('/files').headers['Allow'])


def test_app_accepts_get_files_by_type_request():
    client = app_client()
    assert 'GET' in (client.options('/files/gif').headers['Allow'])
