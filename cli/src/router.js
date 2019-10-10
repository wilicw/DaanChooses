import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Choose from './views/Choose.vue'

Vue.use(Router)

export default new Router({
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
    }
  ]
})
