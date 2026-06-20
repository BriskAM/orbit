<template>
  <div class="profile-container">
    <!-- Back Button -->
    <div class="navigation-bar">
      <router-link to="/" class="back-button">
        ← Back to Search
      </router-link>
    </div>

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
    <div v-else-if="profile" class="profile-content">
      <!-- Profile Header Component -->
      <ProfileHeader :profile="profile.profile" />

      <!-- Stat Row -->
      <div class="stats-grid">
        <StatCard
          :value="profile.profile.total_stars_earned"
          label="Total Stars"
          color="primary"
          icon="⭐"
        />
        <StatCard
          :value="profile.profile.total_forks_received"
          label="Forks Received"
          color="secondary"
          icon="🍴"
        />
        <StatCard
          :value="profile.metrics.current_streak"
          label="Current Streak"
          color="tertiary"
          icon="🔥"
        />
        <StatCard
          :value="profile.metrics.longest_streak"
          label="Longest Streak"
          color="secondary"
          icon="🏆"
        />
      </div>

      <!-- Heatmap / Activity Calendar -->
      <ContributionHeatmap
        v-if="profile.profile.metrics_json?.contributionsCollection?.contributionCalendar"
        :calendar-data="profile.profile.metrics_json.contributionsCollection.contributionCalendar"
      />

      <!-- Middle Section: Languages & Personality -->
      <div class="mid-layout-row">
        <div class="mid-col">
          <LanguageDonut
            v-if="profile.profile.language_breakdown && Object.keys(profile.profile.language_breakdown).length"
            :language-breakdown="profile.profile.language_breakdown"
          />
          <div v-else class="empty-card">
            <h3>Language Breakdown</h3>
            <p>No repository language details found.</p>
          </div>
        </div>

        <!-- Coding Personality Card -->
        <div class="mid-col">
          <div class="personality-glow-card">
            <h3 class="personality-title">Coding Persona</h3>
            
            <div class="personality-value">
              {{ profile.metrics.personality_tag || 'Pragmatic Developer' }}
            </div>
            
            <p class="personality-desc">
              Heuristics generated from commit timings, star count, and language variety.
            </p>
            
            <div class="persona-stats-list">
              <div class="persona-stat">
                <span class="p-label">Night Commits Ratio:</span>
                <span class="p-val">{{ (profile.metrics.night_owl_ratio * 100).toFixed(1) }}%</span>
              </div>
              <div class="persona-stat">
                <span class="p-label">Early Bird Commits Ratio:</span>
                <span class="p-val">{{ (profile.metrics.early_bird_ratio * 100).toFixed(1) }}%</span>
              </div>
              <div class="persona-stat">
                <span class="p-label">Top Language byte share:</span>
                <span class="p-val text-primary">{{ profile.profile.top_language || 'N/A' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Top Repositories Grid -->
      <TopReposGrid v-if="profile.repos && profile.repos.length" :repos="profile.repos" />

      <!-- Raw API Data Viewer (Collapsible) -->
      <div class="raw-data-section">
        <button @click="showRawJson = !showRawJson" class="raw-json-toggle">
          {{ showRawJson ? 'Hide' : 'Show' }} Raw API Payload (Dev Mode)
        </button>
        
        <div v-if="showRawJson" class="raw-data-card animate-fade">
          <pre class="json-code"><code>{{ JSON.stringify(profile, null, 2) }}</code></pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useProfileStore } from '../stores/profile'

// Components
import ProfileHeader from '../components/ProfileHeader.vue'
import StatCard from '../components/StatCard.vue'
import ContributionHeatmap from '../components/ContributionHeatmap.vue'
import LanguageDonut from '../components/LanguageDonut.vue'
import TopReposGrid from '../components/TopReposGrid.vue'

const props = defineProps({
  username: {
    type: String,
    required: true
  }
})

const store = useProfileStore()
const { profile, loading, error } = storeToRefs(store)
const showRawJson = ref(false)

const loadData = () => {
  if (props.username) {
    store.fetchProfile(props.username)
  }
}

onMounted(loadData)
watch(() => props.username, loadData)
</script>

<style scoped>
.profile-container {
  max-width: var(--spacing-container-max);
  margin: 0 auto;
  padding: 2rem var(--spacing-gutter);
}

.navigation-bar {
  margin-bottom: 2rem;
  text-align: left;
}

.back-button {
  display: inline-block;
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  text-decoration: none;
  background: var(--color-glass-fill);
  border: 1px solid var(--color-border-subtle);
  color: var(--color-primary);
  padding: 10px 24px;
  border-radius: var(--rounded-full);
  transition: all 0.2s ease;
}

.back-button:hover {
  border-color: var(--color-primary);
  background: rgba(221, 183, 255, 0.1);
  transform: translateX(-4px);
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
  width: 50px;
  height: 50px;
  border: 4px solid rgba(93, 230, 255, 0.1);
  border-top: 4px solid var(--color-secondary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1.5rem;
}

.loading-text {
  font-family: 'Be Vietnam Pro', sans-serif;
  color: var(--color-on-surface-variant);
  font-size: 1.15rem;
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
  background: rgba(255, 180, 171, 0.04);
  border: 1px solid var(--color-error);
  padding: 3rem;
  border-radius: var(--rounded-md);
  max-width: 500px;
  backdrop-filter: blur(12px);
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-card h3 {
  font-family: 'Quicksand', sans-serif;
  color: var(--color-error);
  font-size: 1.6rem;
  margin-bottom: 0.5rem;
}

.error-card p {
  font-family: 'Be Vietnam Pro', sans-serif;
  color: var(--color-on-surface-variant);
  margin-bottom: 1.5rem;
}

.retry-button {
  display: inline-block;
  font-family: 'Be Vietnam Pro', sans-serif;
  font-weight: 600;
  text-decoration: none;
  background: var(--color-error-container);
  color: var(--color-on-error-container);
  padding: 10px 24px;
  border-radius: var(--rounded-full);
  transition: all 0.2s ease;
}

.retry-button:hover {
  transform: translateY(-2px);
  filter: brightness(1.1);
}

/* Profile Content Layout */
.profile-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  animation: page-fade 0.4s ease;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}

/* Mid Layoutsplit */
.mid-layout-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

@media (max-width: 500px) {
  .mid-layout-row {
    grid-template-columns: 1fr;
  }
}

.mid-col {
  height: 100%;
}

.empty-card {
  background: var(--color-glass-fill);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  padding: 2rem;
  text-align: center;
  backdrop-filter: blur(12px);
}

/* Coding Persona Card */
.personality-glow-card {
  background: var(--color-glass-fill);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  padding: 2rem;
  backdrop-filter: blur(12px);
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
}

.personality-glow-card::after {
  content: '';
  position: absolute;
  bottom: -40px;
  right: -40px;
  width: 150px;
  height: 150px;
  background: radial-gradient(circle, rgba(255, 176, 205, 0.1) 0%, rgba(0,0,0,0) 70%);
  filter: blur(20px);
  pointer-events: none;
}

.personality-title {
  font-family: 'Quicksand', sans-serif;
  font-size: 1.4rem;
  color: var(--color-on-surface);
  margin-bottom: 1.5rem;
}

.personality-value {
  font-family: 'Quicksand', sans-serif;
  font-size: 2.1rem;
  font-weight: 700;
  color: var(--color-tertiary);
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.personality-desc {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.95rem;
  color: var(--color-on-surface-variant);
  line-height: 1.5;
  margin-bottom: 2rem;
}

.persona-stats-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  border-top: 1px solid var(--color-border-subtle);
  padding-top: 1.25rem;
}

.persona-stat {
  display: flex;
  justify-content: space-between;
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.95rem;
}

.p-label {
  color: var(--color-on-surface-variant);
}

.p-val {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  color: var(--color-on-surface);
}

/* Raw Data Section */
.raw-data-section {
  margin-top: 2rem;
  text-align: left;
}

.raw-json-toggle {
  background: transparent;
  border: 1px dashed var(--color-border-subtle);
  color: var(--color-on-surface-variant);
  padding: 10px 20px;
  border-radius: var(--rounded-sm);
  cursor: pointer;
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.raw-json-toggle:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  background: var(--color-glass-fill);
}

.raw-data-card {
  background: var(--color-surface-container-lowest);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  padding: 1.5rem;
  margin-top: 1rem;
  max-height: 400px;
  overflow-y: auto;
}

.json-code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  color: var(--color-secondary);
  white-space: pre-wrap;
  word-break: break-all;
}

@keyframes page-fade {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade {
  animation: page-fade 0.2s ease;
}
</style>
