<template>
  <div class="landing-container animate-fade">
    <div class="search-box-card">
      <div class="search-header">
        <!-- Orbit Custom Logo SVG -->
        <svg height="48" viewBox="0 0 24 24" width="48" fill="none" stroke="currentColor" stroke-width="2" class="orbit-logo">
          <circle cx="12" cy="12" r="10" stroke-dasharray="3 3" />
          <circle cx="12" cy="12" r="6" />
          <circle cx="12" cy="6" r="2" fill="currentColor" />
          <circle cx="6" cy="12" r="1.5" fill="currentColor" />
          <circle cx="18" cy="12" r="1.5" fill="currentColor" />
        </svg>
        <h1 class="search-title">Orbit Profile Analytics</h1>
        <p class="search-subtitle-top">Visualize and audit developer footprint metrics</p>
      </div>

      <form @submit.prevent="handleSubmit" class="search-form">
        <div class="form-group">
          <label for="username" class="input-label">GitHub Username</label>
          <input
            v-model="username"
            id="username"
            type="text"
            placeholder="e.g. torvalds, octocat"
            class="username-input"
            required
            :disabled="loading"
            autocomplete="off"
            autofocus
          />
        </div>

        <button type="submit" class="submit-button" :disabled="loading">
          <span v-if="loading">Fetching footprints...</span>
          <span v-else>Visualize Profile</span>
        </button>
      </form>
    </div>

    <div class="quick-links-box">
      <span class="examples-label">Try these profiles:</span>
      <div class="examples-chips">
        <button @click="quickSearch('torvalds')" class="example-link">@torvalds</button>
        <span class="divider">•</span>
        <button @click="quickSearch('octocat')" class="example-link">@octocat</button>
        <span class="divider">•</span>
        <button @click="quickSearch('yyx990803')" class="example-link">@yyx990803</button>
      </div>
    </div>

    <!-- Orbit Global Statistics Dashboard -->
    <div v-if="stats && stats.total_profiles > 0" class="global-stats-section">
      <h2 class="stats-section-title">Orbit Ecosystem Analytics</h2>
      <p class="stats-section-subtitle">Aggregated developer footprints indexed across the platform</p>
      
      <div class="stats-grid">
        <!-- Card 1: Indexed Users -->
        <div class="stats-card">
          <div class="stats-card-header">
            <svg class="card-icon icon-blue" viewBox="0 0 16 16" version="1.1" width="18" height="18" fill="currentColor">
              <path d="M2 5.5a3.5 3.5 0 1 1 5.898 2.549 5.508 5.508 0 0 1 3.034 4.084.75.75 0 1 1-1.482.235 4 4 0 0 0-7.9 0 .75.75 0 0 1-1.482-.236 5.507 5.507 0 0 1 3.102-4.083A3.493 3.493 0 0 1 2 5.5ZM5.5 3.5a2 2 0 1 0 0 4 2 2 0 0 0 0-4ZM12.5 8a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5Zm-1.898.549A3.493 3.493 0 0 1 12.5 2a5.508 5.508 0 0 1 3.034 4.084.75.75 0 1 1-1.482.235 4 4 0 0 0-3.185-3.185.75.75 0 0 1-.224-.549Z"></path>
            </svg>
            <span class="card-title">Indexed Users</span>
          </div>
          <div class="card-value">{{ stats.total_profiles }}</div>
          <div class="card-desc">Profiles analyzed in Orbit cache</div>
        </div>

        <!-- Card 2: Indexed Repositories -->
        <div class="stats-card">
          <div class="stats-card-header">
            <svg class="card-icon icon-green" viewBox="0 0 16 16" version="1.1" width="18" height="18" fill="currentColor">
              <path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.25.25 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"></path>
            </svg>
            <span class="card-title">Indexed Repos</span>
          </div>
          <div class="card-value">{{ stats.total_repos }}</div>
          <div class="card-desc">Average of {{ stats.avg_repos }} repos per profile</div>
        </div>

        <!-- Card 3: Accumulated Stars -->
        <div class="stats-card">
          <div class="stats-card-header">
            <svg class="card-icon icon-yellow" viewBox="0 0 16 16" version="1.1" width="18" height="18" fill="currentColor">
              <path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97 1.9 4.167a.75.75 0 0 1-1.087.79L8 11.777l-3.766 1.98a.75.75 0 0 1-1.087-.79l1.9-4.167L1.001 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45(2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.695Z"></path>
            </svg>
            <span class="card-title">Accumulated Stars</span>
          </div>
          <div class="card-value">{{ formatBigNumber(stats.total_stars) }}</div>
          <div class="card-desc">Total stars earned by cached users</div>
        </div>

        <!-- Card 4: Ecosystem Habits -->
        <div class="stats-card wide-card">
          <div class="stats-card-header">
            <svg class="card-icon icon-purple" viewBox="0 0 16 16" version="1.1" width="18" height="18" fill="currentColor">
              <path d="M1.5 1.75V13.5h13a.75.75 0 0 1 0 1.5H.75a.75.75 0 0 1-.75-.75V1.75a.75.75 0 0 1 1.5 0Zm4 5.5a.75.75 0 0 1 .75-.75h6a.75.75 0 0 1 .75.75v4.5a.75.75 0 0 1-.75.75h-6a.75.75 0 0 1-.75-.75v-4.5Zm1.5.75v3h4.5v-3h-4.5Z"></path>
            </svg>
            <span class="card-title">System-wide Developer Habits</span>
          </div>
          <div class="habits-list">
            <div class="habit-item">
              <span class="habit-label">Average Night Owl Ratio</span>
              <span class="habit-value">{{ (stats.avg_night_owl_ratio * 100).toFixed(1) }}%</span>
            </div>
            <div class="habit-item">
              <span class="habit-label">Average Early Bird Ratio</span>
              <span class="habit-value">{{ (stats.avg_early_bird_ratio * 100).toFixed(1) }}%</span>
            </div>
            <div class="habit-item">
              <span class="habit-label">Average Longest Streak</span>
              <span class="habit-value">{{ stats.avg_longest_streak }} days</span>
            </div>
          </div>
        </div>

        <!-- Card 5: Languages Share -->
        <div class="stats-card wide-card" v-if="Object.keys(stats.top_languages).length > 0">
          <div class="stats-card-header">
            <svg class="card-icon icon-red" viewBox="0 0 16 16" version="1.1" width="18" height="18" fill="currentColor">
              <path d="M10.22 1.72a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.75.75 0 0 1-1.06-1.06L13.94 6l-3.72-3.72a.75.75 0 0 1-.086-.116Zm-4.44 0a.75.75 0 0 1 0 1.06L2.06 6l3.72 3.72a.75.75 0 1 1-1.06 1.06L.47 6.53a.75.75 0 0 1 0-1.06l4.25-4.25a.75.75 0 0 1 1.06 0Z"></path>
            </svg>
            <span class="card-title">Top Primary Languages</span>
          </div>
          <div class="languages-distribution">
            <div v-for="(count, lang) in stats.top_languages" :key="lang" class="lang-pill">
              <span class="lang-dot" :style="{ backgroundColor: getLanguageColor(lang) }"></span>
              <span class="lang-name">{{ lang }}</span>
              <span class="lang-count">({{ count }} {{ count === 1 ? 'dev' : 'devs' }})</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const loading = ref(false)

const stats = ref(null)
const statsLoading = ref(true)

const loadStats = async () => {
  try {
    const res = await fetch('/api/meta/stats')
    if (res.ok) {
      stats.value = await res.json()
    }
  } catch (err) {
    console.error("Failed to fetch global stats:", err)
  } finally {
    statsLoading.value = false
  }
}

onMounted(loadStats)

const handleSubmit = () => {
  if (username.value.trim()) {
    loading.value = true
    router.push({ name: 'profile', params: { username: username.value.trim().toLowerCase() } })
  }
}

const quickSearch = (name) => {
  router.push({ name: 'profile', params: { username: name } })
}

const formatBigNumber = (num) => {
  if (!num) return '0'
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num.toString()
}

const getLanguageColor = (lang) => {
  if (!lang) return 'var(--color-primary)'
  const map = {
    python: '#3572A5',
    javascript: '#f1e05a',
    vue: '#41b883',
    typescript: '#3178c6',
    html: '#e34c26',
    css: '#563d7c',
    rust: '#dea584',
    go: '#00ADD8',
    cpp: '#f34b7d',
    c: '#a8b9cc',
    shell: '#89e051',
    ruby: '#701516',
    java: '#b07219'
  }
  return map[lang.toLowerCase()] || 'var(--color-primary)'
}
</script>

<style scoped>
.landing-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
  padding: 48px var(--spacing-gutter);
  background-color: var(--color-background);
}

.search-box-card {
  background-color: var(--color-surface-container);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  width: 100%;
  max-width: 360px;
  padding: 32px 24px;
  margin-bottom: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.search-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 28px;
}

.orbit-logo {
  color: var(--color-primary);
  margin-bottom: 16px;
  animation: pulse-slow 4s infinite ease-in-out;
}

@keyframes pulse-slow {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.05); opacity: 0.8; }
}

.search-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--color-on-surface);
  text-align: center;
  letter-spacing: -0.5px;
  margin-bottom: 6px;
}

.search-subtitle-top {
  font-size: 13px;
  color: var(--color-on-surface-variant);
  text-align: center;
  margin: 0;
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-on-surface-variant);
  text-align: left;
}

.username-input {
  background-color: var(--color-surface-container-lowest);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-sm);
  color: var(--color-on-background);
  padding: 8px 12px;
  font-size: 14px;
  outline: none;
  font-family: inherit;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.username-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15);
}

.submit-button {
  background-color: var(--color-secondary-container);
  color: #ffffff;
  border: 1px solid rgba(240, 246, 252, 0.1);
  border-radius: var(--rounded-sm);
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.1s ease;
}

.submit-button:hover:not(:disabled) {
  background-color: #2ea44f;
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.quick-links-box {
  background-color: transparent;
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  width: 100%;
  max-width: 360px;
  padding: 16px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.examples-label {
  font-size: 12px;
  color: var(--color-on-surface-variant);
}

.examples-chips {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.example-link {
  background: none;
  border: none;
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  padding: 0;
}

.example-link:hover {
  text-decoration: underline;
}

.divider {
  color: var(--color-on-surface-variant);
  font-size: 12px;
  user-select: none;
}

/* Global statistics dashboard styles */
.global-stats-section {
  width: 100%;
  max-width: 800px;
  margin-top: 56px;
  text-align: left;
  border-top: 1px solid var(--color-border-subtle);
  padding-top: 40px;
}

.stats-section-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--color-on-surface);
  margin-bottom: 6px;
}

.stats-section-subtitle {
  font-size: 13px;
  color: var(--color-on-surface-variant);
  margin-bottom: 28px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

.stats-card {
  background-color: var(--color-surface-container);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  padding: 20px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.wide-card {
  grid-column: span 1;
}

@media (min-width: 768px) {
  .wide-card {
    grid-column: span 2;
  }
}

.stats-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  color: var(--color-on-surface-variant);
}

.card-icon {
  flex-shrink: 0;
}

.icon-blue { color: #58a6ff; }
.icon-green { color: #3fb950; }
.icon-yellow { color: #d29922; }
.icon-purple { color: #bc8cff; }
.icon-red { color: #ff7b72; }

.card-title {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: var(--color-on-surface-variant);
}

.card-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-on-surface);
  margin-bottom: 8px;
  font-family: var(--font-mono);
}

.card-desc {
  font-size: 12px;
  color: var(--color-on-surface-variant);
}

.habits-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.habit-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  border-bottom: 1px solid rgba(240, 246, 252, 0.05);
  padding-bottom: 6px;
}

.habit-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.habit-label {
  color: var(--color-on-surface-variant);
}

.habit-value {
  font-weight: 600;
  color: var(--color-on-surface);
}

.languages-distribution {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.lang-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  background-color: var(--color-surface-container-high);
  border: 1px solid var(--color-border-subtle);
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 12px;
}

.lang-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.lang-name {
  font-weight: 600;
  color: var(--color-on-surface);
}

.lang-count {
  color: var(--color-on-surface-variant);
}

.animate-fade {
  animation: fade-in 0.3s ease;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
