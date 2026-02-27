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
PR_NUMBER = 15

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

def get_pr_sha(token):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{PR_NUMBER}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["head"]["sha"]

def get_check_runs(token, sha):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits/{sha}/check-runs"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["check_runs"]

def main():
    try:
        jwt_token = get_jwt()
        token = get_installation_token(jwt_token)
        sha = get_pr_sha(token)
        runs = get_check_runs(token, sha)
        for run in runs:
            print(f"Check Run: {run['name']} - Status: {run['status']} - Conclusion: {run['conclusion']}")
            if run['conclusion'] == 'failure':
                output = run.get('output', {})
                print(f"Title: {output.get('title')}")
                print(f"Summary: {output.get('summary')}")
                print(f"Text: {output.get('text')}")
    except Exception as e:
        print(f"Error: {e}")
        # Print full response content on error for debugging
        if hasattr(e, 'response') and e.response:
             print(e.response.text)
        sys.exit(1)

if __name__ == "__main__":
    main()
