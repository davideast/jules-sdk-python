"""Jules REST API Client."""
import os
import httpx
from typing import Iterator, Optional, Dict, Any
from .models import Session, Activity, Source

class JulesError(Exception):
    pass

class JulesAPIError(JulesError):
    """Exception raised for API errors."""

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

    def __enter__(self) -> "JulesClient":
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self._client.close()

    def _paginate(self, endpoint: str, key: str, model_cls: Any) -> Iterator[Any]:
        next_page_token = None
        while True:
            params: Dict[str, Any] = {}
            if next_page_token:
                params["pageToken"] = next_page_token

            response = self._client.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            for item_data in data.get(key, []):
                yield model_cls.from_dict(item_data)

            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break

    def create_session(self, prompt: str) -> Session:
        response = self._client.post("/sessions", json={"prompt": prompt})
        response.raise_for_status()
        return Session.from_dict(response.json())

    def get_session(self, name: str) -> Session:
        response = self._client.get(f"/{name}")
        response.raise_for_status()
        return Session.from_dict(response.json())

    def list_sessions(self) -> Iterator[Session]:
        yield from self._paginate("/sessions", "sessions", Session)

    def delete_session(self, name: str) -> None:
        response = self._client.delete(f"/{name}")
        response.raise_for_status()

    def send_message(self, session_name: str, message: str) -> None:
        response = self._client.post(f"/{session_name}:sendMessage", json={"message": message})
        response.raise_for_status()

    def get_activity(self, name: str) -> Activity:
        response = self._client.get(f"/{name}")
        response.raise_for_status()
        return Activity.from_dict(response.json())

    def list_activities(self, session_name: str) -> Iterator[Activity]:
        yield from self._paginate(f"/{session_name}/activities", "activities", Activity)

    def approve_plan(self, name: str) -> None:
        response = self._client.post(f"/{name}:approvePlan")
        response.raise_for_status()

    def archive_session(self, name: str) -> None:
        response = self._client.post(f"/{name}:archiveSession")
        response.raise_for_status()

    def unarchive_session(self, name: str) -> None:
        response = self._client.post(f"/{name}:unarchiveSession")
        response.raise_for_status()

    def get_source(self, name: str) -> Source:
        response = self._client.get(f"/{name}")
        response.raise_for_status()
        return Source.from_dict(response.json())

    def list_sources(self) -> Iterator[Source]:
        yield from self._paginate("/sources", "sources", Source)
