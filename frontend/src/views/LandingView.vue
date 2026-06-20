<template>
  <div class="landing-container">
    <div class="search-box-card">
      <div class="search-header">
        <!-- Octocat Logo SVG -->
        <svg height="48" aria-hidden="true" viewBox="0 0 16 16" version="1.1" width="48" fill="currentColor" class="github-logo">
          <path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.35 3.12.87 0 .68.01 1.3.01 1.49 0 .21-.15.47-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"></path>
        </svg>
        <h1 class="search-title">Visualize a GitHub Profile</h1>
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
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const loading = ref(false)

const handleSubmit = () => {
  if (username.value.trim()) {
    loading.value = true
    router.push({ name: 'profile', params: { username: username.value.trim().toLowerCase() } })
  }
}

const quickSearch = (name) => {
  router.push({ name: 'profile', params: { username: name } })
}
</script>

<style scoped>
.landing-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  padding: var(--spacing-gutter);
  background-color: var(--color-background);
}

.search-box-card {
  background-color: var(--color-surface-container);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-default);
  width: 100%;
  max-width: 340px;
  padding: 24px;
  margin-bottom: 16px;
}

.search-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 24px;
}

.github-logo {
  color: var(--color-on-background);
  margin-bottom: 16px;
}

.search-title {
  font-size: 20px;
  font-weight: 300;
  color: var(--color-on-surface);
  text-align: center;
  letter-spacing: -0.5px;
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-label {
  font-size: 14px;
  font-weight: 400;
  color: var(--color-on-surface);
  text-align: left;
}

.username-input {
  background-color: var(--color-surface-container-lowest);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-sm);
  color: var(--color-on-background);
  padding: 6px 12px;
  font-size: 14px;
  outline: none;
  font-family: inherit;
}

.username-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(31, 111, 235, 0.3);
}

.submit-button {
  background-color: var(--color-secondary-container); /* Green */
  color: #ffffff;
  border: 1px solid rgba(240, 246, 252, 0.1);
  border-radius: var(--rounded-sm);
  padding: 6px 16px;
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
  border-radius: var(--rounded-default);
  width: 100%;
  max-width: 340px;
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
</style>
