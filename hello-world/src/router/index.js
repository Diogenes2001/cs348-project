import Vue from 'vue'
import Router from 'vue-router'
import Pokedex from '../components/Pokedex.vue'
import myHeader from '../components/Header.vue'
import Profile from '../components/Profile.vue'
import OwnedProfile from '../components/OwnedProfile.vue'
import Ping from '../components/Ping.vue'
import Login from '../components/Login.vue'
import Signup from '../components/Signup.vue'
import ChangePassword from '../components/ChangePassword.vue'
import Delete from '../components/Delete.vue'
import TeamGeneration from '../components/TeamGeneration.vue'
import Pokemon from '../components/Pokemon.vue'
import MyPokemon from '../components/MyPokemon.vue'

Vue.component('myHeader', myHeader);
Vue.component('profile', Profile);
Vue.component('ownedprofile', OwnedProfile);

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
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/signup',
      name: 'Sign Up',
      component: Signup
    },
    {
      path: '/changepass',
      name: 'Change Password',
      component: ChangePassword
    },
    {
      path: '/delete',
      name: 'Delete account',
      component: Delete
    },
    {
      path: '/teams',
      name: 'Generate Teams',
      component: TeamGeneration
    },
    {
      path: '/pokemon/:id',
      name: 'Pokemon Details',
      component: Pokemon
    },
    {
      path: '/ownedpokemon',
      name: 'Owned Pokemon',
      component: MyPokemon
    },
  ]
})
