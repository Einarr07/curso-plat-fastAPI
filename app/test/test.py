from starlette.testclient import TestClient


def test_client(client):
    assert isinstance(client, TestClient)
