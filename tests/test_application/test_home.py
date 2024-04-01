def test_home(test_client):
    response = test_client.get("/")

    assert response.status_code == 200
    assert b"ALeRT | Grammar property visualiser" in response.data
    assert b"1. About ALeRT" in response.data
    assert b"Enter Your Grammar" in response.data


def test_status(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
