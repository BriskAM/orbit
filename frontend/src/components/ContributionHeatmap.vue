<template>
  <div class="heatmap-card">
    <div class="heatmap-header">
      <h3 class="heatmap-title">Contributions in the last year</h3>
      <span class="total-badge">
        {{ calendarData.totalContributions }} contributions
      </span>
    </div>
    
    <div class="calendar-wrapper">
      <div class="calendar-grid">
        <!-- Labels for days -->
        <div class="day-labels">
          <span>Mon</span>
          <span>Wed</span>
          <span>Fri</span>
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
        <div class="legend-square" style="background-color: #161b22"></div>
        <div class="legend-square" style="background-color: #0e4429"></div>
        <div class="legend-square" style="background-color: #006d32"></div>
        <div class="legend-square" style="background-color: #26a641"></div>
        <div class="legend-square" style="background-color: #39d353"></div>
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
  if (count === 0) return '#161b22'
  if (count <= 3) return '#0e4429'
  if (count <= 7) return '#006d32'
  if (count <= 12) return '#26a641'
  return '#39d353'
}
</script>

<style scoped>
.heatmap-card {
  background: transparent;
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  padding: 16px;
  margin-bottom: 24px;
}

.heatmap-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.heatmap-title {
  font-size: 14px;
  font-weight: 400;
  color: var(--color-on-surface);
}

.total-badge {
  font-size: 12px;
  color: var(--color-on-surface-variant);
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
  background: var(--color-surface-container-highest);
  border-radius: var(--rounded-sm);
}

.calendar-grid {
  display: flex;
  gap: 12px;
  min-width: 760px;
}

.day-labels {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 14px 0 2px 0;
  font-size: 10px;
  color: var(--color-on-surface-variant);
  text-align: left;
  width: 28px;
  user-select: none;
}

.weeks-container {
  display: flex;
  flex: 1;
  gap: 3px;
}

.week-column {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.day-square {
  width: 10px;
  height: 10px;
  border-radius: 2px;
  cursor: pointer;
  border: 1px solid rgba(27, 31, 35, 0.04);
}

.day-square:hover {
  filter: brightness(1.2);
  outline: 1px solid #ffffff;
}

.legend-row {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 12px;
}

.legend-label {
  font-size: 11px;
  color: var(--color-on-surface-variant);
}

.legend-squares {
  display: flex;
  gap: 3px;
}

.legend-square {
  width: 10px;
  height: 10px;
  border-radius: 2px;
  border: 1px solid rgba(27, 31, 35, 0.04);
}
</style>

<!-- Unscoped global rules for body-level Tooltip mounting -->
<style>
.heatmap-tooltip {
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
  width: 170px;
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
  border-top: 5px solid var(--color-border-subtle);
}

@keyframes tooltip-fade {
  from { opacity: 0; transform: translateY(0); }
  to { opacity: 1; transform: translateY(-5px); }
}
</style>
