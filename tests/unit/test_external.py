from services.backend import external
import requests, json

def test_get_user_by_username_with_mock(mocker):
    mock_response = {
        "success": True,
        "user": {
            "_id": "662267f220fd1597273f9e55",
            "name": "Erwin Smith",
            "projects": [],
            "role": "project_manager",
            "username": "U06UFU55YBX"
        }
    }
    mocker.patch(
        "services.backend.request.requests.get"
    ).return_value.json.return_value = mock_response
    response = external.get_user_by_username('U06UFU55YBX')
    requests.get.assert_called_once_with(
        "http://3.139.127.119:5000/user/U06UFU55YBX", data='{}', headers={'Accept': '*/*', 'Content-Type': 'application/json'}, params={}
    )
    assert (
        response == mock_response
    )

def test_register_user_with_mock(mocker):
    mock_response = {
        "success": True,
        "user_id": "123123123"
    }
    mocker.patch(
        "services.backend.request.requests.post"
    ).return_value.json.return_value = mock_response
    payload = {
        "username": "MockUserName",
        "password": "testuser1",
        "name": "Mock User",
        "role": "qa",
        "projects": []
    }
    response = external.register_user(payload)
    requests.post.assert_called_once_with(
        "http://3.139.127.119:5000/user/register", data=json.dumps(payload), headers={'Accept': '*/*', 'Content-Type': 'application/json'}
    )
    assert (
        response == mock_response
    )