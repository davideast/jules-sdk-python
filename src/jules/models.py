from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any, Union

class SessionState(str, Enum):
    QUEUED = "QUEUED"
    PLANNING = "PLANNING"
    AWAITING_PLAN_APPROVAL = "AWAITING_PLAN_APPROVAL"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class AutomationMode(str, Enum):
    AUTOMATION_MODE_UNSPECIFIED = "AUTOMATION_MODE_UNSPECIFIED"
    AUTO_CREATE_PR = "AUTO_CREATE_PR"

@dataclass
class Session:
    name: str
    state: Optional[SessionState] = None
    automation_mode: Optional[AutomationMode] = None
    create_time: Optional[str] = None
    update_time: Optional[str] = None
    extra_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Session':
        known_fields = {'name', 'state', 'automationMode', 'createTime', 'updateTime'}
        
        state_val = data.get('state')
        state = SessionState(state_val) if state_val else None
        
        mode_val = data.get('automationMode')
        automation_mode = AutomationMode(mode_val) if mode_val else None
        
        extra = {k: v for k, v in data.items() if k not in known_fields}
        
        return cls(
            name=data['name'],
            state=state,
            automation_mode=automation_mode,
            create_time=data.get('createTime'),
            update_time=data.get('updateTime'),
            extra_fields=extra
        )

@dataclass
class Activity:
    name: str
    create_time: Optional[str] = None
    extra_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Activity':
        known_fields = {'name', 'createTime'}
        extra = {k: v for k, v in data.items() if k not in known_fields}
        
        return cls(
            name=data['name'],
            create_time=data.get('createTime'),
            extra_fields=extra
        )

@dataclass
class Source:
    name: str
    extra_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Source':
        known_fields = {'name'}
        extra = {k: v for k, v in data.items() if k not in known_fields}
        
        return cls(
            name=data['name'],
            extra_fields=extra
        )
