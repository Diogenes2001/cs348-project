<template>
<div>
<b-container style="min-width:360px" v-show="!isEditing">

<!-- NAME, IMAGE, TYPE -->
<b-row>
<b-col>
<h3>{{ pokemon }}</h3>
</b-col>
<b-col cols="1"><img @click="onEdit" class="image" src="../assets/edit.png" alt="edit"></b-col>
<b-col cols="1"><img @click="onDelete" class="image" src="../assets/delete.png" alt="delete"></b-col>
</b-row>
<b-row class="justify-content-md-center">

<b-col>

<b-container>

<b-row class="justify-content-md-center">
<a v-bind:href="'/pokemon/'+ id">
  <div class="bounce-container">
  <b-img center v-bind:src="require(`@/assets/pokemon/${id + (isShiny ? '-shiny' : '')}.png`)" v-bind:alt="pokemon" width="200%" height="200%" class="image-style bounce-item"/>
  </div>
</a>
</b-row>

<b-row class="justify-content-md-center">
  <b-col v-for="(type, index) in types" :key="index" md="auto">

  <!-- TO-DO: Dynamically change color of background depending on type? -->
  <h4>
  <b-badge pill :pressed="true" variant="dark" v-bind:style="{ 'background-color' : colors[index] }">
  {{ type }}
  </b-badge>
  </h4>
  </b-col>
</b-row>
</b-container>

</b-col>

<b-col class="text-center row align-items-end">
<!-- <h5 class="col align-self-end">Details</h5> -->
<table class="table table-bordered">
  <tbody>
    <tr>
      <td>Level {{ level }} {{ speciesName }}</td>
    </tr>
    <!-- <tr>
      <td>Level: {{ level }}</td>
    </tr> -->
    <tr>
      <td>Ability: {{ ability }}</td>
    </tr>
    <tr>
      <td>Gender: {{ gender }}</td>
    </tr>
    <!--<tr>
      <td>Shiny: {{ isShiny ? 'Yes' : 'No' }}</td>
    </tr> -->
  </tbody>
</table>
<!-- <h5 class="text-center">Moves</h5> -->
<table class="table table-bordered">
  <tbody>
    <tr>
      <td>{{ move1 }}</td>
      <td v-show="move2">{{ move2 }}</td>
    </tr>
    <tr v-show="move3 || move4">
      <td>{{ move3 }}</td>
      <td v-show="move4">{{ move4 }}</td>
    </tr>
  </tbody>
</table>
</b-col>
</b-row>
<!-- <b-row class="justify-content-md-center">
  <b-col v-for="(type, index) in types" :key="index" md="auto">
  <h4>
  <b-badge pill :pressed="true" variant="dark" v-bind:style="{ 'background-color' : colors[index] }">
  {{ type }}
  </b-badge>
  </h4>
  </b-col>
</b-row> -->
<br>
<!-- STATS/INFO TABLE -->
<b-row class="text-center">
<!-- <h5 class="text-center">Stats</h5> -->
<table class="table table-bordered">
  <tbody>
    <tr>
      <td>HP: {{ hp }}</td>
      <td>Spd: {{ spd }}</td>
      <td>Atk: {{ atk }}</td>
    </tr>
    <tr>
      <td>Def: {{ def }}</td>
      <td>SpAtk: {{ spAtk }}</td>
      <td>SpDef: {{ spDef }}</td>
    </tr>
</tbody>
</table>
</b-row>

</b-container>

<b-container style="min-width:360px">
<b-card border-variant="dark" v-show="isEditing">
  <b-form @submit="onSubmit" @reset="onReset" class="w-100">
    <b-form-row>
      <b-col><label class="mr-1">Nickname:</label><b-form-input type="text" v-model="pokemon" placeholder="Enter a nickname" /></b-col>
      <b-col><label class="mr-1">Level:</label><b-form-input type="number" v-model="level" placeholder="Enter #" /></b-col>
    </b-form-row>
    <br>
    <b-form-row>
      <b-col><label class="mr-1">HP:</label><b-form-input type="number" v-model="hp" placeholder="Enter #" /></b-col>
      <b-col><label class="mr-1">Spd:</label><b-form-input type="number" v-model="spd" placeholder="Enter #" /></b-col>
      <b-col><label class="mr-1">Atk:</label><b-form-input type="number" v-model="atk" placeholder="Enter #" /></b-col>
    </b-form-row>
    <br>
    <b-form-row>
      <b-col><label class="mr-1">Def:</label><b-form-input type="number" v-model="def" placeholder="Enter #" /></b-col>
      <b-col><label class="mr-1">SpAtk:</label><b-form-input type="number" v-model="spAtk" placeholder="Enter #" /></b-col>
      <b-col><label class="mr-1">SpDef:</label><b-form-input type="number" v-model="spDef" placeholder="Enter #" /></b-col>
    </b-form-row>
    <br>
    <b-form-row>
      <b-col><label class="mr-1">Move 1:</label><b-form-input required type="text" v-model="move1" placeholder="Enter a move" /></b-col>
      <b-col><label class="mr-1">Move 2:</label><b-form-input type="text" v-model="move2" placeholder="Enter a move" /></b-col>
    </b-form-row>
    <br>
    <b-form-row>
      <b-col><label class="mr-1">Move 3:</label><b-form-input type="text" v-model="move3" placeholder="Enter a move" /></b-col>
      <b-col><label class="mr-1">Move 4:</label><b-form-input type="text" v-model="move4" placeholder="Enter a move" /></b-col>
    </b-form-row>
    <div style="color: red;" v-show="this.error">{{ this.error }}</div>
    <br>
    <b-container class="bv-example-row">
      <b-row align-h="end">
        <b-col md="auto"><b-button type="reset" pill variant="danger">Cancel</b-button></b-col>
        <b-col md="auto"><b-button type="submit" pill variant="success">Change</b-button></b-col>
      </b-row>
    </b-container>
  </b-form> 
</b-card>
</b-container>

</div>
</template>

<script>
import axios from "axios";
export default {
  name: 'OwnedProfile',
  props: {
    speciesName: String,
    ownedId: Number,
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
    isShiny: Boolean,
    level: Number,
    gender: String,
    ability: String,
    move1: String,
    move2: String,
    move3: String,
    move4: String,
  },
  data() {
    return {
      isEditing: false,
      error: '',
      genderOptions: [
        { text: 'Unknown', value: 'unknown' },
        { text: 'Male', value: 'male' },
        { text: 'Female', value: 'female' },
      ],
      shinyOptions: [
        { text: 'No', value: 'FALSE' },
        { text: 'Yes', value: 'TRUE' },
      ],
      abilityOptions: [],
    }
  },
  methods: {
    getParams() {
      return {
        nickname: this.pokemon,
        level: this.level,
        hp: this.hp,
        spd: this.spd,
        atk: this.atk,
        def: this.def,
        spAtk: this.spAtk,
        spDef: this.spDef,
        move1: this.move1,
        move2: this.move2,
        move3: this.move3,
        move4: this.move4,
        ownedId: this.ownedId
      }
    },
    onDelete(evt) {
      evt.preventDefault()
      //console.log(this)
      var path = 'http://127.0.0.1:5000/deleteownedpokemon'
      axios.post(path, {ownedId: this.ownedId})
        .then(() => {
          //console.log("Deleted")
          this.$parent.getPokemon()
        }).catch((error) => {
           // eslint-disable-next-line
           console.error(error);
        });
    },
    onEdit(evt) {
      evt.preventDefault()
      console.log("editing")
      this.isEditing = true
    },
    onSubmit(evt) {
      evt.preventDefault()
      var path = 'http://127.0.0.1:5000/changeownedpokemon'
      axios.post(path, this.getParams())
        .then((res) => {
          //console.log("Deleted")
          if (res.data.status == "failure") {
            this.error = res.data.error;
          } else {
            this.error = '';
            this.isEditing = false
            this.$parent.getPokemon()
          }
        }).catch((error) => {
           // eslint-disable-next-line
           console.error(error);
        });
    },
    onReset(evt) {
      evt.preventDefault()
      this.isEditing = false
    }
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