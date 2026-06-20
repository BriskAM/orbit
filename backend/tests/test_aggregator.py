from backend.app.services.aggregator import calculate_metrics, derive_personality_tag

def test_calculate_metrics_basic():
    repos = [
        {"name": "repo1", "full_name": "owner/repo1", "stargazers_count": 10, "forks_count": 2, "fork": False},
        {"name": "repo2", "full_name": "owner/repo2", "stargazers_count": 20, "forks_count": 5, "fork": False},
        {"name": "repo3-fork", "full_name": "owner/repo3-fork", "stargazers_count": 100, "forks_count": 1, "fork": True},
    ]
    languages = {
        "owner/repo1": {"Python": 1000, "JavaScript": 500},
        "owner/repo2": {"Python": 2000},
        "owner/repo3-fork": {"C++": 500}
    }
    
    metrics = calculate_metrics(repos, languages)
    assert metrics["total_stars_earned"] == 30
    assert metrics["total_forks_received"] == 8
    assert metrics["most_starred_repo"] == "repo2"
    assert metrics["top_language"] == "Python"
    assert metrics["language_breakdown"]["Python"] == 75.0

def test_streaks_and_bucketing():
    # Mock calendar data
    calendar = {
        "weeks": [
            {
                "contributionDays": [
                    {"contributionCount": 0, "date": "2026-06-01", "weekday": 1}, # Mon
                    {"contributionCount": 2, "date": "2026-06-02", "weekday": 2}, # Tue
                    {"contributionCount": 1, "date": "2026-06-03", "weekday": 3}, # Wed
                    {"contributionCount": 0, "date": "2026-06-04", "weekday": 4}, # Thu
                    {"contributionCount": 5, "date": "2026-06-05", "weekday": 5}, # Fri
                    {"contributionCount": 3, "date": "2026-06-06", "weekday": 6}, # Sat
                    {"contributionCount": 1, "date": "2026-06-07", "weekday": 0}, # Sun
                ]
            }
        ]
    }
    
    repos = [{"name": "r1", "full_name": "owner/r1", "stargazers_count": 5, "fork": False}]
    metrics = calculate_metrics(repos, {}, calendar_data=calendar)
    
    # Streaks:
    # Tue-Wed: streak of 2
    # Fri-Sun: streak of 3 (longest streak is 3)
    # Since Sun is the last day and has contributions, current streak is 3
    assert metrics["longest_streak"] == 3
    assert metrics["current_streak"] == 3
    
    # Weekday activity:
    # Tue (2): 2, Wed (3): 1, Fri (5): 5, Sat (6): 3, Sun (0): 1
    # weekday_activity = [Sun, Mon, Tue, Wed, Thu, Fri, Sat] = [1, 0, 2, 1, 0, 5, 3]
    assert metrics["weekday_activity"] == [1, 0, 2, 1, 0, 5, 3]
    
    # Month activity (June is index 5):
    # Total count = 2+1+5+3+1 = 12
    assert metrics["month_activity"][5] == 12

def test_commit_times_and_personality():
    # Commits with local offsets:
    # Verify we extract the local hour directly after 'T'
    commits = [
        "2026-06-20T23:15:00+05:30", # Hour 23 (Night Owl)
        "2026-06-20T22:45:00-08:00", # Hour 22 (Night Owl)
        "2026-06-20T00:30:00Z",      # Hour 00 (Night Owl)
        "2026-06-20T14:20:00+02:00", # Hour 14 (Daytime)
        "2026-06-20T06:10:00-05:00", # Hour 06 (Early Bird)
    ]
    
    repos = [{"name": "r1", "full_name": "owner/r1", "stargazers_count": 5, "fork": False}]
    metrics = calculate_metrics(repos, {}, commit_timestamps=commits)
    
    # 5 commits total, 3 in Night range (23, 22, 0), 1 in Early Bird (6), 1 in other (14)
    # Night Owl Ratio: 3/5 = 0.6
    # Early Bird Ratio: 1/5 = 0.2
    assert metrics["night_owl_ratio"] == 0.6
    assert metrics["early_bird_ratio"] == 0.2
    assert metrics["commit_hour_histogram"][23] == 1
    assert metrics["commit_hour_histogram"][22] == 1
    assert metrics["commit_hour_histogram"][0] == 1
    assert metrics["commit_hour_histogram"][6] == 1
    assert metrics["commit_hour_histogram"][14] == 1
    
    # Heuristic matching: Night Owl ratio >= 0.45 and < 5 languages -> Obsessive Night Owl
    assert metrics["personality_tag"] == "Obsessive Night Owl"

if __name__ == "__main__":
    test_calculate_metrics_basic()
    test_streaks_and_bucketing()
    test_commit_times_and_personality()
    print("All aggregator, streak, bucketing, and personality tests passed successfully!")
