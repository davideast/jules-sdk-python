
import os
import time
import jwt
import requests
from github import Github, GithubIntegration

# Configuration
APP_ID = os.environ["FLEET_APP_ID"]
PRIVATE_KEY = os.environ["FLEET_APP_PRIVATE_KEY_BASE64"]
INSTALLATION_ID = os.environ["FLEET_APP_INSTALLATION_ID"]
BRANCH_NAME = "fix-issue-6-jules-client"
BASE_BRANCH = "main"
REPO_OWNER = "google"
REPO_NAME = "jules-sdk-python"  # Inferred from common patterns or previous knowledge; checking current dir if needed.
# Actually, let's get the repo name from the current git config
import subprocess

def get_repo_full_name():
    try:
        remote_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode().strip()
        # Clean up URL to get owner/repo
        if "github.com" in remote_url:
            parts = remote_url.split("github.com/")[-1].replace(".git", "").split("/")
            return f"{parts[0]}/{parts[1]}"
    except Exception as e:
        print(f"Error getting repo name: {e}")
        return "google/jules-sdk-python" # Fallback guess

REPO_FULL_NAME = get_repo_full_name()
print(f"Targeting Repo: {REPO_FULL_NAME}")

def get_installation_access_token(app_id, private_key, installation_id):
    # Create JWT
    now = int(time.time())
    payload = {
        "iat": now,
        "exp": now + 600,
        "iss": app_id
    }
    encoded_jwt = jwt.encode(payload, private_key, algorithm="RS256")

    # Get Access Token
    headers = {
        "Authorization": f"Bearer {encoded_jwt}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.post(
        f"https://api.github.com/app/installations/{installation_id}/access_tokens",
        headers=headers
    )
    
    if response.status_code != 201:
        print(f"Error getting access token: {response.text}")
        exit(1)
        
    return response.json()["token"]

def push_changes(token, branch_name):
    # Configure git with token
    remote_url = f"https://x-access-token:{token}@github.com/{REPO_FULL_NAME}.git"
    
    # Check if branch exists locally
    try:
        subprocess.check_call(["git", "checkout", "-b", branch_name])
    except subprocess.CalledProcessError:
        subprocess.check_call(["git", "checkout", branch_name])
    
    # Add files
    subprocess.check_call(["git", "add", "."])
    
    # Commit (if needed)
    try:
        subprocess.check_call(["git", "commit", "-m", "Implement JulesClient for v1alpha API interaction\n\nFixes #6"])
    except subprocess.CalledProcessError:
        print("No changes to commit or commit failed.")
    
    # Push
    subprocess.check_call(["git", "push", remote_url, branch_name, "--force"])

def create_pull_request(token, repo_full_name, branch_name, base_branch):
    g = Github(token)
    repo = g.get_repo(repo_full_name)
    
    title = "Fixes #6: Implement JulesClient"
    body = """Implement JulesClient for v1alpha API interaction

Fixes #6

- Added `src/jules/client.py` with `JulesClient` implementation.
- Added `src/jules/models.py` with `Session`, `SessionState`, `Activity`, and `Source` dataclasses.
- Added `tests/test_client.py` with `respx` mocked tests.
- Added `requirements.txt` with `httpx`, `pytest`, `respx`.
- Implemented context manager support.
- Implemented pagination for `list_sessions` and `list_activities`.
- Implemented error handling.
"""
    
    # Check if PR already exists
    pulls = repo.get_pulls(state='open', head=f"{repo.owner.login}:{branch_name}")
    if pulls.totalCount > 0:
        print(f"PR already exists: {pulls[0].html_url}")
        return
        
    try:
        pr = repo.create_pull(
            title=title,
            body=body,
            head=branch_name,
            base=base_branch
        )
        print(f"PR Created: {pr.html_url}")
    except Exception as e:
        print(f"Error creating PR: {e}")

if __name__ == "__main__":
    # Decode private key (base64 to string)
    import base64
    private_key_bytes = base64.b64decode(PRIVATE_KEY + "=" * (-len(PRIVATE_KEY) % 4))
    private_key_str = private_key_bytes.decode('utf-8')
    
    print("Getting access token...")
    token = get_installation_access_token(APP_ID, private_key_str, INSTALLATION_ID)
    
    print("Pushing changes...")
    push_changes(token, BRANCH_NAME)
    
    print("Creating PR...")
    create_pull_request(token, REPO_FULL_NAME, BRANCH_NAME, BASE_BRANCH)
