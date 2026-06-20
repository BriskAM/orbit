import { defineStore } from 'pinia'
import axios from 'axios'

export const useProfileStore = defineStore('profile', {
  state: () => ({
    profile: null,
    loading: false,
    error: null,
  }),
  actions: {
    async fetchProfile(username) {
      this.loading = true
      this.error = null
      this.profile = null
      try {
        const response = await axios.get(`/api/profile/${username}`)
        if (response.data && response.data.status === 'success') {
          this.profile = response.data.data
        } else {
          this.error = response.data?.message || 'Failed to load profile'
        }
      } catch (err) {
        this.error = 
          err.response?.data?.message || 
          err.response?.data?.error || 
          err.message || 
          'An error occurred while connecting to the server.'
      } finally {
        this.loading = false
      }
    }
  }
})
