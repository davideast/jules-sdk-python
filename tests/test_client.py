import pytest
import httpx
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
    assert session.state == SessionState.CREATED

def test_get_session(client, mock_api):
    mock_api.get("/sessions/123").mock(return_value=Response(200, json={
        "name": "sessions/123",
        "state": "RUNNING",
        "createTime": "2023-10-26T12:00:00Z",
        "updateTime": "2023-10-26T12:05:00Z",
    }))
    session = client.get_session("sessions/123")
    assert session.state == SessionState.RUNNING

def test_list_sessions_pagination(client, mock_api):
    def side_effect(request):
        params = request.url.params
        if "pageToken" not in params:
             return Response(200, json={
                "sessions": [{"name": "sessions/1", "state": "CREATED", "createTime": "t1", "updateTime": "t1"}],
                "nextPageToken": "page2"
            })
        elif params["pageToken"] == "page2":
             return Response(200, json={
                "sessions": [{"name": "sessions/2", "state": "CREATED", "createTime": "t2", "updateTime": "t2"}],
            })
        return Response(404)

    mock_api.get("/sessions").mock(side_effect=side_effect)
    sessions = list(client.list_sessions())
    assert len(sessions) == 2

def test_delete_session(client, mock_api):
    mock_api.delete("/sessions/123").mock(return_value=Response(200, json={}))
    client.delete_session("sessions/123")

def test_send_message(client, mock_api):
    mock_api.post("/sessions/123:sendMessage").mock(return_value=Response(200, json={}))
    client.send_message("sessions/123", "hello")

def test_get_activity(client, mock_api):
    mock_api.get("/activities/1").mock(return_value=Response(200, json={
        "name": "activities/1", "createTime": "t1", "type": "AGENT_MESSAGED"
    }))
    activity = client.get_activity("activities/1")
    assert activity.name == "activities/1"

def test_get_source(client, mock_api):
    mock_api.get("/sources/1").mock(return_value=Response(200, json={
        "name": "sources/1", "uri": "u1", "type": "GITHUB"
    }))
    source = client.get_source("sources/1")
    assert source.name == "sources/1"

def test_list_sources(client, mock_api):
    mock_api.get("/sources").mock(return_value=Response(200, json={
        "sources": [{"name": "sources/1", "uri": "u1", "type": "GITHUB"}]
    }))
    sources = list(client.list_sources())
    assert len(sources) == 1

def test_approve_plan(client, mock_api):
    mock_api.post("/sessions/123:approvePlan").mock(return_value=Response(200, json={}))
    client.approve_plan("sessions/123")

def test_archive_session(client, mock_api):
    mock_api.post("/sessions/123:archive").mock(return_value=Response(200, json={}))
    client.archive_session("sessions/123")

def test_unarchive_session(client, mock_api):
    mock_api.post("/sessions/123:unarchive").mock(return_value=Response(200, json={}))
    client.unarchive_session("sessions/123")

def test_list_activities(client, mock_api):
    mock_api.get("/sessions/123/activities").mock(return_value=Response(200, json={
        "activities": [
            {"name": "activities/1", "createTime": "t1", "type": "AGENT_MESSAGED", "details": {"foo": "bar"}}
        ]
    }))
    activities = list(client.list_activities("sessions/123"))
    assert len(activities) == 1
    assert activities[0].details == {"foo": "bar"}

def test_error_handling_404(client, mock_api):
    mock_api.get("/sessions/999").mock(return_value=Response(404))
    with pytest.raises(httpx.HTTPStatusError):
        client.get_session("sessions/999")

def test_empty_results(client, mock_api):
    mock_api.get("/sessions").mock(return_value=Response(200, json={}))
    sessions = list(client.list_sessions())
    assert len(sessions) == 0
