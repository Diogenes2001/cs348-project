<template>
<div>
  <myHeader />
  <br>
  <div>
  <b-row v-for="(row, index) in pokemon" :key="index">
      <b-col v-for="(mon, index) in row" :key="index">
      <profile
        v-bind:id="mon.id" v-bind:pokemon="mon.name"
        v-bind:types="mon.types" v-bind:colors="mon.colors"
        v-bind:hp="mon.hp" v-bind:spd="mon.spd"
        v-bind:atk="mon.atk" v-bind:def="mon.def"
        v-bind:spAtk="mon.spAtk" v-bind:spDef="mon.spDef"
        v-bind:moves="mon.moves"
        />
      <br><br>
      </b-col>
    </b-row>
  </div>
  <b-container class="bv-example-row">
    <h1>Evolutions</h1>
    <hr>
    <h4>{{ msg }}</h4>
    <br>
    <b-row v-for="(row, index) in evolutions" :key="index">
      <b-col v-for="(mon, index) in row" :key="index">
      <profile
        v-bind:id="mon.id" v-bind:pokemon="mon.name"
        v-bind:types="mon.types" v-bind:colors="mon.colors"
        v-bind:hp="mon.hp" v-bind:spd="mon.spd"
        v-bind:atk="mon.atk" v-bind:def="mon.def"
        v-bind:spAtk="mon.spAtk" v-bind:spDef="mon.spDef"
        v-bind:evolvesFromName="mon.evolvesFromName"
        />
      <br><br>
      </b-col>
    </b-row>
  </b-container>
  <b-container class="bv-example-row">
    <h1>Weaknesses and Resistances</h1>
    <hr>
    <h4>When used against this Pokémon, a move of the given type has:</h4>
    <br>
    <b-row class="justify-content-md-center">
      <table class="table">
        <tbody>
          <b-col v-for="e in effectiveness" :key="e">
            <td>
              <h4>
                <b-badge pill :pressed="true" variant="dark" v-bind:style="{ 'background-color' : e['color'] }">
                {{ e['moveType'] }}
                </b-badge>
                :
                x{{ e['effectiveness'] }} effectiveness
              </h4>
            </td>
          </b-col>
        </tbody>
      </table>
    </b-row>
  </b-container>
</div>
</template>

<script>
export default {
  name: 'Pokemon',
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
        pokemonId: null,
        evolutions: [],
        effectiveness: [],
        msg: "Click on a Pokémon's image to learn more."
      };
    },
    methods: {
      getPokemon(id) {
        var path = 'http://127.0.0.1:5000/pokemon'
        console.log(path);
        axios.post(path, {id: id})
          .then((res) => {
            this.pokemon = res.data.pokemon;
            this.evolutions = res.data.evolutions;
            this.effectiveness = res.data.effectiveness;
            console.log(this.evolutions)
            console.log(this.effectiveness)
            if(this.evolutions[0].length == 0){
              this.msg = "This Pokemon does not evolve."
            }
            console.log(res.data.message);
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
    },
    created() {
        this.pokemonId = this.$route.params.id
        this.getPokemon(this.pokemonId);
    },
  };
</script>
