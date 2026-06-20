<template>
  <div class="language-card">
    <h3 class="card-title">Language Shares</h3>
    
    <div class="chart-content">
      <!-- SVG Donut Chart -->
      <div class="chart-container">
        <svg viewBox="0 0 100 100" class="donut-svg">
          <!-- Background track circle -->
          <circle
            cx="50"
            cy="50"
            r="38"
            fill="transparent"
            stroke="var(--color-surface-container-lowest)"
            stroke-width="12"
          />
          
          <!-- Colored segments -->
          <circle
            v-for="(segment, idx) in segments"
            :key="idx"
            cx="50"
            cy="50"
            r="38"
            fill="transparent"
            :stroke="segment.color"
            stroke-width="12"
            :stroke-dasharray="`${segment.percent} ${100 - segment.percent}`"
            :stroke-dashoffset="-segment.offset"
            pathLength="100"
            class="donut-segment"
            :class="{ 'segment-active': activeLanguage === segment.lang }"
            @mouseenter="activeLanguage = segment.lang"
            @mouseleave="activeLanguage = null"
          />
          
          <!-- Center Text Details -->
          <g class="center-text">
            <text x="50" y="47" class="center-percent">
              {{ activePercentage ? activePercentage + '%' : 'Top' }}
            </text>
            <text x="50" y="63" class="center-label">
              {{ activeLanguage || segments[0]?.lang || 'None' }}
            </text>
          </g>
        </svg>
      </div>
      
      <!-- Legends -->
      <div class="legend-container">
        <div
          v-for="(segment, idx) in segments"
          :key="idx"
          class="legend-item"
          :class="{ 'legend-active': activeLanguage === segment.lang }"
          @mouseenter="activeLanguage = segment.lang"
          @mouseleave="activeLanguage = null"
        >
          <div class="legend-color-dot" :style="{ backgroundColor: segment.color }"></div>
          <span class="legend-name">{{ segment.lang }}</span>
          <span class="legend-percent">{{ segment.percent }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  languageBreakdown: {
    type: Object,
    required: true
  }
})

const activeLanguage = ref(null)

const activePercentage = computed(() => {
  if (!activeLanguage.value) return null
  return props.languageBreakdown[activeLanguage.value] || null
})

// Standard language colors mapping
const LANGUAGE_COLORS = {
  python: '#3572A5',
  javascript: '#f1e05a',
  vue: '#41b883',
  typescript: '#3178c6',
  html: '#e34c26',
  css: '#563d7c',
  rust: '#dea584',
  go: '#00ADD8',
  cpp: '#f34b7d',
  c: '#a8b9cc',
  shell: '#89e051',
  ruby: '#701516',
  java: '#b07219'
}

// Fallback vibrant palette for other/rare languages
const ACCENT_PALETTE = [
  'var(--color-primary)',   // Vibrant Purple
  'var(--color-secondary)', // Vibrant Cyan
  'var(--color-tertiary)',  // Vibrant Pink
  '#ffb076',                // Pastel Orange
  '#8fffb5',                // Light Green
  '#fff58f',                // Pastel Yellow
  '#b76dff',                // Lavender
  '#00cbe6'                 // Deep Teal
]

const segments = computed(() => {
  const breakdown = props.languageBreakdown || {}
  const keys = Object.keys(breakdown)
  
  let currentOffset = 0
  return keys.map((lang, index) => {
    const percent = breakdown[lang]
    const color = LANGUAGE_COLORS[lang.toLowerCase()] || ACCENT_PALETTE[index % ACCENT_PALETTE.length]
    const offset = currentOffset
    currentOffset += percent
    
    return {
      lang,
      percent,
      color,
      offset
    }
  })
})
</script>

<style scoped>
.language-card {
  background: var(--color-glass-fill);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  padding: 2rem;
  backdrop-filter: blur(12px);
  height: 100%;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.15);
}

.card-title {
  font-family: 'Quicksand', sans-serif;
  font-size: 1.4rem;
  color: var(--color-on-surface);
  margin-bottom: 1.5rem;
}

.chart-content {
  display: flex;
  align-items: center;
  justify-content: space-around;
  gap: 2rem;
  flex-wrap: wrap;
}

.chart-container {
  width: 200px;
  height: 200px;
  position: relative;
}

.donut-svg {
  transform: rotate(-90deg); /* Start segments at 12 o'clock */
  width: 100%;
  height: 100%;
}

.donut-segment {
  transition: stroke-width 0.2s ease, filter 0.2s ease;
  cursor: pointer;
}

.donut-segment:hover,
.segment-active {
  stroke-width: 16;
  filter: drop-shadow(0 0 4px rgba(255, 255, 255, 0.1));
}

.center-text {
  transform: rotate(90deg); /* Counter-rotate center text to be upright */
  transform-origin: 50px 50px;
  text-anchor: middle;
  fill: var(--color-on-surface);
}

.center-percent {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  fill: var(--color-secondary);
}

.center-label {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 7px;
  font-weight: 600;
  fill: var(--color-on-surface-variant);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.legend-container {
  flex: 1;
  min-width: 180px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'Be Vietnam Pro', sans-serif;
  padding: 6px 12px;
  border-radius: var(--rounded-sm);
  transition: all 0.2s ease;
  cursor: pointer;
}

.legend-item:hover,
.legend-active {
  background: var(--color-glass-fill);
  transform: translateX(4px);
}

.legend-color-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.05);
}

.legend-name {
  flex: 1;
  font-size: 0.95rem;
  color: var(--color-on-surface);
}

.legend-percent {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--color-on-surface-variant);
}
</style>
