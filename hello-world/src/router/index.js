import Vue from 'vue'
import Router from 'vue-router'
import Pokedex from '../components/Pokedex.vue'
import myHeader from '../components/Header.vue'
import Profile from '../components/Profile.vue'
import Ping from '../components/Ping.vue'

Vue.component('myHeader', myHeader);
Vue.component('profile', Profile);

Vue.use(Router)
export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Pokedex',
      component: Pokedex
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile,
    },
  ]
})