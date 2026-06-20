<template>
  <div class="chart-card">
    <div class="card-header">
      <h3 class="card-title">Monthly Commit Activity</h3>
      <p class="card-subtitle">Aggregated commit distributions across last 12 months</p>
    </div>
    
    <div v-if="!monthActivity || totalCommits === 0" class="no-data">
      <svg viewBox="0 0 16 16" width="24" height="24" fill="currentColor" class="no-data-icon">
        <path d="M1.5 1.75V13.5h13a.75.75 0 0 1 0 1.5h-14a.75.75 0 0 1-.75-.75V1.75a.75.75 0 0 1 1.5 0Zm4.28 7.47a.75.75 0 0 1-1.06 0L3 7.56v3.69a.75.75 0 0 1-1.5 0V6.5a.75.75 0 0 1 .75-.75h4.75a.75.75 0 0 1 0 1.5H5.06l1.72 1.72 2.72-2.72a.75.75 0 0 1 1.06 0L14 9.56V6.75a.75.75 0 0 1 1.5 0v4.75a.75.75 0 0 1-.75.75h-4.75a.75.75 0 0 1 0-1.5h2.69l-3.22-3.22-2.72 2.72Z"></path>
      </svg>
      <p>No commit history available for last 12 months.</p>
    </div>
    
    <div v-else class="chart-container-wrapper">
      <div class="svg-container">
        <svg viewBox="0 0 500 200" class="bar-svg">
          <!-- Background Grid lines -->
          <line x1="30" y1="40" x2="470" y2="40" stroke="#21262d" stroke-width="1" />
          <line x1="30" y1="95" x2="470" y2="95" stroke="#21262d" stroke-width="1" />
          <line x1="30" y1="150" x2="470" y2="150" stroke="#21262d" stroke-width="1" stroke-dasharray="3 3" />

          <!-- Bars rendering -->
          <rect
            v-for="(bar, idx) in chartBars"
            :key="idx"
            :x="bar.x"
            :y="bar.y"
            :width="bar.width"
            :height="bar.height"
            rx="3"
            fill="var(--color-secondary-container)"
            class="chart-bar"
            @mouseenter="showPointTooltip($event, bar)"
            @mouseleave="hidePointTooltip"
          />

          <!-- X-Axis line -->
          <line x1="30" y1="150" x2="470" y2="150" stroke="var(--color-border-subtle)" stroke-width="1" />

          <!-- Month text labels -->
          <text
            v-for="(bar, idx) in chartBars"
            :key="'lbl-' + idx"
            :x="bar.x + bar.width / 2"
            y="170"
            text-anchor="middle"
            fill="var(--color-on-surface-variant)"
            class="x-label"
          >
            {{ MONTH_NAMES[idx] }}
          </text>
        </svg>
      </div>
    </div>
    
    <!-- Tooltip Teleport -->
    <Teleport to="body">
      <div
        v-if="tooltip.visible"
        class="chart-tooltip"
        :style="{ top: tooltip.top + 'px', left: tooltip.left + 'px' }"
      >
        <strong>{{ tooltip.count }} commits</strong> ({{ tooltip.month }})
        <div class="tooltip-arrow"></div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { computed, reactive } from 'vue'

const props = defineProps({
  monthActivity: {
    type: Array,
    required: true,
    default: () => Array(12).fill(0)
  }
})

const MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

const tooltip = reactive({
  visible: false,
  count: 0,
  month: '',
  top: 0,
  left: 0
})

const totalCommits = computed(() => {
  return props.monthActivity.reduce((sum, count) => sum + count, 0)
})

const chartBars = computed(() => {
  const activity = props.monthActivity || Array(12).fill(0)
  const maxCommits = Math.max(...activity, 1)
  
  const barWidth = 20
  const gap = 16
  const leftStart = 42
  const maxBarHeight = 110
  const baselineY = 150
  
  return activity.map((count, idx) => {
    const x = leftStart + idx * (barWidth + gap)
    const height = (count / maxCommits) * maxBarHeight
    const y = baselineY - height
    
    return {
      x,
      y,
      width: barWidth,
      height: Math.max(height, 2), // Ensure at least a sliver of bar is visible
      count,
      month: MONTH_NAMES[idx]
    }
  })
})

const showPointTooltip = (event, bar) => {
  const rect = event.target.getBoundingClientRect()
  tooltip.count = bar.count
  tooltip.month = bar.month
  
  tooltip.top = window.scrollY + rect.top - 46
  tooltip.left = window.scrollX + rect.left + (rect.width / 2) - 80
  tooltip.visible = true
}

const hidePointTooltip = () => {
  tooltip.visible = false
}
</script>

<style scoped>
.chart-card {
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

.bar-svg {
  width: 100%;
  height: auto;
  overflow: visible;
}

.chart-bar {
  cursor: pointer;
  transition: fill 0.1s ease;
}

.chart-bar:hover {
  fill: var(--color-secondary);
}

.x-label {
  font-size: 9px;
  font-weight: 500;
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