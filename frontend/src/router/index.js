import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView
    },
    {
      path: '/:username',
      name: 'profile',
      component: ProfileView,
      props: true
    }
  ]
})

export default router
