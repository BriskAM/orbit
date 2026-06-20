import requests
from flask import current_app

def get_auth_headers():
    """
    Constructs the headers needed for GitHub API requests.
    Loads GITHUB_TOKEN from application config.
    """
    token = current_app.config.get('GITHUB_TOKEN')
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def fetch_user_repos(username):
    """
    Fetches all public repositories for a user using paginated REST API calls.
    Returns a list of repository dictionaries or None if the user does not exist.
    """
    headers = get_auth_headers()
    repos = []
    page = 1
    
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
            raise IOError(f"Network error when fetching repositories: {e}")
            
        if response.status_code == 404:
            return None
        elif response.status_code != 200:
            raise IOError(f"GitHub REST API returned status code {response.status_code}: {response.text}")
            
        page_repos = response.json()
        if not page_repos:
            break
            
        repos.extend(page_repos)
        
        # If the page returned fewer than 100 items, we are at the last page
        if len(page_repos) < 100:
            break
            
        page += 1
        
    return repos

def fetch_repo_languages(owner, repo_name):
    """
    Fetches the language bytes breakdown for a specific repository.
    Returns a dictionary of language-name -> bytes (e.g. {"Python": 45012}).
    """
    headers = get_auth_headers()
    url = f"https://api.github.com/repos/{owner}/{repo_name}/languages"
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        current_app.logger.warning(f"Failed to fetch languages for {owner}/{repo_name}: {e}")
        return {}
        
    if response.status_code != 200:
        current_app.logger.warning(
            f"GitHub languages API returned status {response.status_code} for {owner}/{repo_name}"
        )
        return {}
        
    return response.json()

def fetch_recent_commits(owner, repo_name, username):
    """
    Fetches up to 30 recent commits authored by the specified user in a repository.
    Returns a list of commit dictionaries or an empty list on failure.
    """
    headers = get_auth_headers()
    url = f"https://api.github.com/repos/{owner}/{repo_name}/commits?author={username}&per_page=30"
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        current_app.logger.warning(f"Failed to fetch commits for {owner}/{repo_name}: {e}")
        return []
        
    if response.status_code != 200:
        current_app.logger.warning(
            f"GitHub commits API returned status {response.status_code} for {owner}/{repo_name}"
        )
        return []
        
    return response.json()
