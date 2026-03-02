from jules.models import Session, Activity, Source, SessionState

def test_session_from_dict():
    data = {
        "name": "sessions/123",
        "state": "CREATED",
        "createTime": "2023-01-01T00:00:00Z",
        "updateTime": "2023-01-01T00:00:00Z",
        "prompt": "hello",
        "id": "123",
        "title": "My Session",
        "requirePlanApproval": True,
        "sourceContext": {
            "source": "sources/1",
            "githubRepoContext": {
                "githubRepo": {
                    "owner": "test",
                    "repo": "repo",
                    "isPrivate": True,
                    "defaultBranch": {"displayName": "main"},
                    "branches": [{"displayName": "main"}]
                }
            },
            "workingBranch": "main",
            "environmentVariablesEnabled": True
        }
    }
    session = Session.from_dict(data)
    assert session.name == "sessions/123"
    assert session.state == SessionState.CREATED
    assert session.prompt == "hello"
    assert session.id == "123"
    assert session.title == "My Session"
    assert session.require_plan_approval is True
    assert session.source_context is not None
    assert session.source_context.source == "sources/1"
    assert session.source_context.github_repo_context is not None
    assert session.source_context.github_repo_context.github_repo.owner == "test"
    assert session.source_context.working_branch == "main"
    assert session.source_context.environment_variables_enabled is True

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
    assert "expireTime" not in d

def test_activity_roundtrip():
    data = {
        "name": "activities/1",
        "createTime": "t",
        "agentMessaged": {"message": "hello world"},
        "id": "activity_1",
        "description": "Agent sent a message",
        "originator": "agent",
        "artifacts": [{"id": "artifact_1", "type": "code"}]
    }
    a = Activity.from_dict(data)
    assert a.details == {"message": "hello world"}
    assert a.type.value == "agentMessaged"
    assert a.id == "activity_1"
    assert a.description == "Agent sent a message"
    assert a.originator == "agent"
    assert len(a.artifacts) == 1
    assert a.artifacts[0]["id"] == "artifact_1"

    roundtrip = a.to_dict()
    assert roundtrip["name"] == "activities/1"
    assert roundtrip["createTime"] == "t"
    assert "agentMessaged" in roundtrip
    assert roundtrip["agentMessaged"] == {"message": "hello world"}
    assert roundtrip["id"] == "activity_1"
    assert roundtrip["description"] == "Agent sent a message"
    assert roundtrip["originator"] == "agent"
    assert roundtrip["artifacts"][0]["id"] == "artifact_1"

def test_source_roundtrip():
    data = {
        "name": "sources/1",
        "id": "1",
        "githubRepo": {
            "owner": "test",
            "repo": "repo",
            "isPrivate": True,
            "defaultBranch": {"displayName": "main"},
            "branches": [{"displayName": "main"}]
        }
    }
    s = Source.from_dict(data)
    assert s.id == "1"
    assert s.github_repo is not None
    assert s.github_repo.owner == "test"
    assert s.github_repo.repo == "repo"

    roundtrip = s.to_dict()
    assert roundtrip["name"] == "sources/1"
    assert roundtrip["id"] == "1"
    assert "githubRepo" in roundtrip
    assert roundtrip["githubRepo"]["owner"] == "test"

from jules.models import Plan, PlanStep, PullRequest, SessionOutput, AutomationMode

def test_plan_roundtrip():
    data = {
        "id": "plans/1",
        "steps": [
            {
                "id": "steps/1",
                "title": "Step 1",
                "description": "Do this",
                "index": 0
            },
            {
                "id": "steps/2",
                "title": "Step 2",
                "description": "Do that",
                "index": 1
            }
        ],
        "createTime": "2023-10-01T00:00:00Z"
    }

    plan = Plan.from_dict(data)
    assert plan.id == "plans/1"
    assert len(plan.steps) == 2
    assert plan.steps[0].id == "steps/1"
    assert plan.steps[0].title == "Step 1"
    assert plan.steps[1].index == 1
    assert plan.create_time == "2023-10-01T00:00:00Z"

    roundtrip = plan.to_dict()
    assert roundtrip == data

def test_session_outputs():
    data = {
        "name": "sessions/456",
        "state": "COMPLETED",
        "createTime": "2023-01-01T00:00:00Z",
        "updateTime": "2023-01-01T00:00:00Z",
        "automationMode": "AUTO_CREATE_PR",
        "outputs": [
            {
                "pullRequest": {
                    "url": "https://github.com/owner/repo/pull/1",
                    "title": "Fix bug",
                    "description": "Fixes an issue.",
                    "baseRef": "main",
                    "headRef": "feature"
                }
            }
        ],
        "archived": True
    }

    session = Session.from_dict(data)
    assert session.name == "sessions/456"
    assert session.state == SessionState.COMPLETED
    assert session.automation_mode == AutomationMode.AUTO_CREATE_PR
    assert len(session.outputs) == 1

    pr = session.outputs[0].pull_request
    assert pr is not None
    assert pr.url == "https://github.com/owner/repo/pull/1"
    assert pr.title == "Fix bug"
    assert pr.base_ref == "main"
    assert pr.head_ref == "feature"
    assert session.outputs[0].change_set is None

    assert session.archived is True

    roundtrip = session.to_dict()
    assert roundtrip["automationMode"] == "AUTO_CREATE_PR"
    assert len(roundtrip["outputs"]) == 1
    assert roundtrip["outputs"][0]["pullRequest"]["url"] == "https://github.com/owner/repo/pull/1"
    assert roundtrip["archived"] is True
