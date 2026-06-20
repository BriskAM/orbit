from backend.app.services.aggregator import calculate_metrics

def test_calculate_metrics_basic():
    # Mock repos list
    repos = [
        {"name": "repo1", "full_name": "owner/repo1", "stargazers_count": 10, "forks_count": 2, "fork": False},
        {"name": "repo2", "full_name": "owner/repo2", "stargazers_count": 20, "forks_count": 5, "fork": False},
        {"name": "repo3-fork", "full_name": "owner/repo3-fork", "stargazers_count": 100, "forks_count": 1, "fork": True},
    ]
    
    # Mock languages by repo
    languages = {
        "owner/repo1": {"Python": 1000, "JavaScript": 500},
        "owner/repo2": {"Python": 2000},
        "owner/repo3-fork": {"C++": 500}
    }
    
    metrics = calculate_metrics(repos, languages)
    
    # Stars should exclude the fork (so repo1 + repo2 = 10 + 20 = 30)
    assert metrics["total_stars_earned"] == 30
    
    # Forks count across all repos (2 + 5 + 1 = 8)
    assert metrics["total_forks_received"] == 8
    
    # Most starred owned repo should be repo2
    assert metrics["most_starred_repo"] == "repo2"
    
    # Total bytes: Python = 3000, JavaScript = 500, C++ = 500. Total = 4000.
    assert metrics["top_language"] == "Python"
    
    # Percentages: Python = 75.0%, JS = 12.5%, C++ = 12.5%
    assert metrics["language_breakdown"]["Python"] == 75.0
    assert metrics["language_breakdown"]["JavaScript"] == 12.5
    assert metrics["language_breakdown"]["C++"] == 12.5

def test_calculate_metrics_empty():
    metrics = calculate_metrics([], {})
    assert metrics["total_stars_earned"] == 0
    assert metrics["total_forks_received"] == 0
    assert metrics["most_starred_repo"] is None
    assert metrics["language_breakdown"] == {}
    assert metrics["top_language"] is None

if __name__ == "__main__":
    test_calculate_metrics_basic()
    test_calculate_metrics_empty()
    print("All aggregator tests passed successfully!")
