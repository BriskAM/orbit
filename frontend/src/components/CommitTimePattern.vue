<template>
  <div class="pattern-card">
    <div class="pattern-header">
      <h3 class="pattern-title">Commit Timing Patterns</h3>
      <p class="pattern-subtitle">Hour of day × Day of week (Sampleed across top repos)</p>
    </div>
    
    <div class="grid-wrapper">
      <div class="heatmap-grid">
        <!-- Header row for Hours (12 AM, 4 AM, 8 AM, 12 PM, 4 PM, 8 PM) -->
        <div class="hours-header">
          <div class="hour-label-spacer"></div>
          <div class="hours-labels">
            <span style="grid-column: 1">12a</span>
            <span style="grid-column: 5">4a</span>
            <span style="grid-column: 9">8a</span>
            <span style="grid-column: 13">12p</span>
            <span style="grid-column: 17">4p</span>
            <span style="grid-column: 21">8p</span>
          </div>
        </div>
        
        <!-- Grid rows (Sunday to Saturday) -->
        <div class="grid-body">
          <div v-for="(row, wIdx) in commitTimeMatrix" :key="wIdx" class="grid-row">
            <span class="row-label">{{ WEEKDAYS[wIdx] }}</span>
            <div class="cells-container">
              <div
                v-for="(commits, hIdx) in row"
                :key="hIdx"
                class="time-cell"
                :style="{ backgroundColor: getCellColor(commits) }"
                @mouseenter="showTooltip($event, commits, wIdx, hIdx)"
                @mouseleave="hideTooltip"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Reactive Tooltip -->
    <Teleport to="body">
      <div
        v-if="tooltip.visible"
        class="pattern-tooltip"
        :style="{ top: tooltip.top + 'px', left: tooltip.left + 'px' }"
      >
        <strong>{{ tooltip.count }} commits</strong> on {{ tooltip.day }}s at {{ tooltip.hour }}
        <div class="tooltip-arrow"></div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { computed, reactive } from 'vue'

const props = defineProps({
  commitTimeMatrix: {
    type: Array,
    required: true,
    default: () => Array(7).fill(null).map(() => Array(24).fill(0))
  }
})

const WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const WEEKDAYS_FULL = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

const tooltip = reactive({
  visible: false,
  count: 0,
  day: '',
  hour: '',
  top: 0,
  left: 0
})

// Find the maximum value in the matrix for dynamic scaling
const maxCommits = computed(() => {
  let maxVal = 0
  props.commitTimeMatrix.forEach(row => {
    row.forEach(val => {
      if (val > maxVal) maxVal = val
    })
  })
  return maxVal
})

const getCellColor = (commits) => {
  if (commits === 0) return '#1b1b20'
  if (maxCommits.value === 0) return '#1b1b20'
  
  const intensity = commits / maxCommits.value
  // Render Purple gradient: rgba(221, 183, 255, intensity)
  // Base background is #1b1b20 (dark gray)
  // Let's use opacity steps
  if (intensity <= 0.25) return 'rgba(221, 183, 255, 0.25)'
  if (intensity <= 0.5) return 'rgba(221, 183, 255, 0.5)'
  if (intensity <= 0.75) return 'rgba(221, 183, 255, 0.75)'
  return 'var(--color-primary)' // 100% Neon Purple
}

const showTooltip = (event, commits, wIdx, hIdx) => {
  const rect = event.target.getBoundingClientRect()
  tooltip.count = commits
  tooltip.day = WEEKDAYS_FULL[wIdx]
  
  // Format hour (0 -> 12 AM, 12 -> 12 PM, 23 -> 11 PM)
  const ampm = hIdx >= 12 ? 'PM' : 'AM'
  const displayHour = hIdx % 12 === 0 ? 12 : hIdx % 12
  tooltip.hour = `${displayHour} ${ampm}`
  
  tooltip.top = window.scrollY + rect.top - 46
  tooltip.left = window.scrollX + rect.left + (rect.width / 2) - 85
  tooltip.visible = true
}

const hideTooltip = () => {
  tooltip.visible = false
}
</script>

<style scoped>
.pattern-card {
  background: var(--color-glass-fill);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  padding: 2rem;
  backdrop-filter: blur(12px);
  margin-bottom: 2.5rem;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.15);
}

.pattern-header {
  margin-bottom: 1.5rem;
  text-align: left;
}

.pattern-title {
  font-family: 'Quicksand', sans-serif;
  font-size: 1.4rem;
  color: var(--color-on-surface);
}

.pattern-subtitle {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.85rem;
  color: var(--color-on-surface-variant);
  margin-top: 0.25rem;
}

.grid-wrapper {
  overflow-x: auto;
  padding-bottom: 8px;
}

/* Custom scrollbar */
.grid-wrapper::-webkit-scrollbar {
  height: 6px;
}
.grid-wrapper::-webkit-scrollbar-thumb {
  background: var(--color-surface-container-high);
  border-radius: var(--rounded-sm);
}

.heatmap-grid {
  min-width: 720px;
}

.hours-header {
  display: flex;
  margin-bottom: 6px;
}

.hour-label-spacer {
  width: 45px;
}

.hours-labels {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(24, 1fr);
  text-align: center;
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.75rem;
  color: rgba(228, 225, 233, 0.4);
}

.grid-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.grid-row {
  display: flex;
  align-items: center;
}

.row-label {
  width: 45px;
  text-align: left;
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.8rem;
  color: rgba(228, 225, 233, 0.4);
  font-weight: 500;
}

.cells-container {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(24, 1fr);
  gap: 4px;
}

.time-cell {
  aspect-ratio: 1;
  border-radius: 2px;
  transition: transform 0.1s ease, filter 0.1s ease;
  cursor: pointer;
}

.time-cell:hover {
  transform: scale(1.3);
  filter: brightness(1.2);
  z-index: 10;
}
</style>

<style>
.pattern-tooltip {
  position: absolute;
  background: #1b1b20;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--color-on-surface);
  padding: 8px 12px;
  border-radius: var(--rounded-sm);
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.8rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  pointer-events: none;
  z-index: 9999;
  width: 170px;
  text-align: center;
  transform: translateY(-5px);
  animation: tooltip-fade 0.15s ease;
}
</style>
