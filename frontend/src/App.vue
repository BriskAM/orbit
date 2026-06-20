<template>
  <div class="app-layout">
    <header class="app-header">
      <div class="header-container">
        <router-link to="/" class="logo">
          <span class="logo-icon">🛰️</span> Orbit
        </router-link>
      </div>
    </header>
    
    <main class="app-main">
      <router-view />
    </main>

    <footer class="app-footer">
      <p>© 2026 Orbit. Built with Flask, Vue 3 & GitHub GraphQL API.</p>
    </footer>
  </div>
</template>

<script setup>
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
  border-bottom: 1px solid var(--color-border-subtle);
  padding: 1.2rem var(--spacing-gutter);
  backdrop-filter: blur(12px);
  background-color: rgba(19, 19, 24, 0.7);
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

.logo {
  font-family: 'Quicksand', sans-serif;
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--color-on-surface);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
  letter-spacing: -0.01em;
  transition: opacity 0.2s ease;
}

.logo:hover {
  opacity: 0.9;
}

.logo-icon {
  font-size: 1.5rem;
}

.app-main {
  flex: 1;
}

.app-footer {
  text-align: center;
  padding: 2rem var(--spacing-gutter);
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.85rem;
  color: rgba(228, 225, 233, 0.4);
  border-top: 1px solid var(--color-border-subtle);
  background-color: var(--color-surface-container-lowest);
}
</style>
