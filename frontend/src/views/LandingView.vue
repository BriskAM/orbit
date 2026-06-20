<template>
  <div class="landing-container">
    <div class="glow-blob"></div>
    <div class="hero-content">
      <h1 class="display-title">🛰️ Orbit</h1>
      <p class="subtitle">Your GitHub, visualized. In-depth profile stats and analytics.</p>
      
      <form @submit.prevent="handleSubmit" class="search-form">
        <div class="input-wrapper">
          <input
            v-model="username"
            type="text"
            placeholder="Enter GitHub username (e.g. torvalds)"
            class="username-input"
            required
            :disabled="loading"
          />
          <button type="submit" class="submit-button" :disabled="loading">
            <span v-if="loading">Searching...</span>
            <span v-else>Visualize</span>
          </button>
        </div>
      </form>
      
      <div class="examples">
        <span class="example-label">Try these:</span>
        <button @click="quickSearch('torvalds')" class="example-chip">@torvalds</button>
        <button @click="quickSearch('octocat')" class="example-chip">@octocat</button>
        <button @click="quickSearch('yyx990803')" class="example-chip">@yyx990803</button>
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
  min-height: 80vh;
  position: relative;
  overflow: hidden;
  padding: var(--spacing-gutter);
}

.glow-blob {
  position: absolute;
  top: 30%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 450px;
  height: 450px;
  background: radial-gradient(circle, rgba(221, 183, 255, 0.15) 0%, rgba(93, 230, 255, 0.05) 60%, rgba(0, 0, 0, 0) 100%);
  filter: blur(45px);
  z-index: -1;
  pointer-events: none;
}

.hero-content {
  text-align: center;
  width: 100%;
  max-width: 600px;
  z-index: 1;
}

.display-title {
  font-family: 'Quicksand', sans-serif;
  font-size: 4rem;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 1.25rem;
  color: var(--color-on-surface-variant);
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.search-form {
  width: 100%;
  margin-bottom: 2.5rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  background: var(--color-glass-fill);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-full);
  padding: 6px;
  backdrop-filter: blur(12px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.input-wrapper:focus-within {
  border-color: var(--color-secondary);
  box-shadow: 0 0 25px rgba(93, 230, 255, 0.25);
}

.username-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 14px 24px;
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 1.1rem;
  color: var(--color-on-surface);
  outline: none;
}

.username-input::placeholder {
  color: rgba(228, 225, 233, 0.35);
}

.submit-button {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-weight: 700;
  background: var(--color-primary-container);
  color: var(--color-on-primary-container);
  border: none;
  border-radius: var(--rounded-full);
  padding: 14px 36px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-button:hover {
  background: var(--color-primary);
  color: var(--color-on-primary);
  transform: scale(1.02) translateY(-1px);
}

.submit-button:active {
  transform: scale(0.98);
}

.examples {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.example-label {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.95rem;
  color: rgba(228, 225, 233, 0.45);
}

.example-chip {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  background: var(--color-glass-fill);
  border: 1px solid var(--color-border-subtle);
  color: var(--color-secondary);
  padding: 6px 16px;
  border-radius: var(--rounded-full);
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.example-chip:hover {
  border-color: var(--color-secondary);
  background: rgba(93, 230, 255, 0.1);
  transform: translateY(-2px);
}

.example-chip:active {
  transform: translateY(0);
}
</style>
