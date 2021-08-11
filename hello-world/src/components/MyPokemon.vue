<template>
<div>
  <myHeader />
  <br>
  <div>
  <b-row v-for="(row, index) in ownedpokemon" :key="index">
      <b-col v-for="(mon, index) in row" :key="index">
      <ownedprofile
        v-bind:id="mon.species" v-bind:pokemon="mon.name"
        v-bind:speciesName="mon.speciesName"
        v-bind:types="mon.types" v-bind:colors="mon.colors"
        v-bind:hp="mon.hp" v-bind:spd="mon.spd"
        v-bind:atk="mon.atk" v-bind:def="mon.def"
        v-bind:spAtk="mon.spAtk" v-bind:spDef="mon.spDef"
        v-bind:isShiny="mon.isShiny"
        v-bind:gender="mon.gender"
        v-bind:ability="mon.ability"
        v-bind:level="mon.level"
        v-bind:move1="mon.move1"
        v-bind:move2="mon.move2"
        v-bind:move3="mon.move3"
        v-bind:move4="mon.move4"
        />
      <br><br>
      </b-col>
    </b-row>
  </div>
</div>
</template>

<script>
export default {
  name: 'MyPokemon',
  props: {
      ownerID: Number,
  }
}
</script>

<script>
  import axios from "axios";
  export default {
    data() {
      return {
        ownerID: 0,
        ownedpokemon: [],
        msg: "Click on a Pokémon's image to learn more."
      };
    },
    methods: {
      getPokemon(id) {
        var path = 'http://127.0.0.1:5000/ownedpokemon'
        console.log(path);
        axios.post(path, {id: id})
          .then((res) => {
            this.ownedpokemon = res.data.ownedpokemon;
            console.log(this.ownedpokemon)
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
    },
    created() {
        this.ownerID = 69 // replace with actual owner ID
        this.getPokemon(this.ownerID);
    },
  };
</script>
