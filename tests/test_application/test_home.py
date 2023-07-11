def test_home(test_client):
    response = test_client.get("/")

    assert response.status_code == 200
    assert b"This is the home page" in response.data


def test_status(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
