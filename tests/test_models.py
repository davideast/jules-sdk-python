import json
import pytest
from datetime import datetime, timezone
from jules.models import Session, SessionState, SessionOutput

def test_session_state_enum():
    assert SessionState.QUEUED == "QUEUED"
    assert SessionState("IN_PROGRESS") == SessionState.IN_PROGRESS
    with pytest.raises(ValueError):
        SessionState("INVALID_STATE")

def test_session_defaults():
    # Test creating a session manually
    now = datetime.now(timezone.utc)
    session = Session(
        name="projects/123/locations/global/sessions/456",
        id="456",
        prompt="do something",
        state=SessionState.QUEUED,
        create_time=now
    )
    assert session.outputs == []

def test_session_from_dict_minimal():
    data = {
        "name": "test-session",
        "state": "PLANNING"
    }
    session = Session.from_dict(data)
    assert session.name == "test-session"
    assert session.state == SessionState.PLANNING
    assert isinstance(session.create_time, datetime)
    assert session.outputs == []

def test_session_from_dict_full():
    data = {
        "name": "projects/123/locations/global/sessions/456",
        "id": "456",
        "prompt": "write code",
        "state": "COMPLETED",
        "create_time": "2023-10-27T10:00:00Z",
        "outputs": [
            {"result": "success"},
            {"log": "done"}
        ]
    }
    session = Session.from_dict(data)
    assert session.name == data["name"]
    assert session.id == data["id"]
    assert session.prompt == data["prompt"]
    assert session.state == SessionState.COMPLETED
    assert session.create_time.year == 2023
    assert session.create_time.month == 10
    assert session.create_time.day == 27
    assert len(session.outputs) == 2
    assert session.outputs[0].data == {"result": "success"}

def test_session_to_dict():
    dt = datetime(2023, 10, 27, 10, 0, 0, tzinfo=timezone.utc)
    # Using SessionOutput directly
    session = Session(
        name="test",
        id="1",
        prompt="hello",
        state=SessionState.IN_PROGRESS,
        create_time=dt,
        outputs=[SessionOutput(data={"foo": "bar"})]
    )
    
    data = session.to_dict()
    assert data["name"] == "test"
    assert data["state"] == "IN_PROGRESS"
    # Ensure Z is used instead of +00:00 for consistency if that's the chosen format
    assert data["create_time"] == "2023-10-27T10:00:00Z"
    assert len(data["outputs"]) == 1
    assert data["outputs"][0] == {"foo": "bar"}

def test_roundtrip_serialization():
    data_json = """
    {
        "name": "projects/123/sessions/abc",
        "id": "abc",
        "prompt": "roundtrip test",
        "state": "FAILED",
        "create_time": "2024-01-01T12:34:56Z",
        "outputs": [{"error": "something went wrong"}]
    }
    """
    initial_dict = json.loads(data_json)
    session = Session.from_dict(initial_dict)
    final_dict = session.to_dict()
    
    # Comparing fields individually or dicts if structure is exact
    assert final_dict["name"] == initial_dict["name"]
    assert final_dict["state"] == initial_dict["state"]
    # Note: to_dict formats iso string, verify it matches
    assert final_dict["create_time"] == initial_dict["create_time"]
    assert final_dict["outputs"] == initial_dict["outputs"]

    # Json roundtrip
    serialized = json.dumps(final_dict)
    deserialized = json.loads(serialized)
    session_recreated = Session.from_dict(deserialized)
    
    assert session_recreated.name == session.name
    assert session_recreated.state == session.state
    assert session_recreated.create_time == session.create_time
    # Deep equality of outputs might fail if list order or dict keys differ slightly in some implementations, 
    # but for simple dicts it should work.
    assert len(session_recreated.outputs) == len(session.outputs)
    assert session_recreated.outputs[0].data == session.outputs[0].data
