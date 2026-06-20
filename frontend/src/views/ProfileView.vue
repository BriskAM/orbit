<template>
  <div class="profile-container-outer">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p class="loading-text">Analyzing GitHub footprint...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="error-card">
        <div class="error-icon">
          <svg class="octicon" viewBox="0 0 16 16" version="1.1" width="32" height="32" aria-hidden="true" fill="currentColor"><path d="M6.457 1.047c.66-1.08 2.226-1.08 2.886 0l6.3 10.31c.66 1.08-.22 2.483-1.443 2.483H1.8c-1.223 0-2.103-1.403-1.443-2.483l6.3-10.31ZM8 1.92l-6.3 10.31a.243.243 0 0 0 .243.37h12.114a.243.243 0 0 0 .243-.37L8 1.92ZM8 5c.414 0 .75.336.75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75.75 0 0 1 8 5Zm0 6a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z"></path></svg>
        </div>
        <h3>Analysis Failed</h3>
        <p>{{ error }}</p>
        <router-link to="/" class="retry-button">Try Another Username</router-link>
      </div>
    </div>

    <!-- Data Loaded State -->
    <div v-else-if="profile" class="profile-layout">
      <!-- Left Sidebar Column -->
      <div class="sidebar-col">
        <ProfileHeader :profile="profile.profile" @share="copyProfileLink" />
      </div>

      <!-- Right Main Column -->
      <div class="main-col">
        <!-- Tab Bar Navigation -->
        <div class="tabs-navigation">
          <button 
            @click="currentTab = 'overview'" 
            class="tab-btn" 
            :class="{ 'active': currentTab === 'overview' }"
          >
            <span class="tab-icon">
              <svg class="octicon" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true" fill="currentColor"><path d="M0 1.75A.75.75 0 0 1 .75 1h4.253c1.227 0 2.317.59 3 1.501.683-.911 1.773-1.501 3-1.501h4.253a.75.75 0 0 1 .75.75v10.5a.75.75 0 0 1-.75.75h-4.253c-1.046 0-2.02.4-2.747 1.127a.75.75 0 0 1-1.06 0A4.243 4.243 0 0 0 5.003 12H.75a.75.75 0 0 1-.75-.75V1.75Zm1.5 1.5v7.25c-.003.022.008.045.03.06a3.738 3.738 0 0 0 3.473-.31V2.75a2.738 2.738 0 0 0-3.503 0ZM14.5 3.25a2.738 2.738 0 0 0-3.503 0v7c1.378.1 2.656.704 3.503 1.61a.1.1 0 0 0 .03-.06V3.25Z"></path></svg>
            </span> Overview
          </button>
          <button 
            @click="currentTab = 'repositories'" 
            class="tab-btn" 
            :class="{ 'active': currentTab === 'repositories' }"
          >
            <span class="tab-icon">
              <svg class="octicon" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true" fill="currentColor"><path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.25.25 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"></path></svg>
            </span> Repositories
            <span class="tab-badge" v-if="profile.repos">{{ profile.repos.length }}</span>
          </button>
          <button 
            @click="currentTab = 'analytics'" 
            class="tab-btn" 
            :class="{ 'active': currentTab === 'analytics' }"
          >
            <span class="tab-icon">
              <svg class="octicon" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true" fill="currentColor"><path d="M1.5 1.75V13.5h13a.75.75 0 0 1 0 1.5H.75a.75.75 0 0 1-.75-.75V1.75a.75.75 0 0 1 1.5 0Zm4 5.5a.75.75 0 0 1 .75-.75h6a.75.75 0 0 1 .75.75v4.5a.75.75 0 0 1-.75.75h-6a.75.75 0 0 1-.75-.75v-4.5Zm1.5.75v3h4.5v-3h-4.5Z"></path></svg>
            </span> Analytics
          </button>
          <button 
            @click="currentTab = 'devmode'" 
            class="tab-btn" 
            :class="{ 'active': currentTab === 'devmode' }"
          >
            <span class="tab-icon">
              <svg class="octicon" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true" fill="currentColor"><path d="M14.7 1.3a1.25 1.25 0 0 0-1.77 0L9.23 5.00H6.77L2.8 1.03a1.25 1.25 0 0 0-1.77 0L.03 2.03a1.25 1.25 0 0 0 0 1.77L4.00 7.77v2.46L.3 13.93a1.25 1.25 0 0 0 0 1.77l1 1a1.25 1.25 0 0 0 1.77 0L6.77 13h2.46l3.97 3.97a1.25 1.25 0 0 0 1.77 0l1-1a1.25 1.25 0 0 0 0-1.77L12 10.23V7.77l3.7-3.7a1.25 1.25 0 0 0 0-1.77ZM11 9.23v1.54l3.25 3.25-.75.75L10.25 11H8.77l-4.5 4.5-.75-.75 4.5-4.5H6.46L3.21 7H1.67L1 6.33V4.67L2.67 3l3.33 3.33h1.54l3.25-3.25h1.54Z"></path></svg>
            </span> Dev Mode
          </button>
        </div>

        <!-- Tab Contents -->
        <div class="tab-content-panel">
          
          <!-- 1. Overview Tab -->
          <div v-if="currentTab === 'overview'" class="tab-pane animate-fade">
            <!-- Profile README Box (Coding Persona) -->
            <div class="readme-box" v-if="profile.metrics">
              <div class="readme-header">
                <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" fill="currentColor" class="readme-header-icon">
                  <path d="M4 1.75C4 .784 4.784 0 5.75 0h5.586a.75.75 0 0 1 .53.22l2.914 2.914a.75.75 0 0 1 .22.53v8.586A1.75 1.75 0 0 1 13.25 14h-7.5A1.75 1.75 0 0 1 4 12.25Zm1.75-.25a.25.25 0 0 0-.25.25v10.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25V4.5h-3a.75.75 0 0 1-.75-.75v-3.5Zm3.5 8a.75.75 0 0 1 .75-.75h3a.75.75 0 0 1 0 1.5h-3a.75.75 0 0 1-.75-.75Zm0 3a.75.75 0 0 1 .75-.75h3a.75.75 0 0 1 0 1.5h-3a.75.75 0 0 1-.75-.75Z"></path>
                </svg>
                <span class="readme-filename">{{ profile.profile.username }} / README.md</span>
              </div>
              <div class="readme-content">
                <h2 class="readme-greeting">Hi, I'm {{ profile.profile.display_name || profile.profile.username }}! 👋</h2>
                <p class="readme-intro">
                  Welcome to my automated profile analysis overview. Based on my commit timings, repository metadata, and coding rhythms, I am classified as a:
                </p>
                
                <div class="readme-persona-card">
                  <h3 class="readme-persona-title">{{ profile.metrics.personality_tag || 'Pragmatic Developer' }}</h3>
                  
                  <div class="readme-persona-stats">
                    <div class="readme-p-stat">
                      <span class="p-bullet-svg">
                        <svg class="octicon" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true" fill="currentColor"><path d="M9.598 1.591a.75.75 0 0 1 .785-.175 7 7 0 1 1-8.967 8.967.75.75 0 0 1 .961-.96 5.5 5.5 0 0 0 7.046-7.046.75.75 0 0 1 .175-.786Z"></path></svg>
                      </span>
                      <span>Night Commit Ratio: <strong>{{ (profile.metrics.night_owl_ratio * 100).toFixed(1) }}%</strong></span>
                    </div>
                    <div class="readme-p-stat">
                      <span class="p-bullet-svg">
                        <svg class="octicon" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true" fill="currentColor"><path d="M8 10.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5ZM8 12a4 4 0 1 1 0-8 4 4 0 0 1 0 8Zm0-8a.75.75 0 0 1-.75-.75V1.75a.75.75 0 0 1 1.5 0V3.25A.75.75 0 0 1 8 4Zm0 8.75a.75.75 0 0 1 .75.75v1.5a.75.75 0 0 1-1.5 0v-1.5a.75.75 0 0 1 .75-.75ZM4.22 4.22a.75.75 0 0 1 1.06 0l1.06 1.06a.75.75 0 0 1-1.06 1.06L4.22 5.28a.75.75 0 0 1 0-1.06Zm6.36 6.36a.75.75 0 0 1 1.06 0l1.06 1.06a.75.75 0 0 1-1.06 1.06l-1.06-1.06a.75.75 0 0 1 0-1.06Zm-7.83 1.48a.75.75 0 0 1 0 1.06l-1.06 1.06a.75.75 0 0 1-1.06-1.06l1.06-1.06a.75.75 0 0 1 1.06 0Zm11.31-7.83a.75.75 0 0 1 0 1.06l-1.06 1.06a.75.75 0 1 1-1.06-1.06l1.06-1.06a.75.75 0 0 1 1.06 0ZM4 8a.75.75 0 0 1-.75.75H1.75a.75.75 0 0 1 0-1.5H3.25A.75.75 0 0 1 4 8Zm10.5 0a.75.75 0 0 1-.75.75h-1.5a.75.75 0 0 1 0-1.5h1.5a.75.75 0 0 1 .75.75Z"></path></svg>
                      </span>
                      <span>Early Bird Ratio: <strong>{{ (profile.metrics.early_bird_ratio * 100).toFixed(1) }}%</strong></span>
                    </div>
                    <div class="readme-p-stat">
                      <span class="p-bullet-svg">
                        <svg class="octicon" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true" fill="currentColor"><path d="M8 0c-.22 0-.41.1-.55.27-.4.5-.78 1.06-1.08 1.6-.28.48-.56.97-.8 1.46-.78.43-1.48.98-2 1.64C3.02 5.64 2.75 6.42 2.75 7.25c0 2.62 2.13 4.75 4.75 4.75s4.75-2.13 4.75-4.75c0-.83-.27-1.61-.82-2.28-.52-.66-1.22-1.21-2-1.64-.24-.49-.52-.98-.8-1.46-.3-.54-.68-1.1-1.08-1.6C8.41.1 8.22 0 8 0Zm0 1.9c.29.38.58.78.85 1.18.25.37.49.75.72 1.13.43.26.82.59 1.13.98.39.49.55 1.04.55 1.56 0 1.79-1.46 3.25-3.25 3.25S4.75 8.54 4.75 6.75c0-.52.16-1.07.55-1.56.31-.39.7-.72 1.13-.98.23-.38.47-.76.72-1.13.27-.4.56-.8.85-1.18Zm0 2.35c.97 0 1.75.78 1.75 1.75s-.78 1.75-1.75 1.75-1.75-.78-1.75-1.75.78-1.75 1.75-1.75Z"></path></svg>
                      </span>
                      <span>Current Streak: <strong>{{ profile.metrics.current_streak }}</strong> days</span>
                    </div>
                    <div class="readme-p-stat">
                      <span class="p-bullet-svg">
                        <svg class="octicon" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true" fill="currentColor"><path d="M2.75 1.5a.25.25 0 0 0-.25.25V3c0 .591.242 1.124.63 1.508.067.067.139.13.216.188C3.766 5.568 4.773 6 6 6h1v1.624c-.958.172-1.782.686-2.302 1.4A3.992 3.992 0 0 0 4 12.25c0 .414.336.75.75.75h6.5a.75.75 0 0 0 .75-.75c0-1.282-.605-2.42-1.562-3.149a4.02 4.02 0 0 0-2.438-1.477V6h1c1.227 0 2.234-.432 2.654-1.304a2.237 2.237 0 0 0 .216-.188C13.508 4.124 13.75 3.59 13.75 3V1.75a.25.25 0 0 0-.25-.25H2.75ZM11.25 3v.004c0 .428-.158.749-.402.973-.24.22-.587.398-1.098.473L9.5 4.486V3h1.75ZM6.5 3v1.486l-.25-.036c-.511-.075-.858-.253-1.102-.477C4.908 3.753 4.75 3.432 4.75 3.004V3H6.5Zm1.5 5.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM4.75 14.5a.75.75 0 0 1 .75-.75h5a.75.75 0 0 1 0 1.5h-5a.75.75 0 0 1-.75-.75Z"></path></svg>
                      </span>
                      <span>Longest Streak: <strong>{{ profile.metrics.longest_streak }}</strong> days</span>
                    </div>
                    <div class="readme-p-stat">
                      <span class="p-bullet-svg">
                        <svg class="octicon" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true" fill="currentColor"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97 1.9 4.167a.75.75 0 0 1-1.087.79L8 11.777l-3.766 1.98a.75.75 0 0 1-1.087-.79l1.9-4.167L1.001 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.695Z"></path></svg>
                      </span>
                      <span>Stars Earned: <strong>{{ profile.profile.total_stars_earned }}</strong></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Pinned Repositories Grid -->
            <TopReposGrid v-if="profile.repos && profile.repos.length" :repos="profile.repos" />

            <!-- Contribution Heatmap -->
            <ContributionHeatmap
              v-if="profile.profile.metrics_json?.contributionsCollection?.contributionCalendar"
              :calendar-data="profile.profile.metrics_json.contributionsCollection.contributionCalendar"
            />
          </div>

          <!-- 2. Repositories Tab -->
          <div v-if="currentTab === 'repositories'" class="tab-pane animate-fade">
            <div class="repo-list">
              <div v-for="repo in profile.repos" :key="repo.id" class="repo-list-row">
                <div class="repo-row-left">
                  <div class="repo-row-title-row">
                    <a :href="`https://github.com/${repo.full_name || repo.name}`" target="_blank" class="repo-row-name">
                      {{ repo.name }}
                    </a>
                    <span class="repo-row-visibility">Public</span>
                  </div>
                  <p v-if="repo.description" class="repo-row-desc">{{ repo.description }}</p>
                  <p v-else class="repo-row-desc no-desc-placeholder">No description provided.</p>
                  
                  <div class="repo-row-meta">
                    <span v-if="repo.primary_language" class="repo-meta-item">
                      <span class="repo-lang-dot" :style="{ backgroundColor: getLangColor(repo.primary_language) }"></span>
                      {{ repo.primary_language }}
                    </span>
                    <a v-if="repo.stars > 0" :href="`https://github.com/${repo.full_name || repo.name}/stargazers`" target="_blank" class="repo-meta-item link-meta" style="display: flex; align-items: center; gap: 4px;">
                      <svg class="octicon" viewBox="0 0 16 16" version="1.1" width="14" height="14" aria-hidden="true" fill="currentColor"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97 1.9 4.167a.75.75 0 0 1-1.087.79L8 11.777l-3.766 1.98a.75.75 0 0 1-1.087-.79l1.9-4.167L1.001 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.695Z"></path></svg>
                      {{ repo.stars }}
                    </a>
                    <a v-if="repo.forks > 0" :href="`https://github.com/${repo.full_name || repo.name}/forks`" target="_blank" class="repo-meta-item link-meta" style="display: flex; align-items: center; gap: 4px;">
                      <svg class="octicon" viewBox="0 0 16 16" version="1.1" width="14" height="14" aria-hidden="true" fill="currentColor"><path d="M5 3.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm0 2.122a2.25 2.25 0 1 0-1.5 0v.878A2.25 2.25 0 0 0 5.75 8.5h1.5v2.128a2.251 2.251 0 1 0 1.5 0V8.5h1.5A2.25 2.25 0 0 0 12.5 6.25v-.878a2.25 2.25 0 1 0-1.5 0v.878a.75.75 0 0 1-.75.75h-4.5A.75.75 0 0 1 5 6.25v-.878Zm3.75 7.378a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm3-9.5a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z"></path></svg>
                      {{ repo.forks }}
                    </a>
                    <span v-if="repo.created_at" class="repo-meta-item">
                      Created {{ formatUpdatedDate(repo.created_at) }}
                    </span>
                  </div>
                </div>
                <div class="repo-row-right">
                  <button class="github-star-mock-btn" style="display: flex; align-items: center; gap: 4px;">
                    <svg class="octicon" viewBox="0 0 16 16" version="1.1" width="12" height="12" aria-hidden="true" fill="currentColor"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97 1.9 4.167a.75.75 0 0 1-1.087.79L8 11.777l-3.766 1.98a.75.75 0 0 1-1.087-.79l1.9-4.167L1.001 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.695Z"></path></svg>
                    Star
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 3. Analytics Tab -->
          <div v-if="currentTab === 'analytics'" class="tab-pane animate-fade">
            <!-- Language shares & Monthly Activity Grid -->
            <div class="analytics-grid" style="margin-bottom: 24px;">
              <div class="analytics-col">
                <LanguageDonut
                  v-if="profile.profile.language_breakdown && Object.keys(profile.profile.language_breakdown).length"
                  :language-breakdown="profile.profile.language_breakdown"
                />
              </div>
              <div class="analytics-col">
                <MonthActivityChart
                  v-if="profile.metrics && profile.metrics.month_activity"
                  :month-activity="profile.metrics.month_activity"
                />
              </div>
            </div>

            <!-- Commits Timing & Stars Growth -->
            <div class="analytics-grid">
              <div class="analytics-col">
                <CommitTimePattern :commit-time-matrix="profile.metrics.commit_time_matrix" />
              </div>
              <div class="analytics-col">
                <StarHistoryChart :star-history="profile.metrics.star_history" />
              </div>
            </div>
          </div>

          <!-- 4. Developer Console Tab -->
          <div v-if="currentTab === 'devmode'" class="tab-pane animate-fade">
            <div class="raw-data-card">
              <pre class="json-code"><code>{{ JSON.stringify(profile, null, 2) }}</code></pre>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- Toast Notification Teleport -->
    <Teleport to="body">
      <div v-if="toast.visible" class="toast-notification">
        {{ toast.message }}
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useProfileStore } from '../stores/profile'

// Components
import ProfileHeader from '../components/ProfileHeader.vue'
import ContributionHeatmap from '../components/ContributionHeatmap.vue'
import TopReposGrid from '../components/TopReposGrid.vue'
import LanguageDonut from '../components/LanguageDonut.vue'
import CommitTimePattern from '../components/CommitTimePattern.vue'
import StarHistoryChart from '../components/StarHistoryChart.vue'
import MonthActivityChart from '../components/MonthActivityChart.vue'

const props = defineProps({
  username: {
    type: String,
    required: true
  }
})

const store = useProfileStore()
const { profile, loading, error } = storeToRefs(store)

const currentTab = ref('overview')

// Toast State
const toast = ref({
  visible: false,
  message: ''
})

const copyProfileLink = async () => {
  try {
    await navigator.clipboard.writeText(window.location.href)
    showToast("Profile link copied to clipboard!")
  } catch (err) {
    showToast("Failed to copy link.")
  }
}

const showToast = (msg) => {
  toast.value.message = msg
  toast.value.visible = true
  setTimeout(() => {
    toast.value.visible = false
  }, 3000)
}

const formatUpdatedDate = (dateStr) => {
  if (!dateStr) return ''
  try {
    const d = new Date(dateStr)
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
  } catch (e) {
    return dateStr
  }
}

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

const getLangColor = (lang) => {
  if (!lang) return 'var(--color-primary)'
  return LANGUAGE_COLORS[lang.toLowerCase()] || 'var(--color-primary)'
}

const loadData = () => {
  if (props.username) {
    store.fetchProfile(props.username)
    currentTab.value = 'overview'
  }
}

onMounted(loadData)
watch(() => props.username, loadData)
</script>

<style scoped>
.profile-container-outer {
  background-color: var(--color-background);
  min-height: 80vh;
}

.profile-layout {
  display: flex;
  max-width: var(--spacing-container-max);
  margin: 0 auto;
  padding: 32px var(--spacing-gutter);
  gap: 32px;
}

.sidebar-col {
  width: 296px;
  flex-shrink: 0;
}

.main-col {
  flex-grow: 1;
  min-width: 0;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(88, 166, 255, 0.1);
  border-top: 3px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

.loading-text {
  color: var(--color-on-surface-variant);
  font-size: 14px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Error State */
.error-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
}

.error-card {
  text-align: center;
  background: var(--color-surface-container);
  border: 1px solid var(--color-error);
  padding: 32px;
  border-radius: var(--rounded-md);
  max-width: 400px;
}

.error-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.error-card h3 {
  color: var(--color-error);
  font-size: 18px;
  margin-bottom: 8px;
}

.error-card p {
  color: var(--color-on-surface-variant);
  font-size: 13px;
  margin-bottom: 16px;
}

.retry-button {
  display: inline-block;
  font-weight: 600;
  text-decoration: none;
  background: var(--color-error-container);
  color: var(--color-on-error-container);
  padding: 6px 16px;
  border-radius: var(--rounded-sm);
  font-size: 13px;
  border: 1px solid rgba(240,246,252,0.1);
}

.retry-button:hover {
  filter: brightness(1.1);
  text-decoration: none;
}

/* Tabs Navigation */
.tabs-navigation {
  display: flex;
  border-bottom: 1px solid var(--color-border-subtle);
  margin-bottom: 16px;
  gap: 8px;
  overflow-x: auto;
}

.tab-btn {
  background: transparent;
  border: none;
  color: var(--color-on-surface-variant);
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  border-bottom: 2px solid transparent;
  transition: all 0.1s ease;
  white-space: nowrap;
}

.tab-btn:hover {
  border-bottom-color: rgba(141, 150, 160, 0.4);
  color: var(--color-on-surface);
}

.tab-btn.active {
  border-bottom-color: #f78166; /* GitHub Tab bottom border active orange */
  color: var(--color-on-surface);
  font-weight: 600;
}

.tab-badge {
  background-color: var(--color-surface-container-highest);
  border-radius: 20px;
  font-size: 12px;
  padding: 0 6px;
  color: var(--color-on-surface);
  font-weight: 500;
}

.tab-content-panel {
  padding-top: 8px;
}

/* Profile README Box */
.readme-box {
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  background-color: transparent;
  margin-bottom: 24px;
  overflow: hidden;
  text-align: left;
}

.readme-header {
  background-color: var(--color-surface-container);
  border-bottom: 1px solid var(--color-border-subtle);
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.readme-header-icon {
  color: var(--color-on-surface-variant);
}

.readme-filename {
  font-size: 12px;
  font-family: var(--font-mono);
  color: var(--color-on-surface);
}

.readme-content {
  padding: 24px;
}

.readme-greeting {
  font-size: 20px;
  font-weight: 600;
  border-bottom: 1px solid var(--color-border-subtle);
  padding-bottom: 8px;
  margin-bottom: 16px;
}

.readme-intro {
  font-size: 14px;
  color: var(--color-on-background);
  margin-bottom: 16px;
}

.readme-persona-card {
  background-color: var(--color-surface-container);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  padding: 20px;
}

.readme-persona-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--color-primary);
  margin-bottom: 16px;
  letter-spacing: -0.5px;
}

.readme-persona-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.readme-p-stat {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-on-surface);
}

.p-bullet {
  font-size: 16px;
}

.p-bullet-svg {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--color-on-surface-variant);
  width: 16px;
  height: 16px;
}

/* Repositories Tab Content */
.repo-list {
  display: flex;
  flex-direction: column;
}

.repo-list-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid var(--color-border-subtle);
  padding: 24px 0;
  gap: 16px;
}

.repo-list-row:first-child {
  padding-top: 0;
}

.repo-row-left {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
  text-align: left;
}

.repo-row-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.repo-row-name {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-primary);
  text-decoration: none;
}

.repo-row-name:hover {
  text-decoration: underline;
}

.repo-row-visibility {
  font-size: 12px;
  color: var(--color-on-surface-variant);
  border: 1px solid var(--color-border-subtle);
  border-radius: 20px;
  padding: 0 7px;
  line-height: 18px;
}

.repo-row-desc {
  font-size: 14px;
  color: var(--color-on-surface-variant);
  line-height: 1.5;
  max-width: 600px;
}

.no-desc-placeholder {
  color: rgba(141, 150, 160, 0.4);
  font-style: italic;
}

.repo-row-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 12px;
  color: var(--color-on-surface-variant);
  flex-wrap: wrap;
}

.repo-meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--color-on-surface-variant);
}

.link-meta {
  color: var(--color-on-surface-variant);
}

.link-meta:hover {
  color: var(--color-primary);
  text-decoration: none;
}

.repo-lang-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.github-star-mock-btn {
  background-color: var(--color-surface-container-high);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-sm);
  color: var(--color-on-surface);
  padding: 3px 12px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
}

.github-star-mock-btn:hover {
  background-color: var(--color-surface-container-highest);
}

/* Analytics Tab Content */
.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 24px;
}

.analytics-col {
  min-width: 0;
}

/* Dev Mode Tab Content */
.raw-data-card {
  background-color: var(--color-surface-container);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--rounded-md);
  padding: 16px;
  max-height: 600px;
  overflow-y: auto;
  text-align: left;
}

.json-code {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--color-tertiary);
  white-space: pre-wrap;
  word-break: break-all;
}

/* Toast Alerts */
.toast-notification {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background-color: var(--color-surface-container-highest);
  border: 1px solid var(--color-primary);
  color: var(--color-on-surface);
  padding: 12px 24px;
  border-radius: var(--rounded-sm);
  font-size: 13px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
  z-index: 9999;
  animation: toast-slide-up 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes toast-slide-up {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .profile-layout {
    flex-direction: column;
    gap: 24px;
    padding: 16px;
  }
  
  .sidebar-col {
    width: 100%;
  }
  
  .analytics-grid {
    grid-template-columns: 1fr;
  }
}

.animate-fade {
  animation: fade-in 0.2s ease;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
