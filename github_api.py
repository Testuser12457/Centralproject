import base64
import requests
import os

# يجب أن يكون لديك متغيرات البيئة GITHUB_TOKENS يحتوي على كل التوكنات الخاصة بكل حساب GitHub
# بصيغة JSON مثل: {"github_user1": "ghp_XXXX", "github_user2": "ghp_YYYY", ...}

GITHUB_TOKENS = json.loads(os.getenv("TOKENS_JSON", "{}"))


def get_auth_header(owner):
    token = GITHUB_TOKENS.get(owner)
    if not token:
        raise ValueError(f"No GitHub token found for owner: {owner}")
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }


def get_file_sha(owner, repo, path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = get_auth_header(owner)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["sha"]
    return None


def push_agent_config(owner, repo, path, content):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = get_auth_header(owner)

    encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    sha = get_file_sha(owner, repo, path)

    data = {
        "message": "Update agent config",
        "content": encoded_content,
        "branch": "main"
    }

    if sha:
        data["sha"] = sha

    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        print(f"✅ Pushed config to {owner}/{repo}")
    else:
        print(f"❌ Failed to push config to {owner}/{repo}: {response.status_code} - {response.text}")
