import pytest
import respx
from httpx import Response
from jules.client import JulesClient
from jules.models import Session, Activity, Source

@respx.mock
def test_client_init():
    with JulesClient() as client:
        assert client.BASE_URL == "https://jules.googleapis.com/"

@respx.mock
def test_sessions_list():
    respx.get("https://jules.googleapis.com/v1alpha/sessions").mock(
        return_value=Response(200, json={
            "sessions": [
                {"name": "sessions/1", "state": "QUEUED"},
                {"name": "sessions/2", "state": "IN_PROGRESS"}
            ],
            "nextPageToken": "token"
        })
    )
    respx.get("https://jules.googleapis.com/v1alpha/sessions?pageToken=token").mock(
        return_value=Response(200, json={
            "sessions": [
                {"name": "sessions/3", "state": "COMPLETED"}
            ]
        })
    )

    with JulesClient() as client:
        sessions = list(client.sessions.list())
        assert len(sessions) == 3
        assert sessions[0].name == "sessions/1"
        assert sessions[0].state == "QUEUED"
        assert sessions[2].name == "sessions/3"

@respx.mock
def test_sessions_get():
    respx.get("https://jules.googleapis.com/v1alpha/sessions/1").mock(
        return_value=Response(200, json={"name": "sessions/1", "state": "QUEUED"})
    )
    with JulesClient() as client:
        session = client.sessions.get("sessions/1")
        assert session.name == "sessions/1"
        assert session.state == "QUEUED"

@respx.mock
def test_sessions_create():
    respx.post("https://jules.googleapis.com/v1alpha/sessions").mock(
        return_value=Response(200, json={"name": "sessions/new", "state": "QUEUED"})
    )
    with JulesClient() as client:
        session = client.sessions.create({"name": "ignored_in_body_usually_but_here_we_pass_it"})
        assert session.name == "sessions/new"

@respx.mock
def test_sessions_delete():
    respx.delete("https://jules.googleapis.com/v1alpha/sessions/1").mock(
        return_value=Response(204)
    )
    with JulesClient() as client:
        client.sessions.delete("sessions/1")

@respx.mock
def test_sessions_actions():
    respx.post("https://jules.googleapis.com/v1alpha/sessions/1:sendMessage").mock(
        return_value=Response(200, json={})
    )
    respx.post("https://jules.googleapis.com/v1alpha/sessions/1:approvePlan").mock(
        return_value=Response(200, json={})
    )
    respx.post("https://jules.googleapis.com/v1alpha/sessions/1:archive").mock(
        return_value=Response(200, json={})
    )
    respx.post("https://jules.googleapis.com/v1alpha/sessions/1:unarchive").mock(
        return_value=Response(200, json={})
    )
    
    with JulesClient() as client:
        client.sessions.send_message("sessions/1", {"text": "hello"})
        client.sessions.approve_plan("sessions/1", {"approved": True})
        client.sessions.archive("sessions/1")
        client.sessions.unarchive("sessions/1")

@respx.mock
def test_activities_list():
    respx.get("https://jules.googleapis.com/v1alpha/sessions/1/activities").mock(
        return_value=Response(200, json={
            "activities": [
                {"name": "sessions/1/activities/1", "createTime": "2023-01-01T00:00:00Z"}
            ]
        })
    )
    with JulesClient() as client:
        activities = list(client.sessions.list_activities("sessions/1"))
        assert len(activities) == 1
        assert activities[0].name == "sessions/1/activities/1"

@respx.mock
def test_activities_get():
    respx.get("https://jules.googleapis.com/v1alpha/sessions/1/activities/1").mock(
        return_value=Response(200, json={"name": "sessions/1/activities/1"})
    )
    with JulesClient() as client:
        activity = client.sessions.get_activity("sessions/1/activities/1")
        assert activity.name == "sessions/1/activities/1"

@respx.mock
def test_sources_list():
    respx.get("https://jules.googleapis.com/v1alpha/sources").mock(
        return_value=Response(200, json={
            "sources": [
                {"name": "sources/1"}
            ]
        })
    )
    with JulesClient() as client:
        sources = list(client.sources.list())
        assert len(sources) == 1
        assert sources[0].name == "sources/1"

@respx.mock
def test_sources_get():
    respx.get("https://jules.googleapis.com/v1alpha/sources/1").mock(
        return_value=Response(200, json={"name": "sources/1"})
    )
    with JulesClient() as client:
        source = client.sources.get("sources/1")
        assert source.name == "sources/1"
