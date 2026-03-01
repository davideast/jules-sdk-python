from jules.models import (
    Session,
    Activity,
    Source,
    SessionState,
    AutomationMode,
    ActivityType,
    GitPatch,
    Plan,
    PlanStep,
    SessionOutput,
    PullRequest,
    GitHubRepo,
)

def test_session_from_dict():
    data = {
        "name": "sessions/123",
        "state": "CREATED",
        "createTime": "2023-01-01T00:00:00Z",
        "updateTime": "2023-01-01T00:00:00Z",
        "prompt": "hello",
        "automationMode": "AUTO_CREATE_PR",
        "output": {
            "gitPatch": {
                "baseCommit": "abcdef",
                "patch": "diff --git a/file b/file"
            }
        }
    }
    session = Session.from_dict(data)
    assert session.name == "sessions/123"
    assert session.state == SessionState.CREATED
    assert session.prompt == "hello"
    assert session.automation_mode == AutomationMode.AUTO_CREATE_PR
    assert session.output is not None
    assert session.output.git_patch is not None
    assert session.output.git_patch.base_commit == "abcdef"
    assert session.output.pull_request is None

def test_session_to_dict():
    session = Session(
        name="sessions/1",
        state=SessionState.RUNNING,
        create_time="t1",
        update_time="t2",
        automation_mode=AutomationMode.AUTO_CREATE_PR,
    )
    d = session.to_dict()
    assert d["name"] == "sessions/1"
    assert d["state"] == "RUNNING"
    assert d["automationMode"] == "AUTO_CREATE_PR"
    assert "output" not in d

def test_session_output_pull_request():
    out = SessionOutput(
        pull_request=PullRequest(
            repo=GitHubRepo(owner="jules", name="repo"),
            number=1,
            url="https://github.com/jules/repo/pull/1"
        )
    )
    d = out.to_dict()
    assert d["pullRequest"]["repo"]["owner"] == "jules"
    out2 = SessionOutput.from_dict(d)
    assert out2.pull_request is not None
    assert out2.pull_request.number == 1

def test_plan_roundtrip():
    data = {
        "status": "APPROVED",
        "steps": [
            {"description": "Step 1", "status": "COMPLETED", "output": "Done"}
        ]
    }
    p = Plan.from_dict(data)
    assert p.status == "APPROVED"
    assert len(p.steps) == 1
    assert p.steps[0].description == "Step 1"
    d = p.to_dict()
    assert d["steps"][0]["status"] == "COMPLETED"

def test_activity_type_inference():
    # Test implicit type
    a1 = Activity.from_dict({"name": "a/1", "createTime": "t1", "agentMessaged": {}})
    assert a1.type == ActivityType.AGENT_MESSAGED

    # Test explicit type
    a2 = Activity.from_dict({"name": "a/2", "createTime": "t2", "type": "USER_MESSAGED"})
    assert a2.type == ActivityType.USER_MESSAGED

    # Test fallback
    a3 = Activity.from_dict({"name": "a/3", "createTime": "t3", "someRandomField": {}})
    assert a3.type == ActivityType.ACTIVITY_TYPE_UNSPECIFIED

def test_activity_roundtrip():
    data = {"name": "activities/1", "createTime": "t", "type": "AGENT_MESSAGED", "details": {"foo": "bar"}}
    a = Activity.from_dict(data)
    assert a.details == {"foo": "bar"}
    assert a.to_dict()["type"] == "AGENT_MESSAGED"

def test_source_roundtrip():
    data = {"name": "sources/1", "uri": "https://github.com/x/y", "type": "GITHUB"}
    s = Source.from_dict(data)
    assert s.uri == "https://github.com/x/y"
    assert s.to_dict()["type"] == "GITHUB"
