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

@dataclass
class Session:
    name: str
    state: SessionState
    create_time: str
    update_time: str
    expire_time: Optional[str] = None
    prompt: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Session":
        return cls(
            name=data["name"],
            state=SessionState(data.get("state", "STATE_UNSPECIFIED")),
            create_time=data["createTime"],
            update_time=data["updateTime"],
            expire_time=data.get("expireTime"),
            prompt=data.get("prompt"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "state": self.state.value,
            "createTime": self.create_time,
            "updateTime": self.update_time,
            "expireTime": self.expire_time,
            "prompt": self.prompt,
        }

@dataclass
class Activity:
    name: str
    create_time: str
    type: str
    details: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Activity":
        return cls(
            name=data["name"],
            create_time=data["createTime"],
            type=data["type"],
            details=data.get("details", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "createTime": self.create_time,
            "type": self.type,
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
