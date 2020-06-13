import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Choose from '../views/Choose.vue'
import Manage from '../views/Manage.vue'

Vue.use(VueRouter)
const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/choose',
    name: 'choose',
    component: Choose
  },
  {
    path: '/control',
    name: 'Manage',
    component: Manage
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
