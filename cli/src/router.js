import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Choose from './views/Choose.vue'
import Manage from './views/Manage.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
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
})
