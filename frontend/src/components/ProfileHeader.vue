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
        <svg viewBox="0 0 16 16" version="1.1" width="16" height="16" fill="currentColor">
          <path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.24 4.24a.751.751 0 0 1 .018 1.042l-1.25 1.25a2.002 2.002 0 0 0 2.83 2.83l2.5-2.5a1.998 1.998 0 0 0 0-2.83.75.75 0 0 1 1.06-1.06 3.502 3.502 0 0 1 0 4.95l-2.5 2.5a3.502 3.502 0 0 1-4.95 0 3.5 3.5 0 0 1 0-4.95l1.25-1.25a.75.75 0 0 1 1.04 0Z"></path>
        </svg>
        <span>Share Profile</span>
      </button>
      <a :href="`/api/meta/og-image/${profile.username}`" target="_blank" class="btn-sidebar btn-preview">
        <svg viewBox="0 0 16 16" version="1.1" width="16" height="16" fill="currentColor">
          <path d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25Zm9.5 8.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Zm-7.65 3.102a.75.75 0 0 1-.035-1.026l2.8-3a.75.75 0 0 1 1.053-.042l1.623 1.488 2.226-2.58a.75.75 0 0 1 1.107-.024l2.5 2.75a.75.75 0 0 1-1.104 1.016l-1.92-2.112-2.25 2.608a.75.75 0 0 1-1.077.035l-1.63-1.495-2.26 2.422a.75.75 0 0 1-1.038.005Z"></path>
        </svg>
        <span>Social Card</span>
      </a>
    </div>

    <p v-if="profile.bio" class="bio">{{ profile.bio }}</p>
    
    <!-- Followers Count -->
    <div class="followers-row">
      <span class="detail-icon">
        <svg viewBox="0 0 16 16" version="1.1" width="16" height="16" fill="currentColor">
          <path d="M2 5.5a3.5 3.5 0 1 1 5.898 2.549 5.508 5.508 0 0 1 3.034 4.084.75.75 0 1 1-1.482.235 4 4 0 0 0-7.9 0 .75.75 0 0 1-1.482-.236 5.507 5.507 0 0 1 3.102-4.083A3.493 3.493 0 0 1 2 5.5ZM5.5 3.5a2 2 0 1 0 0 4 2 2 0 0 0 0-4ZM12.5 8a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5Zm-1.898.549A3.493 3.493 0 0 1 12.5 2a5.508 5.508 0 0 1 3.034 4.084.75.75 0 1 1-1.482.235 4 4 0 0 0-3.185-3.185.75.75 0 0 1-.224-.549Z"></path>
        </svg>
      </span>
      <span class="followers-text">
        <strong>{{ profile.follower_count }}</strong> followers 
        <span class="divider-dot">•</span> 
        <strong>{{ profile.following_count }}</strong> following
      </span>
    </div>
    
    <!-- Details List -->
    <div class="details-list">
      <div v-if="profile.company" class="detail-item">
        <span class="detail-icon">
          <svg viewBox="0 0 16 16" version="1.1" width="16" height="16" fill="currentColor">
            <path d="M1.5 14.25c0 .138.112.25.25.25H4v-3.5a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.5h2.25a.25.25 0 0 1 .25-.25V1.75a.25.25 0 0 1-.25-.25H1.75a.25.25 0 0 1-.25.25v12.5Zm12-.25h1.75a.75.75 0 0 1 0 1.5h-10.5a.75.75 0 0 1 0-1.5h1v-3.5a1.75 1.75 0 0 1 1.75-1.75h3.5A1.75 1.75 0 0 1 11 10.5v3.5h1.25V5.75a.75.75 0 0 1 1.5 0ZM9.5 4a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5ZM2.75 3h1.5a.25.25 0 0 1 .25.25v1.5a.25.25 0 0 1-.25.25h-1.5a.25.25 0 0 1-.25-.25v-1.5a.25.25 0 0 1 .25-.25Zm3.5 0h1.5a.25.25 0 0 1 .25.25v1.5a.25.25 0 0 1-.25.25h-1.5a.25.25 0 0 1-.25-.25v-1.5a.25.25 0 0 1 .25-.25Zm-3.5 3.5h1.5a.25.25 0 0 1 .25.25v1.5a.25.25 0 0 1-.25.25h-1.5a.25.25 0 0 1-.25-.25v-1.5a.25.25 0 0 1 .25-.25Zm3.5 0h1.5a.25.25 0 0 1 .25.25v1.5a.25.25 0 0 1-.25.25h-1.5a.25.25 0 0 1-.25-.25v-1.5a.25.25 0 0 1 .25-.25Zm-3.5 3.5h1.5a.25.25 0 0 1 .25.25v1.5a.25.25 0 0 1-.25.25h-1.5a.25.25 0 0 1-.25-.25v-1.5a.25.25 0 0 1 .25-.25Zm3.5 0h1.5a.25.25 0 0 1 .25.25v1.5a.25.25 0 0 1-.25.25h-1.5a.25.25 0 0 1-.25-.25v-1.5a.25.25 0 0 1 .25-.25Z"></path>
          </svg>
        </span>
        <span>{{ profile.company }}</span>
      </div>
      <div v-if="profile.location" class="detail-item">
        <span class="detail-icon">
          <svg viewBox="0 0 16 16" version="1.1" width="16" height="16" fill="currentColor">
            <path d="M8 0c3.13 0 6 1.94 6 5.15 0 3.32-3.12 6.83-5.5 9.07a.75.75 0 0 1-1 0C5.12 11.98 2 8.47 2 5.15 2 1.94 4.87 0 8 0ZM3.5 5.15c0 2.45 2.37 5.5 4.5 7.42 2.13-1.92 4.5-4.97 4.5-7.42C12.5 2.82 10.36 1.5 8 1.5 5.64 1.5 3.5 2.82 3.5 5.15Zm4.5-1.9a1.75 1.75 0 1 1 0 3.5 1.75 1.75 0 0 1 0-3.5Z"></path>
          </svg>
        </span>
        <span>{{ profile.location }}</span>
      </div>
      <a v-if="profile.blog_url" :href="formatUrl(profile.blog_url)" target="_blank" class="detail-item link-item">
        <span class="detail-icon">
          <svg viewBox="0 0 16 16" version="1.1" width="16" height="16" fill="currentColor">
            <path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.24 4.24a.751.751 0 0 1 .018 1.042l-1.25 1.25a2.002 2.002 0 0 0 2.83 2.83l2.5-2.5a1.998 1.998 0 0 0 0-2.83.75.75 0 0 1 1.06-1.06 3.502 3.502 0 0 1 0 4.95l-2.5 2.5a3.502 3.502 0 0 1-4.95 0 3.5 3.5 0 0 1 0-4.95l1.25-1.25a.75.75 0 0 1 1.04 0Z"></path>
          </svg>
        </span>
        <span class="link-text">{{ cleanUrl(profile.blog_url) }}</span>
      </a>
      <a v-if="profile.twitter_username" :href="`https://twitter.com/${profile.twitter_username}`" target="_blank" class="detail-item link-item">
        <span class="detail-icon">
          <svg viewBox="0 0 16 16" version="1.1" width="16" height="16" fill="currentColor">
            <path d="M16 1.75a.25.25 0 0 0-.25-.25H12.5a3.75 3.75 0 0 0-3.75 3.75v3.25H5.75a.25.25 0 0 0-.25.25v1.5c0 .138.112.25.25.25H8.75v4.25a.25.25 0 0 0 .25.25h1.5a.25.25 0 0 0 .25-.25V10.5h3.25a.25.25 0 0 0 .25-.25v-1.5a.25.25 0 0 0-.25-.25H11V5.25a2.25 2.25 0 0 1 2.25-2.25h2.5a.25.25 0 0 0 .25-.25V1.75Z"></path>
          </svg>
        </span>
        <span class="link-text">@{{ profile.twitter_username }}</span>
      </a>
      <div class="detail-item joined-date">
        <span class="detail-icon">
          <svg viewBox="0 0 16 16" version="1.1" width="16" height="16" fill="currentColor">
            <path d="M4.75 0a.75.75 0 0 1 .75.75V2h5V.75a.75.75 0 0 1 1.5 0V2h1.25c.966 0 1.75.784 1.75 1.75v10.5A1.75 1.75 0 0 1 13.25 16H2.75A1.75 1.75 0 0 1 1 14.25V3.75C1 2.784 1.784 2 2.75 2H4V.75A.75.75 0 0 1 4.75 0ZM2.5 7.5v6.75c0 .138.112.25.25.25h10.5a.25.25 0 0 0 .25-.25V7.5Zm10.75-1.5V3.75a.25.25 0 0 0-.25-.25H2.75a.25.25 0 0 0-.25.25V6Z"></path>
          </svg>
        </span>
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
