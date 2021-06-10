<template>
<div>
  <myHeader />
  <b-container class="bv-example-row">
    <h1>Pokemon</h1>
    <hr><br>
    <b-row v-for="(row, index) in pokemon" :key="index">
      <b-col v-for="(mon, index) in row" :key="index">
      <profile
        v-bind:id="mon.id" v-bind:pokemon="mon.name"
        v-bind:types="mon.types"
        v-bind:hp="mon.hp" v-bind:spd="mon.spd"
        v-bind:atk="mon.atk" v-bind:def="mon.def"
        v-bind:spAtk="mon.spAtk" v-bind:spDef="mon.spDef"
        />
      <br><br>
      </b-col>
    </b-row>
  </b-container>
</div>
</template>

<script>
export default {
  name: 'Pokedex',
  props: {
    msg: String
  }
}
</script>

<script>
  import axios from "axios";
  export default {
    data() {
      return {
        pokemon: [],
      };
    },
    methods: {
      getPokemon() {
        const path = 'http://localhost:5000/pokedex'
        axios.get(path)
          .then((res) => {
            this.pokemon = res.data.pokemon;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
    },
    created() {
      this.getPokemon();
    },
  };
</script>
