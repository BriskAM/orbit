<template>
  <div class="profile-container-outer">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p class="loading-text">Analyzing GitHub footprint...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="error-card">
        <div class="error-icon">⚠️</div>
        <h3>Analysis Failed</h3>
        <p>{{ error }}</p>
        <router-link to="/" class="retry-button">Try Another Username</router-link>
      </div>
    </div>

    <!-- Data Loaded State -->
    <div v-else-if="profile" class="profile-layout">
      <!-- Left Sidebar Column -->
      <div class="sidebar-col">
        <ProfileHeader :profile="profile.profile" @share="copyProfileLink" />
      </div>

      <!-- Right Main Column -->
      <div class="main-col">
        <!-- Tab Bar Navigation -->
        <div class="tabs-navigation">
          <button 
            @click="currentTab = 'overview'" 
            class="tab-btn" 
            :class="{ 'active': currentTab === 'overview' }"
          >
            <span class="tab-icon">📖</span> Overview
          </button>
          <button 
            @click="currentTab = 'repositories'" 
            class="tab-btn" 
            :class="{ 'active': currentTab === 'repositories' }"
          >
            <span class="tab-icon">📁</span> Repositories
            <span class="tab-badge" v-if="profile.repos">{{ profile.repos.length }}</span>
          </button>
          <button 
            @click="currentTab = 'analytics'" 
            class="tab-btn" 
            :class="{ 'active': currentTab === 'analytics' }"
          >
            <span class="tab-icon">📊</span> Analytics
          </button>
          <button 
            @click="currentTab = 'devmode'" 
            class="tab-btn" 
            :class="{ 'active': currentTab === 'devmode' }"
          >
            <span class="tab-icon">🛠️</span> Dev Mode
          </button>
        </div>

        <!-- Tab Contents -->
        <div class="tab-content-panel">
          
          <!-- 1. Overview Tab -->
          <div v-if="currentTab === 'overview'" class="tab-pane animate-fade">
            <!-- Profile README Box (Coding Persona) -->
            <div class="readme-box" v-if="profile.metrics">
              <div class="readme-header">
                <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" fill="currentColor" class="readme-header-icon">
                  <path d="M4 1.75C4 .784 4.784 0 5.75 0h5.586a.75.75 0 0 1 .53.22l2.914 2.914a.75.75 0 0 1 .22.53v8.586A1.75 1.75 0 0 1 13.25 14h-7.5A1.75 1.75 0 0 1 4 12.25Zm1.75-.25a.25.25 0 0 0-.25.25v10.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25V4.5h-3a.75.75 0 0 1-.75-.75v-3.5Zm3.5 8a.75.75 0 0 1 .75-.75h3a.75.75 0 0 1 0 1.5h-3a.75.75 0 0 1-.75-.75Zm0 3a.75.75 0 0 1 .75-.75h3a.75.75 0 0 1 0 1.5h-3a.75.75 0 0 1-.75-.75Z"></path>
                </svg>
                <span class="readme-filename">{{ profile.profile.username }} / README.md</span>
              </div>
              <div class="readme-content">
                <h2 class="readme-greeting">Hi, I'm {{ profile.profile.display_name || profile.profile.username }}! 👋</h2>
                <p class="readme-intro">
                  Welcome to my automated profile analysis overview. Based on my commit timings, repository metadata, and coding rhythms, I am classified as a:
                </p>
                
                <div class="readme-persona-card">
                  <h3 class="readme-persona-title">{{ profile.metrics.personality_tag || 'Pragmatic Developer' }}</h3>
                  
                  <div class="readme-persona-stats">
                    <div class="readme-p-stat">
                      <span class="p-bullet">🦉</span>
                      <span>Night Commit Ratio: <strong>{{ (profile.metrics.night_owl_ratio * 100).toFixed(1) }}%</strong></span>
                    </div>
                    <div class="readme-p-stat">
                      <span class="p-bullet">🌅</span>
                      <span>Early Bird Ratio: <strong>{{ (profile.metrics.early_bird_ratio * 100).toFixed(1) }}%</strong></span>
                    </div>
                    <div class="readme-p-stat">
                      <span class="p-bullet">🔥</span>
                      <span>Current Streak: <strong>{{ profile.metrics.current_streak }}</strong> days</span>
                    </div>
                    <div class="readme-p-stat">
                      <span class="p-bullet">🏆</span>
                      <span>Longest Streak: <strong>{{ profile.metrics.longest_streak }}</strong> days</span>
                    </div>
                    <div class="readme-p-stat">
                      <span class="p-bullet">⭐</span>
                      <span>Stars Earned: <strong>{{ profile.profile.total_stars_earned }}</strong></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Pinned Repositories Grid -->
            <TopReposGrid v-if="profile.repos && profile.repos.length" :repos="profile.repos" />

            <!-- Contribution Heatmap -->
            <ContributionHeatmap
              v-if="profile.profile.metrics_json?.contributionsCollection?.contributionCalendar"
              :calendar-data="profile.profile.metrics_json.contributionsCollection.contributionCalendar"
            />
          </div>

          <!-- 2. Repositories Tab -->
          <div v-if="currentTab === 'repositories'" class="tab-pane animate-fade">
            <div class="repo-list">
              <div v-for="repo in profile.repos" :key="repo.id" class="repo-list-row">
                <div class="repo-row-left">
                  <div class="repo-row-title-row">
                    <a :href="`https://github.com/${repo.full_name || repo.name}`" target="_blank" class="repo-row-name">
                      {{ repo.name }}
                    </a>
                    <span class="repo-row-visibility">Public</span>
                  </div>
                  <p v-if="repo.description" class="repo-row-desc">{{ repo.description }}</p>
                  <p v-else class="repo-row-desc no-desc-placeholder">No description provided.</p>
                  
                  <div class="repo-row-meta">
                    <span v-if="repo.primary_language" class="repo-meta-item">
                      <span class="repo-lang-dot" :style="{ backgroundColor: getLangColor(repo.primary_language) }"></span>
                      {{ repo.primary_language }}
                    </span>
                    <a v-if="repo.stars > 0" :href="`https://github.com/${repo.full_name || repo.name}/stargazers`" target="_blank" class="repo-meta-item link-meta">
                      ⭐ {{ repo.stars }}
                    </a>
                    <a v-if="repo.forks > 0" :href="`https://github.com/${repo.full_name || repo.name}/forks`" target="_blank" class="repo-meta-item link-meta">
                      🍴 {{ repo.forks }}
                    </a>
                    <span v-if="repo.created_at" class="repo-meta-item">
                      Created {{ formatUpdatedDate(repo.created_at) }}
                    </span>
                  </div>
                </div>
                <div class="repo-row-right">
                  <button class="github-star-mock-btn">
                    ⭐ Star
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 3. Analytics Tab -->
          <div v-if="currentTab === 'analytics'" class="tab-pane animate-fade">
            <!-- Language shares -->
            <div class="analytics-row" style="margin-bottom: 24px;">
              <LanguageDonut
                v-if="profile.profile.language_breakdown && Object.keys(profile.profile.language_breakdown).length"
                :language-breakdown="profile.profile.language_breakdown"
              />
            </div>

            <!-- Commits Timing & Stars Growth -->
            <div class="analytics-grid">
              <div class="analytics-col">
                <CommitTimePattern :commit-time-matrix="profile.metrics.commit_time_matrix" />
              </div>
              <div class="analytics-col">
                <StarHistoryChart :star-history="profile.metrics.star_history" />
              </div>
            </div>
          </div>

          <!-- 4. Developer Console Tab -->
          <div v-if="currentTab === 'devmode'" class="tab-pane animate-fade">
            <div class="raw-data-card">
              <pre class="json-code"><code>{{ JSON.stringify(profile, null, 2) }}</code></pre>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- Toast Notification Teleport -->
    <Teleport to="body">
      <div v-if="toast.visible" class="toast-notification">
        {{ toast.message }}
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useProfileStore } from '../stores/profile'

// Components
import ProfileHeader from '../components/ProfileHeader.vue'
import ContributionHeatmap from '../components/ContributionHeatmap.vue'
import TopReposGrid from '../components/TopReposGrid.vue'
import LanguageDonut from '../components/LanguageDonut.vue'
import CommitTimePattern from '../components/CommitTimePattern.vue'
import StarHistoryChart from '../components/StarHistoryChart.vue'

const props = defineProps({
  username: {
    type: String,
    required: true
  }
})

const store = useProfileStore()
const { profile, loading, error } = storeToRefs(store)

const currentTab = ref('overview')

// Toast State
const toast = ref({
  visible: false,
  message: ''
})

const copyProfileLink = async () => {
  try {
    await navigator.clipboard.writeText(window.location.href)
    showToast("Profile link copied to clipboard!")
  } catch (err) {
    showToast("Failed to copy link.")
  }
}

const showToast = (msg) => {
  toast.value.message = msg
  toast.value.visible = true
  setTimeout(() => {
    toast.value.visible = false
  }, 3000)
}

const formatUpdatedDate = (dateStr) => {
  if (!dateStr) return ''
  try {
    const d = new Date(dateStr)
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
  } catch (e) {
    return dateStr
  }
}

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

const loadData = () => {
  if (props.username) {
    store.fetchProfile(props.username)
    currentTab.value = 'overview'
  }
}

onMounted(loadData)
watch(() => props.username, loadData)
</script>

<style scoped>
.profile-container-outer {
  background-color: var(--color-background);
  min-height: 80vh;
}

.profile-layout {
  display: flex;
  max-width: var(--spacing-container-max);
  margin: 0 auto;
  padding: 32px var(--spacing-gutter);
  gap: 32px;
}

.sidebar-col {
  width: 296px;
  flex-shrink: 0;
}

.main-col {
  flex-grow: 1;
  min-width: 0;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(88, 166, 255, 0.1);
  border-top: 3px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

.loading-text {
  color: var(--color-on-surface-variant);
  font-size: 14px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Error State */
.error-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
}

.error-card {
  text-align: center;
  background: var(--color-surface-container);
  border: 1px solid var(--color-error);
  padding: 32px;
  border-radius: var(--rounded-md);
  max-width: 400px;
}

.error-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.error-card h3 {
  color: var(--color-error);
  font-size: 18px;
  margin-bottom: 8px;
}

.error-card p {
  color: var(--color-on-surface-variant);
  font-size: 13px;
  margin-bottom: 16px;
}

.retry-button {
  display: inline-block;
  font-weight: 600;
  text-decoration: none;
  background: var(--color-error-container);
  color: var(--color-on-error-container);
  padding: 6px 16px;
  border-radius: var(--rounded-sm);
  font-size: 13px;
  border: 1px solid rgba(240,246,252,0.1);
}

.retry-button:hover {
  filter: brightness(1.1);
  text-decoration: none;
}

/* Tabs Navigation */
.tabs-navigation {
  display: flex;
  border-bottom: 1px solid var(--color-border-subtle);
  margin-bottom: 16px;
  gap: 8px;
  overflow-x: auto;
}

.tab-btn {
  background: transparent;
  border: none;
  color: var(--color-on-surface-variant);
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  border-bottom: 2px solid transparent;
  transition: all 0.1s ease;
  white-space: nowrap;
}

.tab-btn:hover {
  border-bottom-color: rgba(141, 150, 160, 0.4);
  color: var(--color-on-surface);
}

.tab-btn.active {
  border-bottom-color: #f78166; /* GitHub Tab bottom border active orange */
  color: var(--color-on-surface);
  font-weight: 600;
}

.tab-badge {
  background-color: var(--color-surface-container-highest);
  border-radius: 20px;
  font-size: 12px;
  padding: 0 6px;
  color: var(--color-on-surface);
  font-weight: 500;
}

.tab-content-panel {
  padding-top: 8px;
}

/* Profile README Box */
.readme-box {
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  background-color: transparent;
  margin-bottom: 24px;
  overflow: hidden;
  text-align: left;
}

.readme-header {
  background-color: var(--color-surface-container);
  border-bottom: 1px solid var(--color-border-subtle);
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.readme-header-icon {
  color: var(--color-on-surface-variant);
}

.readme-filename {
  font-size: 12px;
  font-family: var(--font-mono);
  color: var(--color-on-surface);
}

.readme-content {
  padding: 24px;
}

.readme-greeting {
  font-size: 20px;
  font-weight: 600;
  border-bottom: 1px solid var(--color-border-subtle);
  padding-bottom: 8px;
  margin-bottom: 16px;
}

.readme-intro {
  font-size: 14px;
  color: var(--color-on-background);
  margin-bottom: 16px;
}

.readme-persona-card {
  background-color: var(--color-surface-container);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  padding: 20px;
}

.readme-persona-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--color-primary);
  margin-bottom: 16px;
  letter-spacing: -0.5px;
}

.readme-persona-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.readme-p-stat {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-on-surface);
}

.p-bullet {
  font-size: 16px;
}

/* Repositories Tab Content */
.repo-list {
  display: flex;
  flex-direction: column;
}

.repo-list-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid var(--color-border-subtle);
  padding: 24px 0;
  gap: 16px;
}

.repo-list-row:first-child {
  padding-top: 0;
}

.repo-row-left {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
  text-align: left;
}

.repo-row-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.repo-row-name {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-primary);
  text-decoration: none;
}

.repo-row-name:hover {
  text-decoration: underline;
}

.repo-row-visibility {
  font-size: 12px;
  color: var(--color-on-surface-variant);
  border: 1px solid var(--color-border-subtle);
  border-radius: 20px;
  padding: 0 7px;
  line-height: 18px;
}

.repo-row-desc {
  font-size: 14px;
  color: var(--color-on-surface-variant);
  line-height: 1.5;
  max-width: 600px;
}

.no-desc-placeholder {
  color: rgba(141, 150, 160, 0.4);
  font-style: italic;
}

.repo-row-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 12px;
  color: var(--color-on-surface-variant);
  flex-wrap: wrap;
}

.repo-meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--color-on-surface-variant);
}

.link-meta {
  color: var(--color-on-surface-variant);
}

.link-meta:hover {
  color: var(--color-primary);
  text-decoration: none;
}

.repo-lang-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.github-star-mock-btn {
  background-color: var(--color-surface-container-high);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-sm);
  color: var(--color-on-surface);
  padding: 3px 12px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
}

.github-star-mock-btn:hover {
  background-color: var(--color-surface-container-highest);
}

/* Analytics Tab Content */
.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 24px;
}

.analytics-col {
  min-width: 0;
}

/* Dev Mode Tab Content */
.raw-data-card {
  background-color: var(--color-surface-container);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  padding: 16px;
  max-height: 600px;
  overflow-y: auto;
  text-align: left;
}

.json-code {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--color-tertiary);
  white-space: pre-wrap;
  word-break: break-all;
}

/* Toast Alerts */
.toast-notification {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background-color: var(--color-surface-container-highest);
  border: 1px solid var(--color-primary);
  color: var(--color-on-surface);
  padding: 12px 24px;
  border-radius: var(--rounded-sm);
  font-size: 13px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
  z-index: 9999;
  animation: toast-slide-up 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes toast-slide-up {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .profile-layout {
    flex-direction: column;
    gap: 24px;
    padding: 16px;
  }
  
  .sidebar-col {
    width: 100%;
  }
  
  .analytics-grid {
    grid-template-columns: 1fr;
  }
}

.animate-fade {
  animation: fade-in 0.2s ease;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
