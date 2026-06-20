<template>
  <div class="profile-header-card">
    <div class="header-main">
      <img :src="profile.avatar_url" :alt="profile.display_name" class="avatar" />
      
      <div class="info-content">
        <div class="name-badge-row">
          <h2 class="display-name">{{ profile.display_name || profile.username }}</h2>
          <span v-if="profile.metrics_json?.personality_tag" class="personality-tag">
            {{ profile.metrics_json.personality_tag }}
          </span>
        </div>
        
        <p class="username">@{{ profile.username }}</p>
        
        <p class="meta-joined">
          🛰️ Joined GitHub in {{ formattedJoinedDate }} <span class="divider">•</span> {{ yearsOnGithub }} years active
        </p>
        
        <p v-if="profile.bio" class="bio">{{ profile.bio }}</p>
        
        <!-- Details row (Location, Blog, Twitter) -->
        <div class="details-row">
          <div v-if="profile.location" class="detail-item">
            <span class="detail-icon">📍</span>
            <span>{{ profile.location }}</span>
          </div>
          <div v-if="profile.company" class="detail-item">
            <span class="detail-icon">🏢</span>
            <span>{{ profile.company }}</span>
          </div>
          <a v-if="profile.blog_url" :href="formatUrl(profile.blog_url)" target="_blank" class="detail-item link-item">
            <span class="detail-icon">🔗</span>
            <span>{{ cleanUrl(profile.blog_url) }}</span>
          </a>
          <a v-if="profile.twitter_username" :href="`https://twitter.com/${profile.twitter_username}`" target="_blank" class="detail-item link-item">
            <span class="detail-icon">🐦</span>
            <span>@{{ profile.twitter_username }}</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  profile: {
    type: Object,
    required: true
  }
})

const formattedJoinedDate = computed(() => {
  if (!props.profile.account_created_at) return ''
  const date = new Date(props.profile.account_created_at)
  return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
})

const yearsOnGithub = computed(() => {
  if (!props.profile.account_created_at) return 0
  const created = new Date(props.profile.account_created_at)
  const diff = Date.now() - created.getTime()
  const years = diff / (1000 * 60 * 60 * 24 * 365.25)
  return years.toFixed(1)
})

const formatUrl = (url) => {
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  return `https://${url}`
}

const cleanUrl = (url) => {
  return url.replace(/https?:\/\/(www\.)?/, '')
}
</script>

<style scoped>
.profile-header-card {
  background: var(--color-glass-fill);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  padding: 2.5rem;
  backdrop-filter: blur(12px);
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.profile-header-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-secondary) 100%);
}

.header-main {
  display: flex;
  gap: 2.5rem;
  align-items: center;
  flex-wrap: wrap;
}

.avatar {
  width: 130px;
  height: 130px;
  border-radius: var(--rounded-full);
  border: 3px solid var(--color-primary);
  box-shadow: 0 0 25px rgba(221, 183, 255, 0.25);
  transition: all 0.3s ease;
  object-fit: cover;
}

.avatar:hover {
  transform: rotate(3deg) scale(1.05);
  box-shadow: 0 0 35px rgba(221, 183, 255, 0.4);
}

.info-content {
  flex: 1;
  min-width: 280px;
}

.name-badge-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.display-name {
  font-family: 'Quicksand', sans-serif;
  font-size: 2.4rem;
  font-weight: 700;
  color: var(--color-on-surface);
  line-height: 1.1;
}

.personality-tag {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.8rem;
  font-weight: 700;
  background: rgba(255, 176, 205, 0.1);
  border: 1px solid var(--color-tertiary);
  color: var(--color-tertiary);
  padding: 4px 14px;
  border-radius: var(--rounded-full);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.username {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.15rem;
  color: var(--color-secondary);
  margin-top: 0.25rem;
  margin-bottom: 0.75rem;
}

.meta-joined {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.95rem;
  color: rgba(228, 225, 233, 0.5);
  margin-bottom: 1.25rem;
}

.divider {
  margin: 0 6px;
  color: rgba(228, 225, 233, 0.2);
}

.bio {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 1.05rem;
  color: var(--color-on-surface-variant);
  line-height: 1.6;
  margin-bottom: 1.5rem;
  max-width: 800px;
}

.details-row {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.95rem;
  color: var(--color-on-surface-variant);
  text-decoration: none;
  transition: color 0.2s ease;
}

.detail-icon {
  font-size: 1.1rem;
}

.link-item {
  color: var(--color-primary);
}

.link-item:hover {
  color: var(--color-on-surface);
  text-decoration: underline;
}
</style>
