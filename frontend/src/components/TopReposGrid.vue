<template>
  <div class="repos-section">
    <div class="section-header">
      <h3 class="section-title">Pinned</h3>
    </div>
    
    <div class="repos-grid">
      <div v-for="repo in top6Repos" :key="repo.id" class="repo-card">
        <div class="card-top">
          <div class="card-header-row">
            <div class="repo-title-wrapper">
              <!-- Book icon -->
              <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" fill="currentColor" class="repo-icon">
                <path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"></path>
              </svg>
              <a :href="`https://github.com/${repo.full_name || repo.name}`" target="_blank" class="repo-name-link">
                {{ repo.repo_name }}
              </a>
            </div>
            <span class="visibility-badge">Public</span>
          </div>
          
          <p v-if="repo.description" class="repo-desc">{{ repo.description }}</p>
          <p v-else class="repo-desc no-desc">No description provided.</p>
        </div>
        
        <div class="card-footer">
          <div class="footer-left">
            <div v-if="repo.primary_language" class="lang-item">
              <div class="lang-dot" :style="{ backgroundColor: getLangColor(repo.primary_language) }"></div>
              <span class="lang-text">{{ repo.primary_language }}</span>
            </div>
            <div v-else class="lang-item">
              <div class="lang-dot" style="background-color: var(--color-on-surface-variant)"></div>
              <span class="lang-text">Other</span>
            </div>
            
            <a v-if="repo.stars > 0" :href="`https://github.com/${repo.full_name || repo.name}/stargazers`" target="_blank" class="stat-item" title="Stars">
              <!-- Star icon -->
              <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" fill="currentColor" class="footer-icon">
                <path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.75.75 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"></path>
              </svg>
              <span class="stat-num">{{ repo.stars }}</span>
            </a>
            
            <a v-if="repo.forks > 0" :href="`https://github.com/${repo.full_name || repo.name}/forks`" target="_blank" class="stat-item" title="Forks">
              <!-- Fork icon -->
              <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" fill="currentColor" class="footer-icon">
                <path d="M5 3.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm0 2.122a2.25 2.25 0 1 0-1.5 0v.878A2.25 2.25 0 0 0 5.75 8.5h1.5v2.128a2.251 2.251 0 1 0 1.5 0V8.5h1.5A2.25 2.25 0 0 0 12.5 6.25v-.878a2.25 2.25 0 1 0-1.5 0v.878a.75.75 0 0 1-.75.75h-4.5A.75.75 0 0 1 5 6.25v-.878Zm3.75 7.378a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm3-8.5a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z"></path>
              </svg>
              <span class="stat-num">{{ repo.forks }}</span>
            </a>
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
  margin-bottom: 24px;
}

.section-header {
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-size: 16px;
  font-weight: 400;
  color: var(--color-on-surface);
}

.repos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}

.repo-card {
  background-color: var(--color-surface-container);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-default);
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 120px;
}

.card-top {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.repo-title-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.repo-icon {
  color: var(--color-on-surface-variant);
  flex-shrink: 0;
}

.repo-name-link {
  font-weight: 600;
  font-size: 14px;
  color: var(--color-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.repo-name-link:hover {
  text-decoration: underline;
}

.visibility-badge {
  font-size: 12px;
  color: var(--color-on-surface-variant);
  border: 1px solid var(--color-border-subtle);
  border-radius: 20px;
  padding: 0 7px;
  line-height: 18px;
}

.repo-desc {
  font-size: 12px;
  color: var(--color-on-surface-variant);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.no-desc {
  color: rgba(141, 150, 160, 0.4);
  font-style: italic;
}

.card-footer {
  margin-top: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.footer-left {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.lang-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.lang-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.lang-text {
  font-size: 12px;
  color: var(--color-on-surface-variant);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--color-on-surface-variant);
}

.stat-item:hover {
  color: var(--color-primary);
  text-decoration: none;
}

.footer-icon {
  color: var(--color-on-surface-variant);
}

.stat-item:hover .footer-icon {
  color: var(--color-primary);
}

.stat-num {
  font-size: 12px;
}
</style>
