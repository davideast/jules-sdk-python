from dataclasses import dataclass, field
from typing import Optional, List, Any, Dict
from enum import Enum
import datetime

class SessionState(str, Enum):
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"
    QUEUED = "QUEUED"
    PLANNING = "PLANNING"
    AWAITING_PLAN_APPROVAL = "AWAITING_PLAN_APPROVAL"
    AWAITING_USER_FEEDBACK = "AWAITING_USER_FEEDBACK"
    IN_PROGRESS = "IN_PROGRESS"
    PAUSED = "PAUSED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"

@dataclass
class SessionOutput:
    """Represents an output from a session."""
    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> 'SessionOutput':
        return cls(data=data)

    def to_dict(self) -> dict:
        return self.data

@dataclass
class Session:
    name: str
    id: str
    prompt: str
    state: SessionState
    create_time: datetime.datetime
    outputs: List[SessionOutput] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> 'Session':
        create_time_str = data.get("create_time")
        if create_time_str:
            if create_time_str.endswith('Z'):
                create_time_str = create_time_str[:-1] + '+00:00'
            create_time = datetime.datetime.fromisoformat(create_time_str)
        else:
            # If create_time is missing, it's better to raise or handle it. 
            # But based on typical API behavior, we might want a default or just current time for now.
            create_time = datetime.datetime.now(datetime.timezone.utc)

        return cls(
            name=data.get("name", ""),
            id=data.get("id", ""),
            prompt=data.get("prompt", ""),
            state=SessionState(data.get("state", "STATE_UNSPECIFIED")),
            create_time=create_time,
            outputs=[SessionOutput.from_dict(o) for o in data.get("outputs", [])]
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "id": self.id,
            "prompt": self.prompt,
            "state": self.state.value,
            "create_time": self.create_time.isoformat().replace('+00:00', 'Z'),
            "outputs": [o.to_dict() for o in self.outputs]
        }
