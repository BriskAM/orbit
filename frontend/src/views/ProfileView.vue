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
      <p class="loading-text">Fetching data from GitHub...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="error-card">
        <div class="error-icon">⚠️</div>
        <h3>Failed to load profile</h3>
        <p>{{ error }}</p>
        <router-link to="/" class="retry-button">Try Another Username</router-link>
      </div>
    </div>

    <!-- Data Loaded State -->
    <div v-else-if="profile" class="profile-content">
      <!-- Profile Header Snapshot -->
      <div class="profile-card">
        <div class="profile-info">
          <img :src="profile.avatarUrl" :alt="profile.name" class="avatar" />
          <div class="meta">
            <h2 class="display-name">{{ profile.name || profile.login }}</h2>
            <p class="username">@{{ profile.login }}</p>
            <p v-if="profile.bio" class="bio">{{ profile.bio }}</p>
            
            <div class="stats-row">
              <div class="stat">
                <span class="stat-value">{{ profile.followers?.totalCount }}</span>
                <span class="stat-label">Followers</span>
              </div>
              <div class="stat">
                <span class="stat-value">{{ profile.following?.totalCount }}</span>
                <span class="stat-label">Following</span>
              </div>
              <div class="stat">
                <span class="stat-value">{{ profile.repositories?.totalCount }}</span>
                <span class="stat-label">Repos</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Raw GraphQL Data Viewer -->
      <div class="raw-data-section">
        <h3>🔍 Raw API Response (Day 1 Integration)</h3>
        <div class="raw-data-card">
          <pre class="json-code"><code>{{ JSON.stringify(profile, null, 2) }}</code></pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useProfileStore } from '../stores/profile'

const props = defineProps({
  username: {
    type: String,
    required: true
  }
})

const store = useProfileStore()
const { profile, loading, error } = storeToRefs(store)

const loadData = () => {
  if (props.username) {
    store.fetchProfile(props.username)
  }
}

onMounted(loadData)

// Reload if route changes (e.g. searching from sidebar or clicking back/forth)
watch(() => props.username, loadData)
</script>

<style scoped>
.profile-container {
  max-width: var(--spacing-container-max);
  margin: 0 auto;
  padding: var(--spacing-gutter);
}

.navigation-bar {
  margin-bottom: 2rem;
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
  min-height: 40vh;
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
  font-size: 1.1rem;
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
  min-height: 40vh;
}

.error-card {
  text-align: center;
  background: rgba(255, 180, 171, 0.05);
  border: 1px solid var(--color-error);
  padding: 2.5rem;
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
  font-size: 1.5rem;
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

/* Profile Card */
.profile-card {
  background: var(--color-glass-fill);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  padding: 2.5rem;
  margin-bottom: 2rem;
  backdrop-filter: blur(12px);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
}

.profile-info {
  display: flex;
  gap: 2rem;
  align-items: center;
  flex-wrap: wrap;
}

.avatar {
  width: 120px;
  height: 120px;
  border-radius: var(--rounded-full);
  border: 3px solid var(--color-primary);
  box-shadow: 0 0 20px rgba(221, 183, 255, 0.2);
}

.meta {
  flex: 1;
  min-width: 250px;
}

.display-name {
  font-family: 'Quicksand', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-on-surface);
  margin-bottom: 0.25rem;
}

.username {
  font-family: 'JetBrains Mono', monospace;
  color: var(--color-secondary);
  font-size: 1.05rem;
  margin-bottom: 0.75rem;
}

.bio {
  font-family: 'Be Vietnam Pro', sans-serif;
  color: var(--color-on-surface-variant);
  margin-bottom: 1.25rem;
  line-height: 1.5;
}

.stats-row {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.stat {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-primary);
}

.stat-label {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.8rem;
  color: rgba(228, 225, 233, 0.5);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: 0.25rem;
}

/* Raw Data Section */
.raw-data-section h3 {
  font-family: 'Quicksand', sans-serif;
  color: var(--color-on-surface);
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.raw-data-card {
  background: var(--color-surface-container-lowest);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  padding: 1.5rem;
  max-height: 500px;
  overflow-y: auto;
}

.json-code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.9rem;
  color: var(--color-secondary);
  white-space: pre-wrap;
  word-break: break-all;
}
</style>
