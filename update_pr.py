import os
import sys
import base64
import time
import requests
import jwt

# Configuration
APP_ID = os.environ.get("FLEET_APP_ID")
INSTALLATION_ID = os.environ.get("FLEET_APP_INSTALLATION_ID")
PRIVATE_KEY_BASE64 = os.environ.get("FLEET_APP_PRIVATE_KEY_BASE64")
REPO_OWNER = "davideast"
REPO_NAME = "jules-sdk-python"
HEAD_BRANCH = "fix-issue-11-ci-workflow"

def get_jwt():
    key_str = PRIVATE_KEY_BASE64.strip()
    missing_padding = len(key_str) % 4
    if missing_padding:
        key_str += '=' * (4 - missing_padding)
    private_key = base64.b64decode(key_str)
    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + 600,
        "iss": APP_ID
    }
    return jwt.encode(payload, private_key, algorithm="RS256")

def get_installation_token(jwt_token):
    url = f"https://api.github.com/app/installations/{INSTALLATION_ID}/access_tokens"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()["token"]

def push_changes(token):
    remote_url = f"https://x-access-token:{token}@github.com/{REPO_OWNER}/{REPO_NAME}.git"
    print(f"Pushing updates to {HEAD_BRANCH}...")
    # Push the current branch to the remote HEAD_BRANCH
    cmd = f"git push {remote_url} HEAD:refs/heads/{HEAD_BRANCH} > /dev/null 2>&1"
    if os.system(cmd) != 0:
        print("Push failed. Trying with force...")
        cmd = f"git push --force {remote_url} HEAD:refs/heads/{HEAD_BRANCH} > /dev/null 2>&1"
        if os.system(cmd) != 0:
             raise Exception("Failed to push changes")

def main():
    try:
        jwt_token = get_jwt()
        token = get_installation_token(jwt_token)
        # Commit local changes first
        os.system('git add .github/workflows/ci.yml')
        # Check if there are changes to commit
        if os.system('git diff --staged --quiet') != 0:
            os.system('git commit -m "Fix CI workflow to handle missing project files"')
            push_changes(token)
            print("Updated PR.")
        else:
            print("No changes to commit.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
