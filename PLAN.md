# 🛰️ Orbit — GitHub Profile Analytics Tool
### Full Technical Plan

---

## 1. Product Vision

Navigate to `orbit.dev/torvalds` and instantly get a rich, visual, shareable analytics page for any public GitHub profile — built entirely from public data, no login required to view.

No AI. No chat. Pure aggregation + visualization, built to be fast, cached, and beautiful enough that people screenshot it and post it on Twitter/LinkedIn.

**Core idea:** GitHub shows you a contribution graph and a repo list. Orbit shows you the *story* behind that data — trends, breakdowns, comparisons, and patterns GitHub itself never surfaces.

**Who uses this:**
- Developers checking out their own stats / building a shareable profile card
- Recruiters/hiring managers getting a quick visual read on a candidate's activity
- Anyone curious about a maintainer's or contributor's footprint

---

## 2. System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Vue3 Frontend                       │
│       orbit.dev/:username → Profile Dashboard            │
└────────────────────┬────────────────────────────────────┘
                     │ Axios (REST)
┌────────────────────▼────────────────────────────────────┐
│                   Flask REST API                         │
│      /api/profile/:username    /api/profile/:u/refresh   │
└──────┬──────────────────────────────┬────────────────────┘
       │                              │
┌──────▼──────┐               ┌───────▼────────┐
│  PostgreSQL  │               │     Redis      │
│  Cached      │               │  Rate-limit    │
│  profiles +  │               │  tracking +    │
│  computed    │               │  short-term    │
│  metrics     │               │  response cache│
└─────────────┘               └────────────────┘
       │
       │ (cache miss or stale > 6hrs)
       ▼
┌─────────────────────────┐
│   GitHub GraphQL API     │  ← single authenticated token
│   (1 query, most data)   │     (server-owned, 5000 req/hr)
│   + REST API (fallback   │
│   for fields GraphQL     │
│   doesn't expose)        │
└─────────────────────────┘
       │
       ▼
┌─────────────────────────┐
│   Aggregation Engine      │
│   (Python, in Flask)      │
│   - Language breakdown    │
│   - Star/fork totals      │
│   - Commit time patterns  │
│   - Repo rankings         │
└─────────────────────────┘
```

**Key architectural decision:** Use **one server-owned GitHub PAT** (authenticated, 5,000 req/hr) for ALL lookups, never per-visitor unauthenticated calls. Unauthenticated requests are limited to 60 per hour while authenticated requests get 5,000 per hour — at public-tool scale, an unauthenticated approach would break almost immediately. Combine this with aggressive caching (PostgreSQL + Redis) so a popular profile is served from cache, not re-fetched on every visit.

---

## 3. Folder Structure

```
orbit/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extensions.py            # db, redis, cache
│   │   │
│   │   ├── models/
│   │   │   ├── profile.py           # CachedProfile
│   │   │   ├── repo_snapshot.py     # RepoSnapshot (per-repo data at fetch time)
│   │   │   └── fetch_log.py         # FetchLog (rate limit tracking, debugging)
│   │   │
│   │   ├── api/
│   │   │   ├── profile.py           # /api/profile/:username
│   │   │   └── meta.py              # /api/meta/og-image/:username (social share image)
│   │   │
│   │   ├── services/
│   │   │   ├── github_graphql.py    # Single GraphQL query for bulk of the data
│   │   │   ├── github_rest.py       # REST fallback calls (events, specific endpoints)
│   │   │   ├── aggregator.py        # All metric computation logic
│   │   │   ├── cache_service.py     # Read/write PostgreSQL + Redis cache
│   │   │   └── og_image_service.py  # Generate shareable preview image (Pillow/SVG)
│   │   │
│   │   └── tasks/
│   │       └── refresh_tasks.py     # Background refresh for popular profiles
│   │
│   ├── tests/
│   ├── run.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── router/index.js          # /:username dynamic route
│   │   ├── stores/profile.js        # Pinia: current profile data
│   │   ├── views/
│   │   │   ├── LandingView.vue      # orbit.dev/
│   │   │   └── ProfileView.vue      # orbit.dev/:username
│   │   ├── components/
│   │   │   ├── ProfileHeader.vue    # Avatar, name, bio, follower count
│   │   │   ├── StatCard.vue         # Single big number + label
│   │   │   ├── LanguageDonut.vue    # Language breakdown pie/donut chart
│   │   │   ├── ContributionHeatmap.vue  # Enhanced contribution calendar
│   │   │   ├── CommitTimePattern.vue    # Hour-of-day / day-of-week heatmap
│   │   │   ├── TopReposGrid.vue     # Top repos by stars/forks
│   │   │   ├── StarHistoryChart.vue # Cumulative stars over time
│   │   │   ├── RepoTypeBreakdown.vue # Original vs forked, by topic
│   │   │   ├── StreakCard.vue       # Current streak, longest streak
│   │   │   ├── ShareButton.vue      # Copy link / download share image
│   │   │   └── ProfileNotFound.vue
│   │   └── api/axios.js
│   └── package.json
│
├── docker-compose.yml
└── .env.example
```

---

## 4. Database Models (cache layer, not a user system)

### CachedProfile
```python
class CachedProfile(db.Model):
    id
    username                  # unique, indexed
    display_name
    avatar_url
    bio
    company
    location
    blog_url
    twitter_username
    follower_count
    following_count
    public_repo_count
    account_created_at
    total_stars_earned        # sum across all owned repos
    total_forks_received
    total_commits_last_year   # from contributionsCollection
    longest_streak_days
    current_streak_days
    top_language              # most-used by bytes
    language_breakdown        # JSON: {"Python": 45.2, "JS": 30.1, ...}
    metrics_json              # JSON: full computed metrics blob (see section 6)
    last_fetched_at
    fetch_count                # how many times this profile has been viewed/fetched
```

### RepoSnapshot
```python
class RepoSnapshot(db.Model):
    id
    profile_id                 # FK → CachedProfile
    repo_name
    full_name                  # owner/repo
    description
    is_fork
    primary_language
    languages_json             # JSON: byte breakdown for this repo
    stars
    forks
    watchers
    open_issues
    size_kb
    created_at
    pushed_at                  # last commit date
    topics                     # JSON list
```

### FetchLog
```python
class FetchLog(db.Model):
    id
    username
    fetch_type                 # full | partial | refresh
    api_calls_used
    success
    error_message
    duration_ms
    created_at
```

---

## 5. API Endpoints

```
GET    /api/profile/:username
  → Check cache (Postgres). If fresh (< 6hrs old): return immediately.
  → If stale or missing: fetch from GitHub, compute, cache, return.
  → Response: { profile, repos, metrics, cached_at }

POST   /api/profile/:username/refresh
  → Force refresh, bypasses cache (rate-limited per IP via Redis: 1/min)

GET    /api/meta/og-image/:username
  → Returns a generated PNG/SVG share-card image for social media previews
  → Cached aggressively (regenerate only when profile data changes)

GET    /api/health
  → Returns current GitHub API rate limit remaining (for monitoring)
```

**Caching strategy:**
- Redis: short-term (5 min) response cache to absorb traffic spikes on trending profiles
- PostgreSQL: long-term cache (6 hour TTL) as source of truth, survives restarts
- Popular profiles (high `fetch_count`) get proactively refreshed by a lightweight background task rather than waiting for a user request to trigger a stale-cache fetch

---

## 6. Comprehensive Metrics List (all from public data)

### A. Identity & Account Overview
| Metric | Source |
|---|---|
| Display name, bio, avatar, location, company, blog/website | REST `/users/:username` |
| Account age (years since `created_at`) | REST `/users/:username` |
| Follower / following count | REST `/users/:username` |
| Public repo count, public gist count | REST `/users/:username` |
| Hireable flag | REST `/users/:username` |
| Pinned repositories | GraphQL `pinnedItems` |
| Organizations they belong to (public) | REST `/users/:username/orgs` |

### B. Star & Fork Metrics
| Metric | Computation |
|---|---|
| Total stars earned | Sum of `stargazers_count` across all owned, non-fork repos |
| Total forks received | Sum of `forks_count` across all owned repos |
| Most-starred repo | Max by `stargazers_count` |
| Star-to-repo ratio | `total_stars / public_repo_count` (avg stars per repo) |
| Star history over time | GraphQL `stargazers(orderBy: STARRED_AT)` per repo, aggregated by month |
| Forking ratio | `% of owned repos that are forks of other projects` |

### C. Language Breakdown
| Metric | Computation |
|---|---|
| Language % across all repos | Sum `bytes` per language (REST `/repos/:owner/:repo/languages`) across all repos, normalize to % |
| Most-used language | Top by total bytes |
| Language count | Number of distinct languages used |
| Language trend over time | Bucket repos by `created_at` year, compute language % per year (shows evolution) |
| Niche language flag | Highlight unusual/rare languages used (fun fact, e.g. "uses Zig, top 2% of profiles") |

### D. Activity & Contribution Patterns
| Metric | Source |
|---|---|
| Contribution calendar (heatmap) | GraphQL `contributionsCollection.contributionCalendar` |
| Total contributions (last year) | GraphQL `contributionsCollection.contributionCalendar.totalContributions` |
| Current streak (consecutive days with a contribution) | Computed from calendar days |
| Longest streak ever | Computed from calendar days (requires year-by-year GraphQL calls) |
| Most active day of week | Bucket contribution days by weekday |
| Most active month | Bucket contribution days by month |
| Commit time-of-day pattern | REST `/repos/:owner/:repo/commits` → commit timestamps → hour-of-day histogram (sampled across top repos due to rate limits) |
| Night owl / early bird classification | Derived from commit time-of-day pattern |
| Weekday vs weekend commit ratio | Derived from contribution calendar |

### E. Repository-Level Aggregates
| Metric | Computation |
|---|---|
| Total repos (owned vs forked) | REST `/users/:username/repos` |
| Total combined repo size | Sum `size` field across all repos |
| Repos with open issues enabled | Count where `has_issues = true` |
| Average open issues per repo | Mean of `open_issues_count` |
| Most-forked repo | Max by `forks_count` |
| Most recently active repo | Max by `pushed_at` |
| Archived repo count | Count where `archived = true` |
| License breakdown | Count repos by `license.spdx_id`, show as donut |
| Topic cloud | Aggregate all `topics` across repos into a tag cloud |
| Repo creation timeline | Bucket `created_at` by year — shows growth of their portfolio over time |

### F. Collaboration & Social Signals
| Metric | Source |
|---|---|
| PRs opened (across GitHub, not just their repos) | GraphQL `contributionsCollection.pullRequestContributions` |
| PRs reviewed for others | GraphQL `contributionsCollection.pullRequestReviewContributions` |
| Issues opened | GraphQL `contributionsCollection.issueContributions` |
| Repos contributed to (not owned) | GraphQL `contributionsCollection.commitContributionsByRepository` |
| External contribution ratio | `% of contributions that are to repos they don't own` (signals OSS involvement vs solo projects) |
| Top collaborators | For their most-starred repo, list of contributors (REST `/repos/:owner/:repo/contributors`) |

### G. Fun / Shareable Derived Metrics
| Metric | Computation |
|---|---|
| "Coding personality" tag | Heuristic combining language diversity + commit time pattern + fork ratio (e.g. "Polyglot Night Owl", "OSS Contributor", "Solo Builder") |
| Profile percentile (stars, contributions) | Compare against a rough baseline distribution (optional, needs a reference dataset) |
| GitHub age in "dog years" | Just a fun framing of account age |
| Total lines changed (approx) | Sum additions+deletions from sampled recent commits across top repos |
| Busiest single day ever | Max contributions in a single day from the calendar |

---

## 7. Aggregation Engine Logic

```python
# aggregator.py — pseudocode for the core computation

def compute_profile_metrics(username, graphql_data, repos_data):
    metrics = {}

    # Language breakdown (needs per-repo language bytes — batched REST calls)
    lang_totals = {}
    for repo in repos_data:
        for lang, bytes_count in repo.languages.items():
            lang_totals[lang] = lang_totals.get(lang, 0) + bytes_count
    total_bytes = sum(lang_totals.values())
    metrics['language_breakdown'] = {
        lang: round(bytes_count / total_bytes * 100, 1)
        for lang, bytes_count in lang_totals.items()
    }

    # Stars / forks
    owned_repos = [r for r in repos_data if not r.is_fork]
    metrics['total_stars'] = sum(r.stars for r in owned_repos)
    metrics['total_forks_received'] = sum(r.forks for r in owned_repos)
    metrics['most_starred_repo'] = max(owned_repos, key=lambda r: r.stars)

    # Contribution streaks (from GraphQL calendar)
    days = graphql_data.contributionCalendar.days  # flat list, chronological
    metrics['current_streak'] = compute_current_streak(days)
    metrics['longest_streak'] = compute_longest_streak(days)
    metrics['most_active_weekday'] = bucket_by_weekday(days)

    # Coding personality heuristic
    metrics['personality_tag'] = derive_personality(
        language_count=len(lang_totals),
        external_contribution_ratio=metrics['external_contribution_ratio'],
        night_commit_ratio=metrics['night_owl_score']
    )

    return metrics
```

**Rate-limit-aware fetching strategy:**
- 1 GraphQL call gets: profile info, contribution calendar, PR/issue/review contribution counts, pinned repos — this is the highest-value single call
- 1 REST call gets the full repo list (paginated if > 100 repos)
- Per-repo language data requires 1 REST call **per repo** — this is the expensive part. **Cap it**: only fetch detailed language data for the top 30 repos by stars/recency, extrapolate the rest as "other"
- Commit time-of-day pattern: sample commits from only the top 5 most active repos, not all repos

This keeps a full profile fetch to roughly **35-40 API calls**, comfortably within the 5,000/hr authenticated budget — supports ~125 unique profile fetches per hour even with zero caching, and far more with caching in place.

---

## 8. Frontend Views

### Landing (`/`)
- Hero: "Your GitHub, visualized." + username input
- A few example profiles shown as live preview cards

### Profile View (`/:username`)
Single scrollable dashboard page:

1. **Header** — avatar, name, bio, location, follower count, "Joined GitHub in 2014" (account age)
2. **Stat row** — 4-5 StatCards: Total Stars, Total Repos, Current Streak, Total Contributions
3. **Contribution Heatmap** — enhanced version of GitHub's, with streak callouts
4. **Language Donut** — interactive, hover shows % and repo count per language
5. **Top Repos Grid** — cards for top 6 repos by stars, with description + language badge
6. **Commit Time Pattern** — hour-of-day × day-of-week heatmap ("you mostly code at 11pm on Tuesdays")
7. **Star History Chart** — cumulative stars over time, line chart
8. **Personality Card** — the fun derived tag, designed to be the most "screenshot-able" element
9. **Share button** — copies link, or downloads a generated share image

### Not Found (`/:username` → 404 state)
- Clean "We couldn't find @username on GitHub" message

---

## 9. Tech Stack Summary

| Layer | Technology |
|---|---|
| Backend Framework | Flask |
| Database | PostgreSQL + SQLAlchemy (cache layer) |
| Cache | Redis (short-term response cache) |
| GitHub Access | GraphQL API (primary) + REST API (language data, fallback) |
| Image generation | Pillow or `svg` templating (for share-card images) |
| Charts | Recharts / Chart.js (Vue wrapper) |
| Frontend | Vue3 + Pinia + Vue Router |
| HTTP Client | Axios |
| Containerization | Docker + docker-compose |

No Celery needed for the core flow — fetches happen synchronously on cache miss (they're fast: ~40 calls in parallel/batched). A lightweight scheduled task (cron or simple Celery Beat) can proactively refresh popular profiles, but it's optional polish, not core architecture.

---

## 10. Environment Variables

```env
# Flask
FLASK_SECRET_KEY=
DATABASE_URL=postgresql://...

# Redis
REDIS_URL=redis://localhost:6379/0

# GitHub — single server-owned token, never per-visitor
GITHUB_TOKEN=                  # PAT, public_repo scope only (read-only public data)

# Cache tuning
PROFILE_CACHE_TTL_HOURS=6
RESPONSE_CACHE_TTL_SECONDS=300
MAX_REPOS_FOR_LANGUAGE_DETAIL=30
```

---

## 11. Build Order (1 Week Sprint)

### Day 1 — Foundation + GraphQL Core Fetch
- [ ] Flask app factory, config
- [ ] CachedProfile, RepoSnapshot models
- [ ] github_graphql.py — single query for profile + contributions + pinned repos
- [ ] /api/profile/:username returns raw GraphQL data (no aggregation yet)
- [ ] Vue3 setup, dynamic `/:username` route

### Day 2 — Repo Data + Language Aggregation
- [ ] github_rest.py — paginated repo list fetch
- [ ] Per-repo language fetch (capped at top 30 repos)
- [ ] aggregator.py — language breakdown, stars/forks totals
- [ ] Cache write to PostgreSQL

### Day 3 — Contribution Patterns + Streaks
- [ ] Streak computation (current + longest) from contribution calendar
- [ ] Weekday/month activity bucketing
- [ ] Commit time-of-day sampling (top 5 repos)
- [ ] Personality tag heuristic

### Day 4 — Caching + Rate Limit Safety
- [ ] Redis short-term cache layer
- [ ] Cache-hit/miss logic in /api/profile/:username
- [ ] Rate limit monitoring (/api/health)
- [ ] FetchLog for debugging

### Day 5 — Frontend Core Views
- [ ] ProfileHeader, StatCard row
- [ ] ContributionHeatmap component
- [ ] LanguageDonut component
- [ ] TopReposGrid

### Day 6 — Frontend Polish + Charts
- [ ] CommitTimePattern heatmap
- [ ] StarHistoryChart
- [ ] Personality card (make this visually the star of the page)
- [ ] ShareButton + og-image generation endpoint

### Day 7 — Docker + README + Buffer
- [ ] docker-compose (flask + postgres + redis)
- [ ] README with setup + architecture
- [ ] Test against profiles with 0 repos, 1000+ repos, private-everything accounts (edge cases)

---

## 12. What Makes This Stand Out

1. **No AI crutch** — pure data engineering + visualization, shows you can ship a polished product without an LLM doing the heavy lifting.
2. **Rate-limit-aware architecture** — the whole design (single server token, capped per-repo calls, caching layers) is built around a real constraint, not naive "just call the API."
3. **GraphQL + REST hybrid** — uses each API where it's actually better suited, rather than defaulting to one.
4. **Shareable by design** — the og-image endpoint and "personality tag" are built specifically to make people want to post this.
5. **Edge case resilience** — handles users with 1000+ repos, zero repos, and private-everything profiles gracefully.
6. **Same dynamic URL pattern as Cortex** — `orbit.dev/username` mirrors `cortex.dev/owner/repo`, a nice consistent through-line across your projects.

---

*Start with Day 1. The single GraphQL query is the foundation — get it returning clean data before touching aggregation.*