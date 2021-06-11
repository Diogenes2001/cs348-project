<template>
  <b-navbar toggleable="lg" type="dark" variant="dark" fixed="top">
      <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
      <b-navbar-brand href="/">
      <img class="image" src="../assets/logo.png" alt="logo" width="3%" height="3%">
      PokeDB (name subject to change)
      </b-navbar-brand>

      <b-navbar-nav class="ml-auto">
        <b-nav-item href="/">Pokedex</b-nav-item>
        <b-nav-item href="/login">Login</b-nav-item>
      </b-navbar-nav>
    </b-navbar>
</template>

<script>
export default {
  name: 'myHeader'
}
</script>