from datetime import datetime

def calculate_metrics(repos_data, languages_by_repo, calendar_data=None, commit_timestamps=None):
    """
    Calculates aggregated metrics from repository list, language breakdowns,
    contribution calendar, and sampled commit timestamps.
    """
    metrics = {
        "total_stars_earned": 0,
        "total_forks_received": 0,
        "most_starred_repo": None,
        "language_breakdown": {},
        "top_language": None,
        
        # Day 3 metrics placeholders
        "current_streak": 0,
        "longest_streak": 0,
        "weekday_activity": [0] * 7, # Sun (0) to Sat (6)
        "month_activity": [0] * 12,   # Jan (0) to Dec (11)
        "commit_hour_histogram": [0] * 24, # 0 to 23
        "night_owl_ratio": 0.0,
        "early_bird_ratio": 0.0,
        "personality_tag": "Pragmatic Developer"
    }
    
    if not repos_data:
        return metrics
        
    # Helper to check if repository is a fork
    def is_repo_fork(r):
        return r.get('fork', r.get('isFork', False))
        
    # Helper to get stars
    def get_repo_stars(r):
        return r.get('stargazers_count', r.get('stargazerCount', 0))
        
    # Helper to get forks
    def get_repo_forks(r):
        return r.get('forks_count', r.get('forkCount', 0))

    # Calculate stars and forks
    owned_repos = [r for r in repos_data if not is_repo_fork(r)]
    metrics["total_stars_earned"] = sum(get_repo_stars(r) for r in owned_repos)
    metrics["total_forks_received"] = sum(get_repo_forks(r) for r in repos_data)
    
    if owned_repos:
        most_starred = max(owned_repos, key=get_repo_stars)
        if get_repo_stars(most_starred) > 0:
            metrics["most_starred_repo"] = most_starred.get('name')
            
    # Aggregate language bytes
    total_bytes_by_lang = {}
    for lang_bytes in languages_by_repo.values():
        for lang, byte_count in lang_bytes.items():
            total_bytes_by_lang[lang] = total_bytes_by_lang.get(lang, 0) + byte_count
            
    total_bytes = sum(total_bytes_by_lang.values())
    if total_bytes > 0:
        breakdown = {
            lang: round((count / total_bytes) * 100, 1)
            for lang, count in total_bytes_by_lang.items()
        }
        breakdown = {k: v for k, v in breakdown.items() if v > 0}
        
        sorted_breakdown = dict(
            sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
        )
        metrics["language_breakdown"] = sorted_breakdown
        metrics["top_language"] = max(total_bytes_by_lang, key=total_bytes_by_lang.get)
        
    # --- Day 3 Calculations ---
    
    # 1. Compute streaks and calendar activity from contribution calendar
    if calendar_data:
        weeks = calendar_data.get("weeks", [])
        days = []
        for w in weeks:
            for d in w.get("contributionDays", []):
                days.append(d)
        
        # Sort chronologically by date
        days = sorted(days, key=lambda x: x.get("date", ""))
        
        # Streaks
        longest = 0
        current = 0
        for d in days:
            if d.get("contributionCount", 0) > 0:
                current += 1
                longest = max(longest, current)
            else:
                current = 0
                
        metrics["longest_streak"] = longest
        
        # Current streak logic walking backwards
        last_active_idx = -1
        if days:
            if days[-1].get("contributionCount", 0) > 0:
                last_active_idx = len(days) - 1
            elif len(days) > 1 and days[-2].get("contributionCount", 0) > 0:
                last_active_idx = len(days) - 2
                
            if last_active_idx != -1:
                curr_run = 0
                for i in range(last_active_idx, -1, -1):
                    if days[i].get("contributionCount", 0) > 0:
                        curr_run += 1
                    else:
                        break
                metrics["current_streak"] = curr_run
                
        # Weekday and Month activity bucketing
        for d in days:
            count = d.get("contributionCount", 0)
            if count > 0:
                # Weekday
                wday = d.get("weekday")
                if wday is not None and 0 <= wday <= 6:
                    metrics["weekday_activity"][wday] += count
                    
                # Month
                date_str = d.get("date", "")
                try:
                    # format: "YYYY-MM-DD"
                    parts = date_str.split("-")
                    if len(parts) >= 2:
                        month_num = int(parts[1])
                        if 1 <= month_num <= 12:
                            metrics["month_activity"][month_num - 1] += count
                except Exception:
                    pass
                    
    # 2. Analyze commit timestamps
    if commit_timestamps:
        total_sampled = 0
        night_commits = 0
        early_bird_commits = 0
        
        for ts in commit_timestamps:
            if not ts or 'T' not in ts:
                continue
            try:
                # Extract local hour directly after 'T' (e.g. '2026-06-20T10:47:51+05:30' -> hour 10)
                time_part = ts.split('T')[1]
                hour = int(time_part[:2])
                if 0 <= hour <= 23:
                    metrics["commit_hour_histogram"][hour] += 1
                    total_sampled += 1
                    # Night Owl: 10 PM (22) to 4 AM (4)
                    if hour >= 22 or hour <= 4:
                        night_commits += 1
                    # Early Bird: 5 AM (5) to 9 AM (9)
                    elif 5 <= hour <= 9:
                        early_bird_commits += 1
            except Exception:
                pass
                
        if total_sampled > 0:
            metrics["night_owl_ratio"] = round(night_commits / total_sampled, 3)
            metrics["early_bird_ratio"] = round(early_bird_commits / total_sampled, 3)
            
    # 3. Derive personality tag
    metrics["personality_tag"] = derive_personality_tag(metrics)
    
    return metrics

def derive_personality_tag(metrics):
    """
    Heuristic rule engine to classify developer coding personality.
    """
    lang_count = len(metrics.get("language_breakdown", {}))
    night_owl = metrics.get("night_owl_ratio", 0.0)
    early_bird = metrics.get("early_bird_ratio", 0.0)
    total_stars = metrics.get("total_stars_earned", 0)
    
    if lang_count >= 5 and night_owl >= 0.4:
        return "Polyglot Night Owl"
    elif lang_count >= 5 and early_bird >= 0.4:
        return "Polyglot Early Bird"
    elif night_owl >= 0.45:
        return "Obsessive Night Owl"
    elif early_bird >= 0.45:
        return "Early Bird Builder"
    elif total_stars >= 500:
        return "Rockstar Maintainer"
    elif lang_count >= 4:
        return "Versatile Polyglot"
    elif lang_count == 1:
        top_lang = metrics.get("top_language", "Code")
        return f"{top_lang} Specialist"
    else:
        return "Pragmatic Developer"
