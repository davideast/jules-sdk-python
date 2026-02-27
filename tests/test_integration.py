import pytest
from httpx import Response
from jules.models import SessionState

def test_create_session(client, mock_api):
    mock_api.post("/sessions").mock(return_value=Response(200, json={
        "name": "sessions/123",
        "state": "CREATED",
        "createTime": "2023-10-26T12:00:00Z",
        "updateTime": "2023-10-26T12:00:00Z",
        "prompt": "foo"
    }))
    session = client.create_session("foo")
    assert session.name == "sessions/123"
    assert session.prompt == "foo"
    assert session.state == SessionState.CREATED

def test_get_session(client, mock_api):
    mock_api.get("/sessions/123").mock(return_value=Response(200, json={
        "name": "sessions/123",
        "state": "RUNNING",
        "createTime": "2023-10-26T12:00:00Z",
        "updateTime": "2023-10-26T12:05:00Z",
        "prompt": "foo"
    }))
    session = client.get_session("sessions/123")
    assert session.name == "sessions/123"
    assert session.state == SessionState.RUNNING

def test_list_sessions_pagination(client, mock_api):
    # Match the first page request
    mock_api.get("/sessions").mock(return_value=Response(200, json={
        "sessions": [{"name": "sessions/1", "state": "CREATED", "createTime": "t1", "updateTime": "t1"}],
        "nextPageToken": "page2"
    }))
    
    # Match the second page request with query param
    mock_api.get("/sessions", params={"pageToken": "page2"}).mock(return_value=Response(200, json={
        "sessions": [{"name": "sessions/2", "state": "CREATED", "createTime": "t2", "updateTime": "t2"}],
        "nextPageToken": ""
    }))
    
    sessions = list(client.list_sessions())
    assert len(sessions) == 2
    assert sessions[0].name == "sessions/1"
    assert sessions[1].name == "sessions/2"

def test_delete_session(client, mock_api):
    mock_api.delete("/sessions/123").mock(return_value=Response(200, json={}))
    client.delete_session("sessions/123")
    assert mock_api.calls.last.request.method == "DELETE"
    assert mock_api.calls.last.request.url.path == "/v1alpha/sessions/123"

def test_send_message(client, mock_api):
    mock_api.post("/sessions/123:sendMessage").mock(return_value=Response(200, json={}))
    client.send_message("sessions/123", "hello")
    assert mock_api.calls.last.request.method == "POST"
    assert b"hello" in mock_api.calls.last.request.content

def test_list_activities(client, mock_api):
    mock_api.get("/sessions/123/activities").mock(return_value=Response(200, json={
        "activities": [
            {"name": "activities/1", "createTime": "t1", "type": "TYPE_A", "details": {"foo": "bar"}}
        ]
    }))
    
    activities = list(client.list_activities("sessions/123"))
    assert len(activities) == 1
    assert activities[0].name == "activities/1"
    assert activities[0].details == {"foo": "bar"}

import httpx

def test_error_handling_404(client, mock_api):
    mock_api.get("/sessions/999").mock(return_value=Response(404))
    with pytest.raises(httpx.HTTPStatusError):
        client.get_session("sessions/999")

def test_error_handling_500(client, mock_api):
    mock_api.post("/sessions").mock(return_value=Response(500))
    with pytest.raises(httpx.HTTPStatusError):
        client.create_session("fail")

def test_empty_results(client, mock_api):
    mock_api.get("/sessions").mock(return_value=Response(200, json={}))
    sessions = list(client.list_sessions())
    assert len(sessions) == 0
