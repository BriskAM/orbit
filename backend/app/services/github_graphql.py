import requests
from flask import current_app

def fetch_github_profile_raw(username):
    """
    Executes a single unified GraphQL query to retrieve:
    - User identity & account details
    - Pinned items (up to 6 repositories)
    - Top 50 repositories sorted by stars
    - Last year's contribution calendar
    
    Returns parsed dictionary of user details or None if user is not found.
    Raises ValueError if GITHUB_TOKEN is missing.
    Raises IOError if API request fails.
    """
    token = current_app.config.get('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN is not configured in the application environment.")
        
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    query = """
    query($username: String!) {
      user(login: $username) {
        name
        login
        avatarUrl
        bio
        company
        location
        websiteUrl
        twitterUsername
        followers {
          totalCount
        }
        following {
          totalCount
        }
        createdAt
        repositories(first: 50, orderBy: {field: STARGAZERS, direction: DESC}) {
          totalCount
          nodes {
            name
            nameWithOwner
            description
            isFork
            stargazerCount
            forkCount
            watchers {
              totalCount
            }
            diskUsage
            isArchived
            hasIssuesEnabled
            createdAt
            pushedAt
            primaryLanguage {
              name
            }
            repositoryTopics(first: 10) {
              nodes {
                topic {
                  name
                }
              }
            }
          }
        }
        pinnedItems(first: 6, types: [REPOSITORY]) {
          nodes {
            ... on Repository {
              name
              description
              stargazerCount
              forkCount
              primaryLanguage {
                name
              }
            }
          }
        }
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
                weekday
              }
            }
          }
        }
      }
    }
    """
    
    variables = {"username": username}
    
    try:
        response = requests.post(
            url, 
            json={"query": query, "variables": variables}, 
            headers=headers,
            timeout=10
        )
    except requests.exceptions.RequestException as e:
        raise IOError(f"Network error when contacting GitHub GraphQL API: {e}")
    
    if response.status_code != 200:
        raise IOError(f"GitHub GraphQL API returned status code {response.status_code}: {response.text}")
        
    data = response.json()
    
    # Check for errors in the GraphQL response
    if "errors" in data:
        for error in data["errors"]:
            # If the error is user not found, return None
            if error.get("type") == "NOT_FOUND" or "Could not resolve to a User" in error.get("message", ""):
                return None
        raise IOError(f"GitHub GraphQL error: {data['errors']}")
        
    if not data.get("data") or not data["data"].get("user"):
        return None
        
    return data["data"]["user"]
