<template>
  <b-navbar toggleable="lg" type="dark" variant="dark" fixed="top">
      <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
      <b-navbar-brand href="/" class="w-25">
      <img class="image" src="../assets/logo.png" alt="logo" width="8%" height="8%">
      Pok&eacute;DB
      </b-navbar-brand>

      <b-navbar-nav class="ml-auto">
        <b-nav-item href="/">Pok&eacute;dex</b-nav-item>
        <b-nav-item href="/teams">Teams</b-nav-item>
        <b-nav-item href="/ownedpokemon" v-show="this.username">My Pokemon</b-nav-item>
        <b-nav-item v-show="this.username == null" href="/login">Login</b-nav-item>
        <b-nav-item-dropdown v-show="this.username" :text="this.username" right>
          <b-dropdown-item href="/changepass">Change password</b-dropdown-item>
          <b-dropdown-item href="/delete">Delete account</b-dropdown-item>
          <b-dropdown-item @click="logout()">Log out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>
</template>

<script>
export default {
  name: 'myHeader'
}
</script>

<script>
  import { mapState } from 'vuex'

  export default {
    computed: mapState({
      username: state => state.username
    }),
    methods: {
      logout() {
        this.$store.commit('logout')
      }
    }
  }
</script>
