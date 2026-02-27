import os
import httpx
from typing import Iterator, Optional, Dict, Any
from .models import Session, SessionState, Activity, Source

class JulesClient:
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://jules.googleapis.com"):
        self.api_key = api_key or os.getenv("JULES_API_KEY")
        headers = {}
        if self.api_key:
             headers["x-goog-api-key"] = self.api_key
        self.client = httpx.Client(base_url=base_url, headers=headers)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def list_sessions(self, page_size: int = 30) -> Iterator[Session]:
        next_page_token = None
        while True:
            params = {"pageSize": page_size}
            if next_page_token:
                params["pageToken"] = next_page_token
            
            response = self.client.get("/v1alpha/sessions", params=params)
            response.raise_for_status()
            data = response.json()
            
            for session_data in data.get("sessions", []):
                yield Session.from_dict(session_data)
                
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break

    def create_session(self, prompt: str, source_context: Optional[dict] = None) -> Session:
        # Assuming typical structure for creating a session
        body: Dict[str, Any] = {"prompt": prompt}
        if source_context:
            body["sourceContext"] = source_context
            
        response = self.client.post("/v1alpha/sessions", json=body)
        response.raise_for_status()
        return Session.from_dict(response.json())

    def get_session(self, session_id: str) -> Session:
        response = self.client.get(f"/v1alpha/{session_id}")
        response.raise_for_status()
        return Session.from_dict(response.json())

    def delete_session(self, session_id: str) -> None:
        response = self.client.delete(f"/v1alpha/{session_id}")
        response.raise_for_status()

    def send_message(self, session_id: str, content: str) -> Activity:
        # Assuming typical structure for sending a message/activity
        body = {"content": content}
        response = self.client.post(f"/v1alpha/{session_id}/activities", json=body)
        response.raise_for_status()
        return Activity.from_dict(response.json())

    def list_activities(self, session_id: str, page_size: int = 30) -> Iterator[Activity]:
        next_page_token = None
        while True:
            params = {"pageSize": page_size}
            if next_page_token:
                params["pageToken"] = next_page_token
            
            response = self.client.get(f"/v1alpha/{session_id}/activities", params=params)
            response.raise_for_status()
            data = response.json()
            
            for activity_data in data.get("activities", []):
                yield Activity.from_dict(activity_data)
                
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break
