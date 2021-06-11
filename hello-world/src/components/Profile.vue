<template>
<b-container>

<!-- NAME, IMAGE, TYPE -->
<h3>{{ id }}: {{ pokemon }}</h3>
<b-img center v-bind:src="require(`@/assets/pokemon/${id}.png`)" v-bind:alt="pokemon" width="200%" height="200%" />
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
      <td>Spd: {{ spd }}</td>
    </tr>
    <tr>
      <td>Atk: {{ atk }}</td>
      <td>Def: {{ def }}</td>
    </tr>
    <tr>
      <td>SpAtk: {{ spAtk }}</td>
      <td>SpDef: {{ spDef }}</td>
    </tr>
    <tr></tr>
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
    spDef: Number
  }
}
</script>