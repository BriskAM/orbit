<template>
  <div class="stat-card" :class="[colorClass]">
    <div class="card-content">
      <div v-if="icon" class="stat-icon">{{ icon }}</div>
      <div class="stat-value">{{ value }}</div>
      <div class="stat-label">{{ label }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: {
    type: [String, Number],
    required: true
  },
  label: {
    type: String,
    required: true
  },
  color: {
    type: String,
    default: 'primary' // primary, secondary, tertiary, error
  },
  icon: {
    type: String,
    default: ''
  }
})

const colorClass = computed(() => `accent-${props.color}`)
</script>

<style scoped>
.stat-card {
  position: relative;
  background: var(--color-glass-fill);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-default);
  padding: 1.5rem;
  overflow: hidden;
  backdrop-filter: blur(12px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
}

.stat-card:hover {
  transform: scale(1.03) translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

/* Color Accent Variations */
.stat-card.accent-primary:hover {
  border-color: var(--color-primary);
  box-shadow: 0 0 20px rgba(221, 183, 255, 0.12);
}
.stat-card.accent-primary .stat-value {
  color: var(--color-primary);
}

.stat-card.accent-secondary:hover {
  border-color: var(--color-secondary);
  box-shadow: 0 0 20px rgba(93, 230, 255, 0.12);
}
.stat-card.accent-secondary .stat-value {
  color: var(--color-secondary);
}

.stat-card.accent-tertiary:hover {
  border-color: var(--color-tertiary);
  box-shadow: 0 0 20px rgba(255, 176, 205, 0.12);
}
.stat-card.accent-tertiary .stat-value {
  color: var(--color-tertiary);
}

.stat-card.accent-error:hover {
  border-color: var(--color-error);
  box-shadow: 0 0 20px rgba(255, 180, 171, 0.12);
}
.stat-card.accent-error .stat-value {
  color: var(--color-error);
}

.card-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.stat-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 2.2rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.85rem;
  color: var(--color-on-surface-variant);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
</style>
