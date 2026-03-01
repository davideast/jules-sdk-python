from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum

class SessionState(str, Enum):
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class AutomationMode(str, Enum):
    AUTOMATION_MODE_UNSPECIFIED = "AUTOMATION_MODE_UNSPECIFIED"
    AUTO_CREATE_PR = "AUTO_CREATE_PR"

class ActivityType(str, Enum):
    ACTIVITY_TYPE_UNSPECIFIED = "ACTIVITY_TYPE_UNSPECIFIED"
    AGENT_MESSAGED = "AGENT_MESSAGED"
    USER_MESSAGED = "USER_MESSAGED"
    PLAN_CREATED = "PLAN_CREATED"
    PLAN_UPDATED = "PLAN_UPDATED"
    PLAN_APPROVED = "PLAN_APPROVED"
    PATCH_GENERATED = "PATCH_GENERATED"
    PR_CREATED = "PR_CREATED"
    ERROR_OCCURRED = "ERROR_OCCURRED"

@dataclass
class GitHubRepo:
    owner: str
    name: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GitHubRepo":
        return cls(
            owner=data["owner"],
            name=data["name"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "owner": self.owner,
            "name": self.name,
        }

@dataclass
class PullRequest:
    repo: GitHubRepo
    number: int
    url: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PullRequest":
        return cls(
            repo=GitHubRepo.from_dict(data["repo"]),
            number=data["number"],
            url=data["url"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "repo": self.repo.to_dict(),
            "number": self.number,
            "url": self.url,
        }

@dataclass
class GitPatch:
    base_commit: str
    patch: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GitPatch":
        return cls(
            base_commit=data["baseCommit"],
            patch=data["patch"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "baseCommit": self.base_commit,
            "patch": self.patch,
        }

@dataclass
class PlanStep:
    description: str
    status: str
    output: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlanStep":
        return cls(
            description=data["description"],
            status=data["status"],
            output=data.get("output"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "status": self.status,
            "output": self.output,
        }

@dataclass
class Plan:
    steps: List[PlanStep]
    status: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Plan":
        return cls(
            steps=[PlanStep.from_dict(s) for s in data.get("steps", [])],
            status=data["status"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "steps": [s.to_dict() for s in self.steps],
            "status": self.status,
        }

@dataclass
class SessionOutput:
    pull_request: Optional[PullRequest] = None
    git_patch: Optional[GitPatch] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SessionOutput":
        return cls(
            pull_request=PullRequest.from_dict(data["pullRequest"]) if "pullRequest" in data else None,
            git_patch=GitPatch.from_dict(data["gitPatch"]) if "gitPatch" in data else None,
        )

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        if self.pull_request:
            res["pullRequest"] = self.pull_request.to_dict()
        if self.git_patch:
            res["gitPatch"] = self.git_patch.to_dict()
        return res

@dataclass
class Session:
    name: str
    state: SessionState
    create_time: str
    update_time: str
    expire_time: Optional[str] = None
    prompt: Optional[str] = None
    automation_mode: AutomationMode = AutomationMode.AUTOMATION_MODE_UNSPECIFIED
    output: Optional[SessionOutput] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Session":
        return cls(
            name=data["name"],
            state=SessionState(data.get("state", "STATE_UNSPECIFIED")),
            create_time=data["createTime"],
            update_time=data["updateTime"],
            expire_time=data.get("expireTime"),
            prompt=data.get("prompt"),
            automation_mode=AutomationMode(data.get("automationMode", "AUTOMATION_MODE_UNSPECIFIED")),
            output=SessionOutput.from_dict(data["output"]) if "output" in data else None,
        )

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {
            "name": self.name,
            "state": self.state.value,
            "createTime": self.create_time,
            "updateTime": self.update_time,
            "expireTime": self.expire_time,
            "prompt": self.prompt,
            "automationMode": self.automation_mode.value,
        }
        if self.output:
            res["output"] = self.output.to_dict()
        return res

@dataclass
class Activity:
    name: str
    create_time: str
    type: ActivityType
    details: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Activity":
        # Deduce activity type based on provided one-of properties if type is not explicit
        # The discovery doc might not explicitly provide an enum, so we synthesize it here
        # E.g. agentMessaged, userMessaged, planCreated, etc.
        # However, if 'type' is present, we try to parse it
        activity_type_str = data.get("type")
        if not activity_type_str:
            if "agentMessaged" in data:
                activity_type_str = "AGENT_MESSAGED"
            elif "userMessaged" in data:
                activity_type_str = "USER_MESSAGED"
            elif "planCreated" in data:
                activity_type_str = "PLAN_CREATED"
            elif "planUpdated" in data:
                activity_type_str = "PLAN_UPDATED"
            elif "planApproved" in data:
                activity_type_str = "PLAN_APPROVED"
            elif "patchGenerated" in data:
                activity_type_str = "PATCH_GENERATED"
            elif "prCreated" in data:
                activity_type_str = "PR_CREATED"
            elif "errorOccurred" in data:
                activity_type_str = "ERROR_OCCURRED"
            else:
                activity_type_str = "ACTIVITY_TYPE_UNSPECIFIED"

        try:
            activity_type = ActivityType(activity_type_str)
        except ValueError:
            activity_type = ActivityType.ACTIVITY_TYPE_UNSPECIFIED

        return cls(
            name=data["name"],
            create_time=data["createTime"],
            type=activity_type,
            details=data.get("details", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "createTime": self.create_time,
            "type": self.type.value,
            "details": self.details,
        }

@dataclass
class Source:
    name: str
    uri: str
    type: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Source":
        return cls(
            name=data["name"],
            uri=data["uri"],
            type=data["type"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "uri": self.uri,
            "type": self.type,
        }
