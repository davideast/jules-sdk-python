"""Data models for the Jules API."""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum

class AutomationMode(str, Enum):
    AUTOMATION_MODE_UNSPECIFIED = "AUTOMATION_MODE_UNSPECIFIED"
    AUTO_CREATE_PR = "AUTO_CREATE_PR"

class SessionState(str, Enum):
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class ActivityType(str, Enum):
    AGENT_MESSAGED = "agentMessaged"
    USER_MESSAGED = "userMessaged"
    PLAN_GENERATED = "planGenerated"
    PLAN_APPROVED = "planApproved"
    PROGRESS_UPDATED = "progressUpdated"
    SESSION_COMPLETED = "sessionCompleted"
    SESSION_FAILED = "sessionFailed"

@dataclass
class Session:
    name: str
    state: SessionState
    create_time: str
    update_time: str
    expire_time: Optional[str] = None
    prompt: Optional[str] = None
    automation_mode: AutomationMode = AutomationMode.AUTOMATION_MODE_UNSPECIFIED
    outputs: List['SessionOutput'] = field(default_factory=list)
    archived: bool = False
    url: Optional[str] = None

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
            outputs=[SessionOutput.from_dict(o) for o in data.get("outputs", [])],
            archived=data.get("archived", False),
            url=data.get("url"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "name": self.name,
            "state": self.state.value,
            "createTime": self.create_time,
            "updateTime": self.update_time,
            "automationMode": self.automation_mode.value,
            "outputs": [o.to_dict() for o in self.outputs],
            "archived": self.archived,
        }
        if self.expire_time:
            result["expireTime"] = self.expire_time
        if self.prompt:
            result["prompt"] = self.prompt
        if self.url:
            result["url"] = self.url
        return result


@dataclass
class Activity:
    name: str
    create_time: str
    type: ActivityType
    details: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Activity":
        # Identify the activity type from the keys
        # The actual API returns one-of fields, e.g. "userMessaged": {...}
        # The synthetic type will correspond to the one-of field present.
        details: Dict[str, Any] = {}
        activity_type = ActivityType.AGENT_MESSAGED  # fallback, should ideally not happen if enum covers all

        # We need to look for any of the known one-of fields
        # Note: If memory states that ActivityType is not explicitly defined in the discovery doc
        # (which uses one-of properties) and requires a custom synthetic enum in the Python SDK
        # for idiomatic usage (e.g., AGENT_MESSAGED, USER_MESSAGED), we implement that logic here.
        for t in ActivityType:
            if t.value in data:
                activity_type = t
                details = data[t.value]
                break

        return cls(
            name=data["name"],
            create_time=data["createTime"],
            type=activity_type,
            details=details,
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "name": self.name,
            "createTime": self.create_time,
        }
        result[self.type.value] = self.details
        return result

@dataclass
class GitHubBranch:
    display_name: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GitHubBranch":
        return cls(
            display_name=data["displayName"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "displayName": self.display_name,
        }

@dataclass
class GitHubRepo:
    owner: str
    repo: str
    is_private: bool
    default_branch: GitHubBranch
    branches: List[GitHubBranch]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GitHubRepo":
        return cls(
            owner=data.get("owner", ""),
            repo=data.get("repo", ""),
            is_private=data.get("isPrivate", False),
            default_branch=GitHubBranch.from_dict(data["defaultBranch"]) if "defaultBranch" in data else GitHubBranch(""),
            branches=[GitHubBranch.from_dict(b) for b in data.get("branches", [])],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "owner": self.owner,
            "repo": self.repo,
            "isPrivate": self.is_private,
            "defaultBranch": self.default_branch.to_dict(),
            "branches": [b.to_dict() for b in self.branches],
        }

@dataclass
class Source:
    name: str
    id: str
    github_repo: Optional[GitHubRepo] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Source":
        return cls(
            name=data["name"],
            id=data.get("id", ""),
            github_repo=GitHubRepo.from_dict(data["githubRepo"]) if "githubRepo" in data else None,
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "name": self.name,
            "id": self.id,
        }
        if self.github_repo:
            result["githubRepo"] = self.github_repo.to_dict()
        return result

@dataclass
class PlanStep:
    id: str
    title: str
    description: str
    index: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlanStep":
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            index=data["index"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "index": self.index,
        }

@dataclass
class Plan:
    id: str
    steps: List[PlanStep]
    create_time: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Plan":
        return cls(
            id=data["id"],
            steps=[PlanStep.from_dict(s) for s in data.get("steps", [])],
            create_time=data["createTime"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "steps": [s.to_dict() for s in self.steps],
            "createTime": self.create_time,
        }


@dataclass
class PullRequest:
    url: str
    title: str
    description: str
    base_ref: str
    head_ref: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PullRequest":
        return cls(
            url=data.get("url", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            base_ref=data.get("baseRef", ""),
            head_ref=data.get("headRef", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "baseRef": self.base_ref,
            "headRef": self.head_ref,
        }

@dataclass
class GitPatch:
    unidiff_patch: str
    base_commit_id: str
    suggested_commit_message: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GitPatch":
        return cls(
            unidiff_patch=data.get("unidiffPatch", ""),
            base_commit_id=data.get("baseCommitId", ""),
            suggested_commit_message=data.get("suggestedCommitMessage", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "unidiffPatch": self.unidiff_patch,
            "baseCommitId": self.base_commit_id,
            "suggestedCommitMessage": self.suggested_commit_message,
        }

@dataclass
class ChangeSet:
    git_patch: GitPatch
    source: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChangeSet":
        return cls(
            git_patch=GitPatch.from_dict(data["gitPatch"]) if "gitPatch" in data else GitPatch("", "", ""),
            source=data.get("source", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gitPatch": self.git_patch.to_dict(),
            "source": self.source,
        }

@dataclass
class SessionOutput:
    pull_request: Optional[PullRequest] = None
    change_set: Optional[ChangeSet] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SessionOutput":
        return cls(
            pull_request=PullRequest.from_dict(data["pullRequest"]) if "pullRequest" in data else None,
            change_set=ChangeSet.from_dict(data["changeSet"]) if "changeSet" in data else None,
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.pull_request:
            result["pullRequest"] = self.pull_request.to_dict()
        if self.change_set:
            result["changeSet"] = self.change_set.to_dict()
        return result
