import os
import httpx
from typing import Iterator, Optional, Dict, Any
from .models import Session, Activity, Source

class JulesError(Exception):
    pass

class JulesClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("JULES_API_KEY")
        if not self.api_key:
            raise JulesError("API key must be provided or set in JULES_API_KEY environment variable")
        self.base_url = "https://jules.googleapis.com/v1alpha"
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"x-goog-api-key": self.api_key}
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._client.close()

    def create_session(self, prompt: str) -> Session:
        response = self._client.post("/sessions", json={"prompt": prompt})
        response.raise_for_status()
        return Session.from_dict(response.json())

    def get_session(self, name: str) -> Session:
        response = self._client.get(f"/{name}")
        response.raise_for_status()
        return Session.from_dict(response.json())

    def list_sessions(self) -> Iterator[Session]:
        next_page_token = None
        while True:
            params: Dict[str, Any] = {}
            if next_page_token:
                params["pageToken"] = next_page_token

            response = self._client.get("/sessions", params=params)
            response.raise_for_status()
            data = response.json()

            for session_data in data.get("sessions", []):
                yield Session.from_dict(session_data)

            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break

    def get_activity(self, name: str) -> Activity:
        response = self._client.get(f"/{name}")
        response.raise_for_status()
        return Activity.from_dict(response.json())

    def get_source(self, name: str) -> Source:
        response = self._client.get(f"/{name}")
        response.raise_for_status()
        return Source.from_dict(response.json())

    def list_sources(self) -> Iterator[Source]:
        next_page_token = None
        while True:
            params: Dict[str, Any] = {}
            if next_page_token:
                params["pageToken"] = next_page_token

            response = self._client.get("/sources", params=params)
            response.raise_for_status()
            data = response.json()

            for source_data in data.get("sources", []):
                yield Source.from_dict(source_data)

            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break

    def approve_plan(self, session_name: str) -> None:
        response = self._client.post(f"/{session_name}:approvePlan")
        response.raise_for_status()

    def archive_session(self, session_name: str) -> None:
        response = self._client.post(f"/{session_name}:archive")
        response.raise_for_status()

    def unarchive_session(self, session_name: str) -> None:
        response = self._client.post(f"/{session_name}:unarchive")
        response.raise_for_status()

    def delete_session(self, name: str) -> None:
        response = self._client.delete(f"/{name}")
        response.raise_for_status()

    def send_message(self, session_name: str, message: str) -> None:
        response = self._client.post(f"/{session_name}:sendMessage", json={"message": message})
        response.raise_for_status()

    def list_activities(self, session_name: str) -> Iterator[Activity]:
        next_page_token = None
        while True:
            params: Dict[str, Any] = {}
            if next_page_token:
                params["pageToken"] = next_page_token

            response = self._client.get(f"/{session_name}/activities", params=params)
            response.raise_for_status()
            data = response.json()

            for activity_data in data.get("activities", []):
                yield Activity.from_dict(activity_data)

            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break
