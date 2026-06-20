def calculate_metrics(repos_data, languages_by_repo):
    """
    Calculates aggregated metrics from repository data and pre-fetched language breakdowns.
    
    :param repos_data: List of repo dictionaries (from REST API or parsed GraphQL)
    :param languages_by_repo: Dictionary mapping full_name -> languages dict (e.g. {"Python": 1200})
    :return: A dictionary containing:
        - total_stars_earned
        - total_forks_received
        - most_starred_repo
        - language_breakdown (sorted dict of percentages, e.g. {"Python": 60.5})
        - top_language
    """
    metrics = {
        "total_stars_earned": 0,
        "total_forks_received": 0,
        "most_starred_repo": None,
        "language_breakdown": {},
        "top_language": None,
    }
    
    if not repos_data:
        return metrics
        
    # Helper to check if repository is a fork
    # Handles both REST ('fork') and GraphQL ('isFork') formats
    def is_repo_fork(r):
        return r.get('fork', r.get('isFork', False))
        
    # Helper to get stars
    def get_repo_stars(r):
        return r.get('stargazers_count', r.get('stargazerCount', 0))
        
    # Helper to get forks
    def get_repo_forks(r):
        return r.get('forks_count', r.get('forkCount', 0))

    # We sum stars and forks only across owned repositories (exclude forks)
    owned_repos = [r for r in repos_data if not is_repo_fork(r)]
    
    metrics["total_stars_earned"] = sum(get_repo_stars(r) for r in owned_repos)
    metrics["total_forks_received"] = sum(get_repo_forks(r) for r in repos_data) # Forks received is typically counted across all repos
    
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
        # Calculate percentages
        breakdown = {
            lang: round((count / total_bytes) * 100, 1)
            for lang, count in total_bytes_by_lang.items()
        }
        # Filter out negligible languages (e.g. < 0.1%)
        breakdown = {k: v for k, v in breakdown.items() if v > 0}
        
        # Sort breakdown by percentage descending
        sorted_breakdown = dict(
            sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
        )
        metrics["language_breakdown"] = sorted_breakdown
        
        # Determine top language
        metrics["top_language"] = max(total_bytes_by_lang, key=total_bytes_by_lang.get)
        
    return metrics
