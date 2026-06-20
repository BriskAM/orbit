<template>
  <div class="heatmap-card">
    <div class="heatmap-header">
      <h3 class="heatmap-title">Activity Grid</h3>
      <span class="total-badge">
        {{ calendarData.totalContributions }} contributions last year
      </span>
    </div>
    
    <div class="calendar-wrapper">
      <div class="calendar-grid">
        <!-- Labels for days -->
        <div class="day-labels">
          <span>Sun</span>
          <span>Tue</span>
          <span>Thu</span>
          <span>Sat</span>
        </div>
        
        <!-- Grid columns representing weeks -->
        <div class="weeks-container">
          <div v-for="(week, wIdx) in calendarData.weeks" :key="wIdx" class="week-column">
            <div
              v-for="(day, dIdx) in week.contributionDays"
              :key="dIdx"
              class="day-square"
              :style="{ backgroundColor: getShadeColor(day.contributionCount) }"
              @mouseenter="showTooltip($event, day)"
              @mouseleave="hideTooltip"
            ></div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Legend -->
    <div class="legend-row">
      <span class="legend-label">Less</span>
      <div class="legend-squares">
        <div class="legend-square" style="background-color: #1b1b20"></div>
        <div class="legend-square" style="background-color: rgba(93, 230, 255, 0.25)"></div>
        <div class="legend-square" style="background-color: rgba(93, 230, 255, 0.55)"></div>
        <div class="legend-square" style="background-color: rgba(93, 230, 255, 0.8)"></div>
        <div class="legend-square" style="background-color: var(--color-secondary)"></div>
      </div>
      <span class="legend-label">More</span>
    </div>

    <!-- Reactive Portal-like Tooltip -->
    <Teleport to="body">
      <div
        v-if="tooltip.visible"
        class="heatmap-tooltip"
        :style="{ top: tooltip.top + 'px', left: tooltip.left + 'px' }"
      >
        <strong>{{ tooltip.count }} contributions</strong> on {{ tooltip.date }}
        <div class="tooltip-arrow"></div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const props = defineProps({
  calendarData: {
    type: Object,
    required: true
  }
})

const tooltip = reactive({
  visible: false,
  count: 0,
  date: '',
  top: 0,
  left: 0
})

const showTooltip = (event, day) => {
  const rect = event.target.getBoundingClientRect()
  tooltip.count = day.contributionCount
  
  const d = new Date(day.date)
  tooltip.date = d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
  
  // Position above the square center
  tooltip.top = window.scrollY + rect.top - 46
  tooltip.left = window.scrollX + rect.left + (rect.width / 2) - 80
  tooltip.visible = true
}

const hideTooltip = () => {
  tooltip.visible = false
}

const getShadeColor = (count) => {
  if (count === 0) return '#1b1b20'
  if (count <= 3) return 'rgba(93, 230, 255, 0.25)'
  if (count <= 7) return 'rgba(93, 230, 255, 0.55)'
  if (count <= 12) return 'rgba(93, 230, 255, 0.8)'
  return 'var(--color-secondary)' // Neon Cyan
}
</script>

<style scoped>
.heatmap-card {
  background: var(--color-glass-fill);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  padding: 2rem;
  backdrop-filter: blur(12px);
  margin-bottom: 2rem;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.15);
}

.heatmap-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 12px;
}

.heatmap-title {
  font-family: 'Quicksand', sans-serif;
  font-size: 1.4rem;
  color: var(--color-on-surface);
}

.total-badge {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.85rem;
  background: rgba(93, 230, 255, 0.1);
  border: 1px solid var(--color-secondary);
  color: var(--color-secondary);
  padding: 4px 14px;
  border-radius: var(--rounded-full);
}

.calendar-wrapper {
  overflow-x: auto;
  padding-bottom: 8px;
}

/* Custom scrollbar for calendar */
.calendar-wrapper::-webkit-scrollbar {
  height: 6px;
}
.calendar-wrapper::-webkit-scrollbar-thumb {
  background: var(--color-surface-container-high);
  border-radius: var(--rounded-sm);
}

.calendar-grid {
  display: flex;
  gap: 10px;
  min-width: 750px;
  justify-content: space-between;
}

.day-labels {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 4px 0;
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.75rem;
  color: rgba(228, 225, 233, 0.4);
  text-align: left;
  width: 30px;
}

.weeks-container {
  display: flex;
  flex: 1;
  justify-content: space-between;
}

.week-column {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.day-square {
  width: 11px;
  height: 11px;
  border-radius: 2px;
  transition: transform 0.1s ease, filter 0.1s ease;
  cursor: pointer;
}

.day-square:hover {
  transform: scale(1.3);
  filter: brightness(1.2);
  z-index: 10;
}

.legend-row {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 1rem;
}

.legend-label {
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 0.75rem;
  color: rgba(228, 225, 233, 0.4);
}

.legend-squares {
  display: flex;
  gap: 3px;
}

.legend-square {
  width: 10px;
  height: 10px;
  border-radius: 2px;
}
</style>

<!-- Unscoped global rules for body-level Tooltip mounting -->
<style>
.heatmap-tooltip {
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
  width: 160px;
  text-align: center;
  transform: translateY(-5px);
  animation: tooltip-fade 0.15s ease;
}

.tooltip-arrow {
  position: absolute;
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px solid #1b1b20;
}

@keyframes tooltip-fade {
  from { opacity: 0; transform: translateY(0); }
  to { opacity: 1; transform: translateY(-5px); }
}
</style>
