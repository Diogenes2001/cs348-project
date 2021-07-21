<template>
<b-container>

<!-- NAME, IMAGE, TYPE -->
<h3>{{ id }}: {{ pokemon }}</h3>
<a v-bind:href="'/pokemon/'+ id">
  <div class="bounce-container">
  <b-img center v-bind:src="require(`@/assets/pokemon/${id}.png`)" v-bind:alt="pokemon" width="200%" height="200%" class="image-style bounce-item"/>
  </div>
</a>
<b-row class="justify-content-md-center">
  <b-col v-for="(type, index) in types" :key="index" md="auto">

  <!-- TO-DO: Dynamically change color of background depending on type? -->
  <b-badge pill :pressed="true" variant="dark" v-bind:style="{ 'background-color' : colors[index] }">
  {{ type }}
  </b-badge>
  </b-col>
</b-row>
<br>

<!-- STATS/INFO TABLE -->
<b-row class="text-center">
<table class="table table-bordered">
  <tbody>
    <tr>
      <td>HP: {{ hp }}</td>
    </tr>
    <tr>
      <td>Atk: {{ atk }}</td>
    </tr>
    <tr>
      <td>Def: {{ def }}</td>
    </tr>
    <tr>
      <td>SpAtk: {{ spAtk }}</td>
    </tr>
    <tr>
      <td>SpDef: {{ spDef }}</td>
    </tr>
    <tr>
      <td>Spd: {{ spd }}</td>
    </tr>
    <tr v-if="moves && moves.length != 0">
      <td>{{ moves ? "Selected Moves Known: " + moves : (evolvesFromName ? "Evolves from: " + evolvesFromName : "") }}</td>
    </tr>
  </tbody>
</table>
</b-row>


<!--
UNCOMMENT FOR NON-TABLE VERSION (leaving it for now)
<b-row class="text-center">
  <b-col>HP: {{ hp }}</b-col>
  <b-col>Spd: {{ spd }}</b-col>
</b-row>
<b-row class="text-center">
  <b-col>Atk: {{ atk }}</b-col>
  <b-col>Def: {{ def }}</b-col>
</b-row>
<b-row class="text-center">
  <b-col>SpAtk: {{ spAtk }}</b-col>
  <b-col>SpDef: {{ spDef }}</b-col>
</b-row>
-->

</b-container>
</template>

<script>
export default {
  name: 'Profile',
  props: {
    id: Number,
    pokemon: String,
    types: Array,
    colors: Array,
    hp: Number,
    spd: Number,
    atk: Number,
    def: Number,
    spAtk: Number,
    spDef: Number,
    moves: String,
    evolvesFromName: String,
  }
}
</script>

<style>
.image-style {
  margin: 1rem 1rem !important;
  -webkit-transform: translate3d(0,0,0);
  -webkit-backface-visibility: hidden;
  transform: translate3d(0,0,0);
}

.bounce-item {
    align-self: flex-end;
    animation-duration: 0.3s;
    animation-iteration-count: once;
    animation-fill-mode: both;
    transform-origin: bottom;
}
.bounce-item:hover {
    animation-name: bounce;
    animation-timing-function: ease;
}
.bounce-container {
    display: flex;
    height: 100%;
    width: 100%;
}

@keyframes bounce {
  0%   { transform: translateY(0); }
  100% { transform: translateY(-5px); }
}
</style>