"""Jules REST API Client."""
import os
import httpx
from typing import Iterator, Optional, Dict, Any
from .models import Session, Activity, Source

class JulesError(Exception):
    pass

class JulesAPIError(JulesError):
    """Exception raised for API errors."""
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code

class JulesClient:
    def _raise_for_status(self, response: httpx.Response) -> None:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise JulesAPIError(
                f"API Error {e.response.status_code}: {e.response.text}",
                e.response.status_code
            ) from e

    def _request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        try:
            response = self._client.request(method, url, **kwargs)
            self._raise_for_status(response)
            return response
        except httpx.RequestError as e:
            raise JulesError(f"Network error: {e}") from e


    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://jules.googleapis.com/v1alpha"):
        self.api_key = api_key or os.environ.get("JULES_API_KEY")
        if not self.api_key:
            raise JulesError("API key must be provided or set in JULES_API_KEY environment variable")
        self.base_url = base_url
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

            response = self._request("GET", endpoint, params=params)
            data = response.json()

            for item_data in data.get(key, []):
                yield model_cls.from_dict(item_data)

            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break

    def create_session(self, prompt: str, require_plan_approval: Optional[bool] = None, source: Optional[str] = None, source_context: Optional[Any] = None) -> Session:
        payload: Dict[str, Any] = {"prompt": prompt}
        if require_plan_approval is not None:
            payload["requirePlanApproval"] = require_plan_approval

        if source_context is not None:
            payload["sourceContext"] = source_context.to_dict()
        elif source is not None:
            # Format the source properly per the API documentation, default to 'sources/' prefix
            if not source.startswith("sources/"):
                source = f"sources/{source}"
            payload["sourceContext"] = {
                "source": source,
                "githubRepoContext": {"startingBranch": "main"}
            }

        response = self._request("POST", "/sessions", json=payload)
        return Session.from_dict(response.json())

    def get_session(self, name: str) -> Session:
        response = self._request("GET", f"/{name}")
        return Session.from_dict(response.json())

    def list_sessions(self) -> Iterator[Session]:
        yield from self._paginate("/sessions", "sessions", Session)

    def delete_session(self, name: str) -> None:
        response = self._request("DELETE", f"/{name}")

    def send_message(self, session_name: str, message: str) -> None:
        response = self._request("POST", f"/{session_name}:sendMessage", json={"prompt": message})

    def get_activity(self, name: str) -> Activity:
        response = self._request("GET", f"/{name}")
        return Activity.from_dict(response.json())

    def list_activities(self, session_name: str) -> Iterator[Activity]:
        yield from self._paginate(f"/{session_name}/activities", "activities", Activity)

    def approve_plan(self, name: str) -> None:
        response = self._request("POST", f"/{name}:approvePlan")

    def archive_session(self, name: str) -> None:
        response = self._request("POST", f"/{name}:archiveSession")

    def unarchive_session(self, name: str) -> None:
        response = self._request("POST", f"/{name}:unarchiveSession")

    def get_source(self, name: str) -> Source:
        response = self._request("GET", f"/{name}")
        return Source.from_dict(response.json())

    def list_sources(self) -> Iterator[Source]:
        yield from self._paginate("/sources", "sources", Source)
