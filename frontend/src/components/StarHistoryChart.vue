<template>
  <div class="star-card">
    <div class="card-header">
      <h3 class="card-title">Star History Growth</h3>
      <p class="card-subtitle">Cumulative stars earned over time (Project creation dates)</p>
    </div>
    
    <div v-if="!starHistory || starHistory.length === 0" class="no-data">
      <div class="no-data-icon">⭐</div>
      <p>No star history data available.</p>
    </div>
    
    <div v-else class="chart-container-wrapper">
      <div class="svg-container">
        <svg viewBox="0 0 500 200" class="star-svg">
          <defs>
            <!-- Area Gradient -->
            <linearGradient id="area-grad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="var(--color-secondary)" stop-opacity="0.2" />
              <stop offset="100%" stop-color="var(--color-secondary)" stop-opacity="0.0" />
            </linearGradient>
          </defs>
          
          <!-- Background Grid lines -->
          <line x1="0" y1="40" x2="500" y2="40" stroke="rgba(255,255,255,0.03)" stroke-width="1" />
          <line x1="0" y1="100" x2="500" y2="100" stroke="rgba(255,255,255,0.03)" stroke-width="1" />
          <line x1="0" y1="160" x2="500" y2="160" stroke="rgba(255,255,255,0.03)" stroke-width="1" />

          <!-- Filled glow area -->
          <polygon :points="areaPoints" fill="url(#area-grad)" />

          <!-- Stroke growth line -->
          <path
            :d="pathData"
            fill="transparent"
            stroke="var(--color-secondary)"
            stroke-width="3"
            stroke-linecap="round"
            stroke-linejoin="round"
          />

          <!-- Dots for each repo creation timestamp -->
          <circle
            v-for="(pt, idx) in chartPoints"
            :key="idx"
            :cx="pt.x"
            :cy="pt.y"
            r="4"
            fill="var(--color-background)"
            stroke="var(--color-secondary)"
            stroke-width="2.5"
            class="chart-dot"
            @mouseenter="showPointTooltip($event, pt)"
            @mouseleave="hidePointTooltip"
          />
        </svg>
      </div>
      
      <!-- Time X-Axis labels -->
      <div class="labels-row">
        <span>{{ starHistory[0].date }}</span>
        <span>{{ starHistory[Math.floor(starHistory.length / 2)].date }}</span>
        <span>{{ starHistory[starHistory.length - 1].date }}</span>
      </div>
    </div>
    
    <!-- Tooltip Teleport -->
    <Teleport to="body">
      <div
        v-if="tooltip.visible"
        class="chart-tooltip"
        :style="{ top: tooltip.top + 'px', left: tooltip.left + 'px' }"
      >
        <strong>{{ tooltip.stars }} stars</strong> ({{ tooltip.date }})
        <div class="tooltip-arrow"></div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { computed, reactive } from 'vue'

const props = defineProps({
  starHistory: {
    type: Array,
    required: true,
    default: () => []
  }
})

const tooltip = reactive({
  visible: false,
  stars: 0,
  date: '',
  top: 0,
  left: 0
})

const chartPoints = computed(() => {
  const history = props.starHistory || []
  if (history.length === 0) return []
  
  // Find max stars for proper Y scaling
  const maxStars = Math.max(...history.map(pt => pt.stars), 1)
  const width = 500
  const height = 140 // Leave padding at top and bottom of 200px container
  const paddingY = 20
  
  return history.map((pt, idx) => {
    // Calculate X coordinate
    const x = history.length > 1 ? (idx / (history.length - 1)) * width : width / 2
    // Calculate Y coordinate (inverted in SVG viewbox)
    const relativeY = (pt.stars / maxStars) * height
    const y = 200 - paddingY - relativeY
    
    return {
      x,
      y,
      stars: pt.stars,
      date: pt.date
    }
  })
})

const pathData = computed(() => {
  const pts = chartPoints.value
  if (pts.length === 0) return ''
  return `M ${pts[0].x} ${pts[0].y} ` + pts.slice(1).map(p => `L ${p.x} ${p.y}`).join(' ')
})

const areaPoints = computed(() => {
  const pts = chartPoints.value
  if (pts.length === 0) return ''
  // Close the polygon at the bottom x boundaries
  return `${pts[0].x},200 ` + pts.map(p => `${p.x},${p.y}`).join(' ') + ` ${pts[pts.length - 1].x},200`
})

const showPointTooltip = (event, pt) => {
  const rect = event.target.getBoundingClientRect()
  tooltip.stars = pt.stars
  
  // Format Month-Year
  const parts = pt.date.split('-')
  const dateObj = new Date(parts[0], parts[1] - 1)
  tooltip.date = dateObj.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
  
  tooltip.top = window.scrollY + rect.top - 46
  tooltip.left = window.scrollX + rect.left + (rect.width / 2) - 80
  tooltip.visible = true
}

const hidePointTooltip = () => {
  tooltip.visible = false
}
</script>

<style scoped>
.star-card {
  background-color: var(--color-surface-container);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  padding: 16px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.card-header {
  margin-bottom: 16px;
  text-align: left;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-on-surface);
}

.card-subtitle {
  font-size: 11px;
  color: var(--color-on-surface-variant);
  margin-top: 4px;
}

.chart-container-wrapper {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.svg-container {
  width: 100%;
  height: 100%;
}

.star-svg {
  width: 100%;
  height: auto;
  overflow: visible;
}

.chart-dot {
  cursor: pointer;
  transition: r 0.1s ease;
}

.chart-dot:hover {
  r: 6;
}

.labels-row {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--color-on-surface-variant);
  border-top: 1px solid var(--color-border-subtle);
  padding-top: 8px;
}

.no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-grow: 1;
  padding: 24px 0;
  color: var(--color-on-surface-variant);
}

.no-data-icon {
  font-size: 24px;
  margin-bottom: 8px;
  opacity: 0.3;
}
</style>

<style>
.chart-tooltip {
  position: absolute;
  background: #161b22;
  border: 1px solid var(--color-border-subtle);
  color: var(--color-on-surface);
  padding: 6px 10px;
  border-radius: var(--rounded-sm);
  font-size: 11px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  pointer-events: none;
  z-index: 9999;
  width: 160px;
  text-align: center;
  transform: translateY(-5px);
  animation: tooltip-fade 0.15s ease;
}
</style>
