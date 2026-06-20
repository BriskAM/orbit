<template>
  <div class="repos-section">
    <h3 class="section-title">Top Repositories</h3>
    
    <div class="repos-grid">
      <div v-for="repo in top6Repos" :key="repo.id" class="repo-card">
        <div class="card-header">
          <h4 class="repo-name">{{ repo.repo_name }}</h4>
          <span v-if="repo.is_fork" class="fork-badge">Fork</span>
        </div>
        
        <p v-if="repo.description" class="repo-desc">{{ repo.description }}</p>
        <p v-else class="repo-desc no-desc">No description provided.</p>
        
        <!-- Topics -->
        <div v-if="repo.topics && repo.topics.length" class="topics-row">
          <span v-for="topic in repo.topics.slice(0, 3)" :key="topic" class="topic-chip">
            #{{ topic }}
          </span>
        </div>

        <div class="card-footer">
          <div v-if="repo.primary_language" class="lang-item">
            <div class="lang-dot" :style="{ backgroundColor: getLangColor(repo.primary_language) }"></div>
            <span class="lang-text">{{ repo.primary_language }}</span>
          </div>
          <div v-else class="lang-item">
            <div class="lang-dot" style="background-color: var(--color-on-surface-variant)"></div>
            <span class="lang-text">Other</span>
          </div>
          
          <div class="stats-row">
            <span class="stat-item" title="Stars">
              ⭐ <span class="stat-num">{{ repo.stars }}</span>
            </span>
            <span class="stat-item" title="Forks">
              🍴 <span class="stat-num">{{ repo.forks }}</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  repos: {
    type: Array,
    required: true
  }
})

const top6Repos = computed(() => {
  // Take top 6 repositories (already pre-sorted by stars desc from the API)
  return props.repos.slice(0, 6)
})

// Standard language colors mapping
const LANGUAGE_COLORS = {
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

const getLangColor = (lang) => {
  if (!lang) return 'var(--color-primary)'
  return LANGUAGE_COLORS[lang.toLowerCase()] || 'var(--color-primary)'
}
</script>

<style scoped>
.repos-section {
  margin-bottom: 2.5rem;
}

.section-title {
  font-family: 'Quicksand', sans-serif;
  font-size: 1.4rem;
  color: var(--color-on-surface);
  margin-bottom: 1.5rem;
  text-align: left;
}

.repos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.repo-card {
  background: var(--color-glass-fill);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-default);
  padding: 1.5rem;
  backdrop-filter: blur(12px);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 190px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.repo-card:hover {
  transform: scale(1.025) translateY(-2px);
  border-color: var(--color-primary);
  box-shadow: 0 10px 30px rgba(183, 109, 255, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.repo-name {
  font-family: 'Quicksand', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-on-surface);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 80%;
}

.fork-badge {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.7rem;
  font-weight: 700;
  background: rgba(93, 230, 255, 0.1);
  border: 1px solid var(--color-secondary);
  color: var(--color-secondary);
  padding: 2px 8px;
  border-radius: var(--rounded-full);
  text-transform: uppercase;
}

.repo-desc {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.9rem;
  color: var(--color-on-surface-variant);
  line-height: 1.5;
  margin-bottom: 1.25rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-grow: 1;
}

.no-desc {
  color: rgba(228, 225, 233, 0.3);
  font-style: italic;
}

.topics-row {
  display: flex;
  gap: 8px;
  margin-bottom: 1.25rem;
  flex-wrap: wrap;
}

.topic-chip {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  background: rgba(255, 176, 205, 0.08);
  border: 1px solid rgba(255, 176, 205, 0.2);
  color: var(--color-tertiary);
  padding: 2px 10px;
  border-radius: var(--rounded-full);
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--color-border-subtle);
  padding-top: 0.75rem;
  margin-top: auto;
}

.lang-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.lang-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.lang-text {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.85rem;
  color: var(--color-on-surface-variant);
}

.stats-row {
  display: flex;
  gap: 12px;
}

.stat-item {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  color: var(--color-on-surface-variant);
  display: flex;
  align-items: center;
  gap: 3px;
}

.stat-num {
  font-weight: 700;
  color: var(--color-on-surface);
}
</style>
