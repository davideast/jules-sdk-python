from typing import Iterator, Optional, Dict, Any, List, Union
import httpx
from .models import Session, Activity, Source

class JulesClient:
    BASE_URL = "https://jules.googleapis.com/"

    def __init__(self, client: Optional[httpx.Client] = None):
        self._client = client
        self._own_client = False
        if self._client is None:
            self._client = httpx.Client(base_url=self.BASE_URL)
            self._own_client = True
        
        self.sessions = SessionsResource(self._client)
        self.sources = SourcesResource(self._client)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if self._own_client:
            self._client.close()


class Resource:
    def __init__(self, client: httpx.Client):
        self._client = client

    def _get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self._client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, url: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self._client.post(url, json=json)
        response.raise_for_status()
        return response.json()

    def _delete(self, url: str) -> Dict[str, Any]:
        response = self._client.delete(url)
        # Delete might return 200 with json or 204 no content.
        # Discovery findings say "delete(name)", typically returns Empty or the deleted resource.
        # Safely handle empty response
        if response.status_code == 204:
             return {}
        response.raise_for_status()
        return response.json()
        
    def _paginate(self, url: str, key: str, params: Optional[Dict[str, Any]] = None) -> Iterator[Dict[str, Any]]:
        # Avoid modifying the original params dict in loop
        current_params = params.copy() if params else {}
        
        while True:
            response_json = self._get(url, params=current_params)
            items = response_json.get(key, [])
            for item in items:
                yield item
            
            next_page_token = response_json.get("nextPageToken")
            if not next_page_token:
                break
            current_params["pageToken"] = next_page_token


class SessionsResource(Resource):
    def get(self, name: str) -> Session:
        data = self._get(f"v1alpha/{name}")
        return Session.from_dict(data)

    def list(self, page_size: Optional[int] = None, filter: Optional[str] = None) -> Iterator[Session]:
        params = {}
        if page_size:
            params["pageSize"] = page_size
        if filter:
            params["filter"] = filter
        
        for item in self._paginate("v1alpha/sessions", "sessions", params):
            yield Session.from_dict(item)

    def create(self, session_body: Dict[str, Any]) -> Session:
         data = self._post("v1alpha/sessions", json=session_body)
         return Session.from_dict(data)

    def delete(self, name: str):
        self._delete(f"v1alpha/{name}")

    def send_message(self, session: str, body: Dict[str, Any]):
        return self._post(f"v1alpha/{session}:sendMessage", json=body)

    def approve_plan(self, session: str, body: Dict[str, Any]):
        return self._post(f"v1alpha/{session}:approvePlan", json=body)

    def archive(self, name: str):
        return self._post(f"v1alpha/{name}:archive")

    def unarchive(self, name: str):
        return self._post(f"v1alpha/{name}:unarchive")

    # Activities flattened under sessions
    def get_activity(self, name: str) -> Activity:
        # name is full resource name e.g. sessions/123/activities/456
        data = self._get(f"v1alpha/{name}")
        return Activity.from_dict(data)

    def list_activities(self, parent: str, page_size: Optional[int] = None, filter: Optional[str] = None) -> Iterator[Activity]:
        params = {}
        if page_size:
            params["pageSize"] = page_size
        if filter:
            params["filter"] = filter
            
        # The URL structure for listing activities is v1alpha/sessions/{session}/activities
        # parent should be "sessions/{session}"
        
        for item in self._paginate(f"v1alpha/{parent}/activities", "activities", params):
            yield Activity.from_dict(item)


class SourcesResource(Resource):
    def get(self, name: str) -> Source:
        data = self._get(f"v1alpha/{name}")
        return Source.from_dict(data)

    def list(self, page_size: Optional[int] = None, filter: Optional[str] = None) -> Iterator[Source]:
        params = {}
        if page_size:
            params["pageSize"] = page_size
        if filter:
            params["filter"] = filter
        
        for item in self._paginate("v1alpha/sources", "sources", params):
            yield Source.from_dict(item)
