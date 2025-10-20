from fastapi.testclient import TestClient
import main
from fastapi import status

client = TestClient(main.app)

def test_return_health_check():
    response = client.get("/healthy/")
    assert  response.status_code == status.HTTP_200_OK
    assert  response.json() == {'status':'Healthy'}

def get_auth_header():
    response = client.post("/auth/user/login",data={'username':'kayrabk','password':'k123k'})
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_todo_by_id():
    headers = get_auth_header()
    response = client.get("/todos/todo/999",headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'Todo Not Found'}