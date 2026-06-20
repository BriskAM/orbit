<template>
  <div class="profile-sidebar">
    <div class="avatar-wrapper">
      <img :src="profile.avatar_url" :alt="profile.display_name" class="avatar" />
    </div>
    
    <div class="name-container">
      <h2 class="display-name">{{ profile.display_name || profile.username }}</h2>
      <p class="username">{{ profile.username }}</p>
    </div>
    
    <!-- Share Controls directly in Sidebar -->
    <div class="share-actions-sidebar">
      <button @click="$emit('share')" class="btn-sidebar btn-share">
        🔗 Share Profile
      </button>
      <a :href="`/api/meta/og-image/${profile.username}`" target="_blank" class="btn-sidebar btn-preview">
        🖼️ Social Card
      </a>
    </div>

    <p v-if="profile.bio" class="bio">{{ profile.bio }}</p>
    
    <!-- Followers Count -->
    <div class="followers-row">
      <span class="followers-icon">👥</span>
      <span class="followers-text">
        <strong>{{ profile.follower_count }}</strong> followers 
        <span class="divider-dot">•</span> 
        <strong>{{ profile.following_count }}</strong> following
      </span>
    </div>
    
    <!-- Details List -->
    <div class="details-list">
      <div v-if="profile.company" class="detail-item">
        <span class="detail-icon">🏢</span>
        <span>{{ profile.company }}</span>
      </div>
      <div v-if="profile.location" class="detail-item">
        <span class="detail-icon">📍</span>
        <span>{{ profile.location }}</span>
      </div>
      <a v-if="profile.blog_url" :href="formatUrl(profile.blog_url)" target="_blank" class="detail-item link-item">
        <span class="detail-icon">🔗</span>
        <span class="link-text">{{ cleanUrl(profile.blog_url) }}</span>
      </a>
      <a v-if="profile.twitter_username" :href="`https://twitter.com/${profile.twitter_username}`" target="_blank" class="detail-item link-item">
        <span class="detail-icon">🐦</span>
        <span class="link-text">@{{ profile.twitter_username }}</span>
      </a>
      <div class="detail-item joined-date">
        <span class="detail-icon">📅</span>
        <span>Joined {{ formattedJoinedDate }}</span>
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

const emit = defineEmits(['share'])

const formattedJoinedDate = computed(() => {
  if (!props.profile.account_created_at) return ''
  const date = new Date(props.profile.account_created_at)
  return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
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
.profile-sidebar {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.avatar-wrapper {
  width: 100%;
  max-width: 296px;
  aspect-ratio: 1;
  border-radius: var(--rounded-full);
  overflow: hidden;
  border: 1px solid var(--color-border-subtle);
  background-color: var(--color-surface-container);
  margin-bottom: 16px;
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.name-container {
  padding: 16px 0;
  border-bottom: none;
}

.display-name {
  font-size: 26px;
  font-weight: 600;
  line-height: 1.25;
  color: var(--color-on-surface);
}

.username {
  font-size: 20px;
  font-weight: 300;
  line-height: 24px;
  color: var(--color-on-surface-variant);
}

.share-actions-sidebar {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.btn-sidebar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  font-size: 14px;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: var(--rounded-sm);
  cursor: pointer;
  text-decoration: none;
  text-align: center;
  transition: background-color 0.1s ease;
}

.btn-share {
  background-color: var(--color-surface-container-high);
  border: 1px solid var(--color-border-subtle);
  color: var(--color-on-surface);
}

.btn-share:hover {
  background-color: var(--color-surface-container-highest);
  text-decoration: none;
}

.btn-preview {
  background-color: transparent;
  border: 1px solid var(--color-border-subtle);
  color: var(--color-primary);
}

.btn-preview:hover {
  background-color: var(--color-surface-container-high);
  text-decoration: none;
}

.bio {
  font-size: 14px;
  color: var(--color-on-surface);
  line-height: 1.5;
  margin-bottom: 16px;
}

.followers-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--color-on-surface-variant);
  margin-bottom: 16px;
}

.followers-icon {
  font-size: 14px;
}

.divider-dot {
  margin: 0 4px;
}

.details-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  border-top: 1px solid var(--color-border-subtle);
  padding-top: 16px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--color-on-surface);
}

.detail-icon {
  width: 16px;
  text-align: center;
  color: var(--color-on-surface-variant);
  font-size: 14px;
}

.link-item {
  color: var(--color-on-surface);
}

.link-item:hover {
  color: var(--color-primary);
}

.link-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.joined-date {
  color: var(--color-on-surface-variant);
}
</style>
