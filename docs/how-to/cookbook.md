# Framework Integrations Cookbook

This cookbook provides specific, real-world examples of how to integrate the Jules SDK into various popular Python web frameworks. It focuses on the intersection of the SDK and the framework. If you need details on the underlying SDK methods, please see the [JulesClient Reference](../reference/client.md).

## Django: Management Command

A common pattern in Django is to trigger a long-running Jules session from a management command, perhaps via a cron job or external scheduler.

**`myapp/management/commands/run_jules.py`**

```python
import time
from django.core.management.base import BaseCommand
from jules import JulesClient
from jules.models import SessionState

class Command(BaseCommand):
    help = 'Kicks off a Jules session and waits for completion'

    def handle(self, *args, **options):
        self.stdout.write("Starting Jules session...")

        with JulesClient() as client:
            session = client.create_session(
                prompt="Update Django dependencies",
                source="github/myorg/myrepo"
            )
            self.stdout.write(f"Created session: {session.name}")

            # Simple polling mechanism
            while True:
                current = client.get_session(session.name)
                if current.state in (SessionState.COMPLETED, SessionState.FAILED, SessionState.CANCELLED):
                    self.stdout.write(self.style.SUCCESS(f"Finished with state: {current.state.value}"))
                    break
                time.sleep(5)
```

## Flask: Webhook Listener

If you configure Jules to send webhooks (or if you are polling and exposing the results), you might want a Flask endpoint to list recent activities for a given session.

**`app.py`**

```python
from flask import Flask, jsonify, abort
from jules import JulesClient, JulesAPIError

app = Flask(__name__)

@app.route('/api/sessions/<session_name>/activities', methods=['GET'])
def list_session_activities(session_name):
    try:
        with JulesClient() as client:
            activities = list(client.list_activities(session_name))

            # Convert Activity objects to dictionaries for JSON serialization
            return jsonify([activity.to_dict() for activity in activities])

    except JulesAPIError as e:
        if e.status_code == 404:
            abort(404, description=f"Session {session_name} not found")
        abort(500, description=str(e))

if __name__ == '__main__':
    app.run(port=5000)
```

## FastAPI: Async Wrapper

Because the Jules SDK is synchronous but FastAPI is asynchronous, you should run blocking SDK calls in a thread pool using FastAPI's `run_in_threadpool` or background tasks so you don't block the event loop.

**`main.py`**

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from jules import JulesClient
from jules.models import Session
from fastapi.concurrency import run_in_threadpool

app = FastAPI()

class SessionRequest(BaseModel):
    prompt: str
    source: str

def _create_jules_session(prompt: str, source: str) -> Session:
    with JulesClient() as client:
        return client.create_session(prompt=prompt, source=source)

@app.post("/sessions/")
async def create_session(request: SessionRequest):
    try:
        # Run the synchronous SDK call in a separate thread
        session = await run_in_threadpool(
            _create_jules_session,
            request.prompt,
            request.source
        )
        return {"session_name": session.name, "state": session.state.value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```
