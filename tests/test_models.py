from jules.models import Session, Activity, Source, SessionState

def test_session_from_dict():
    data = {
        "name": "sessions/123",
        "state": "CREATED",
        "createTime": "2023-01-01T00:00:00Z",
        "updateTime": "2023-01-01T00:00:00Z",
        "prompt": "hello",
    }
    session = Session.from_dict(data)
    assert session.name == "sessions/123"
    assert session.state == SessionState.CREATED
    assert session.prompt == "hello"

def test_session_to_dict():
    session = Session(
        name="sessions/1",
        state=SessionState.RUNNING,
        create_time="t1",
        update_time="t2",
    )
    d = session.to_dict()
    assert d["name"] == "sessions/1"
    assert d["state"] == "RUNNING"

def test_activity_roundtrip():
    data = {"name": "activities/1", "createTime": "t", "type": "TYPE_A", "details": {"foo": "bar"}}
    a = Activity.from_dict(data)
    assert a.details == {"foo": "bar"}
    assert a.to_dict()["type"] == "TYPE_A"

def test_source_roundtrip():
    data = {"name": "sources/1", "uri": "https://github.com/x/y", "type": "GITHUB"}
    s = Source.from_dict(data)
    assert s.uri == "https://github.com/x/y"
    assert s.to_dict()["type"] == "GITHUB"
