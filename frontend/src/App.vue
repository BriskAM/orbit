<template>
  <div class="app-layout">
    <header class="app-header">
      <div class="header-container">
        <div class="header-left">
          <!-- GitHub Octocat Logo SVG -->
          <router-link to="/" class="logo">
            <svg height="32" aria-hidden="true" viewBox="0 0 16 16" version="1.1" width="32" data-view-component="true" fill="currentColor">
              <path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.35 3.12.87 0 .68.01 1.3.01 1.49 0 .21-.15.47-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"></path>
            </svg>
            <span class="logo-text">Orbit</span>
          </router-link>

          <!-- Top-bar global search box -->
          <form @submit.prevent="onSearchSubmit" class="header-search-form">
            <div class="search-input-wrapper">
              <input
                v-model="searchUsername"
                type="text"
                placeholder="Type username and press Enter..."
                class="header-search-input"
              />
              <span class="search-shortcut">/</span>
            </div>
          </form>

          <!-- Header Navigation links -->
          <nav class="header-nav">
            <router-link to="/" class="nav-link">Search</router-link>
            <a href="https://github.com/BriskAM/orbit" target="_blank" class="nav-link">Repository</a>
            <a href="https://github.com/trending" target="_blank" class="nav-link">Trending</a>
          </nav>
        </div>

        <div class="header-right">
          <!-- Mock profile/action icons for realism -->
          <span class="header-icon-btn">🔔</span>
          <span class="header-icon-btn">➕</span>
          <div class="mock-avatar"></div>
        </div>
      </div>
    </header>
    
    <main class="app-main">
      <router-view />
    </main>

    <footer class="app-footer">
      <div class="footer-container">
        <div class="footer-left">
          <span>🛰️ Orbit Profile Analytics</span>
        </div>
        <div class="footer-right">
          <a href="https://github.com/BriskAM/orbit" target="_blank">About</a>
          <a href="https://docs.github.com" target="_blank">GitHub API</a>
          <a href="https://github.com" target="_blank">GitHub.com</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchUsername = ref('')

const onSearchSubmit = () => {
  if (searchUsername.value.trim()) {
    router.push({ name: 'profile', params: { username: searchUsername.value.trim().toLowerCase() } })
    searchUsername.value = ''
  }
}
</script>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--color-background);
  color: var(--color-on-background);
}

.app-header {
  background-color: var(--color-surface-container);
  border-bottom: 1px solid var(--color-border-subtle);
  padding: 12px 24px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-container {
  max-width: var(--spacing-container-max);
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.logo {
  color: #f0f6fc;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 16px;
  transition: opacity 0.2s ease;
}

.logo:hover {
  text-decoration: none;
  opacity: 0.85;
}

.logo-text {
  font-weight: 600;
  color: #ffffff;
}

.header-search-form {
  max-width: 280px;
  width: 100%;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.header-search-input {
  width: 100%;
  background-color: var(--color-surface-container-lowest);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-sm);
  color: var(--color-on-background);
  padding: 5px 12px;
  font-size: 13px;
  outline: none;
  font-family: inherit;
  transition: width 0.2s ease, border-color 0.2s ease;
}

.header-search-input:focus {
  background-color: var(--color-background);
  border-color: var(--color-primary);
}

.search-shortcut {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  border: 1px solid var(--color-border-subtle);
  border-radius: 3px;
  padding: 1px 5px;
  font-size: 10px;
  color: var(--color-on-surface-variant);
  pointer-events: none;
}

.header-nav {
  display: flex;
  gap: 16px;
}

.nav-link {
  color: #ffffff;
  font-weight: 600;
  font-size: 14px;
}

.nav-link:hover {
  text-decoration: none;
  color: rgba(255, 255, 255, 0.7);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon-btn {
  color: var(--color-on-surface-variant);
  cursor: pointer;
  font-size: 16px;
  user-select: none;
}

.header-icon-btn:hover {
  color: var(--color-on-surface);
}

.mock-avatar {
  width: 24px;
  height: 24px;
  border-radius: var(--rounded-full);
  background-color: var(--color-surface-container-highest);
  border: 1px solid var(--color-border-subtle);
}

.app-main {
  flex: 1;
}

.app-footer {
  padding: 24px var(--spacing-gutter);
  background-color: var(--color-background);
  border-top: 1px solid var(--color-border-subtle);
  font-size: 12px;
  color: var(--color-on-surface-variant);
}

.footer-container {
  max-width: var(--spacing-container-max);
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-right {
  display: flex;
  gap: 16px;
}

.footer-right a {
  color: var(--color-on-surface-variant);
}

.footer-right a:hover {
  color: var(--color-primary);
  text-decoration: underline;
}

@media (max-width: 768px) {
  .header-nav, .header-search-form, .header-right {
    display: none;
  }
}
</style>
