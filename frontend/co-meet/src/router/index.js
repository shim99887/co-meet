import Vue from 'vue'
import VueRouter from 'vue-router'

import LandingPage from '@/views/LandingPage.vue'
import Recommendation from '@/views/Recom.vue'
import notFound from '@/views/notFound.vue'

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
  {
    path: '/404',
    name: 'notFound',
    component: notFound,
  },
  {
    path:'*',
    redirect: '/404',
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
