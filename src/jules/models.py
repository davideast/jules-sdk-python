from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime

class SessionState(str, Enum):
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"
    ACTIVE = "ACTIVE"
    ENDED = "ENDED"
    ERROR = "ERROR"

@dataclass
class Source:
    uri: str
    mime_type: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Source":
        return cls(
            uri=data.get("uri", ""),
            mime_type=data.get("mimeType")
        )

@dataclass
class Activity:
    name: str
    type: str
    create_time: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Activity":
        create_time = None
        if "createTime" in data:
            try:
                create_time = datetime.fromisoformat(data["createTime"].replace("Z", "+00:00"))
            except ValueError:
                pass
                
        return cls(
            name=data.get("name", ""),
            type=data.get("type", ""),
            create_time=create_time
        )

@dataclass
class Session:
    name: str
    state: SessionState
    create_time: Optional[datetime] = None
    expire_time: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Session":
        create_time = None
        if "createTime" in data:
            try:
                create_time = datetime.fromisoformat(data["createTime"].replace("Z", "+00:00"))
            except ValueError:
                pass

        expire_time = None
        if "expireTime" in data:
            try:
                expire_time = datetime.fromisoformat(data["expireTime"].replace("Z", "+00:00"))
            except ValueError:
                pass
                
        return cls(
            name=data.get("name", ""),
            state=SessionState(data.get("state", "STATE_UNSPECIFIED")),
            create_time=create_time,
            expire_time=expire_time
        )
