import httpx
import pytest
import respx
from jules.client import JulesClient
from jules.models import SessionState

@respx.mock
def test_create_session():
    respx.post("https://jules.googleapis.com/v1alpha/sessions").mock(
        return_value=httpx.Response(
            200, 
            json={
                "name": "sessions/123", 
                "state": "ACTIVE",
                "createTime": "2023-01-01T00:00:00Z"
            }
        )
    )

    with JulesClient(api_key="test") as client:
        session = client.create_session("test prompt")
        assert session.name == "sessions/123"
        assert session.state == SessionState.ACTIVE

@respx.mock
def test_list_sessions():
    respx.get("https://jules.googleapis.com/v1alpha/sessions").mock(
        return_value=httpx.Response(
            200,
            json={
                "sessions": [
                    {"name": "sessions/1", "state": "ACTIVE"},
                    {"name": "sessions/2", "state": "ENDED"}
                ]
            }
        )
    )

    with JulesClient(api_key="test") as client:
        sessions = list(client.list_sessions())
        assert len(sessions) == 2
        assert sessions[0].name == "sessions/1"
        assert sessions[1].state == SessionState.ENDED

@respx.mock
def test_list_sessions_pagination():
    route = respx.get("https://jules.googleapis.com/v1alpha/sessions")
    route.side_effect = [
        httpx.Response(200, json={
            "sessions": [{"name": "sessions/1"}],
            "nextPageToken": "page2"
        }),
        httpx.Response(200, json={
            "sessions": [{"name": "sessions/2"}],
            "nextPageToken": ""
        })
    ]

    with JulesClient(api_key="test") as client:
        sessions = list(client.list_sessions())
        assert len(sessions) == 2
        assert sessions[0].name == "sessions/1"
        assert sessions[1].name == "sessions/2"

@respx.mock
def test_get_session():
    respx.get("https://jules.googleapis.com/v1alpha/sessions/123").mock(
        return_value=httpx.Response(
            200,
            json={"name": "sessions/123", "state": "ACTIVE"}
        )
    )

    with JulesClient(api_key="test") as client:
        session = client.get_session("sessions/123")
        assert session.name == "sessions/123"

@respx.mock
def test_delete_session():
    respx.delete("https://jules.googleapis.com/v1alpha/sessions/123").mock(
        return_value=httpx.Response(200)
    )

    with JulesClient(api_key="test") as client:
        client.delete_session("sessions/123")

@respx.mock
def test_send_message():
    respx.post("https://jules.googleapis.com/v1alpha/sessions/123/activities").mock(
        return_value=httpx.Response(
            200,
            json={
                "name": "sessions/123/activities/456",
                "type": "message"
            }
        )
    )

    with JulesClient(api_key="test") as client:
        activity = client.send_message("sessions/123", "Hello")
        assert activity.name == "sessions/123/activities/456"

@respx.mock
def test_list_activities():
    respx.get("https://jules.googleapis.com/v1alpha/sessions/123/activities").mock(
        return_value=httpx.Response(
            200,
            json={
                "activities": [
                    {"name": "act1", "type": "message"},
                    {"name": "act2", "type": "tool_use"}
                ]
            }
        )
    )

    with JulesClient(api_key="test") as client:
        activities = list(client.list_activities("sessions/123"))
        assert len(activities) == 2
        assert activities[0].name == "act1"

@respx.mock
def test_error_handling():
    respx.get("https://jules.googleapis.com/v1alpha/sessions/999").mock(
        return_value=httpx.Response(404)
    )

    with JulesClient(api_key="test") as client:
        with pytest.raises(httpx.HTTPStatusError):
            client.get_session("sessions/999")

def test_context_manager():
    client = JulesClient(api_key="test")
    with client:
        assert not client.client.is_closed
    assert client.client.is_closed
