import Vue from 'vue'
import VueRouter from 'vue-router'

import LandingPage from '@/views/LandingPage.vue'
import Recommendation from '@/views/Recom.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage
  },
  {
    path: '/recommendation',
    name: 'Recommendation',
    component: Recommendation,
  },
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
