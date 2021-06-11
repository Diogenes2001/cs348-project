<template>
<div>
  <myHeader />
  <div>
  <b-container class="bv-example-row">
    <b-button pill v-b-toggle.collapse-1 variant="info">Filters</b-button>
    <b-collapse id="collapse-1" class="mt-2">
      <b-card border-variant="dark">
        <b-form @submit="onSubmit" @reset="onReset" class="w-100">
          <b-form-group id="form-name-group"
                      label="Name:"
                      label-for="form-name-input">
            <b-form-input id="form-name-input"
                          type="text"
                          v-model="name"
                          placeholder="Enter Pokemon Name">
            </b-form-input>
          </b-form-group>
          <b-form-group label="Type:">
            <b-form-checkbox-group
              id="checkbox-group-1"
              v-model="types"
              :options="options"
              name="types"
            ></b-form-checkbox-group>
          </b-form-group>
          <b-container class="bv-example-row">
            <b-row align-h="end">
              <b-col md="auto"><b-button type="submit" pill variant="success">Ok</b-button></b-col>
              <b-col md="auto"><b-button type="reset" pill variant="danger">Reset</b-button></b-col>
            </b-row>
          </b-container>
        </b-form>
      </b-card>
    </b-collapse>
  </b-container>
  </div>
  <br>
  <div>
  <b-container class="bv-example-row">
    <h1>Pokemon</h1>
    <hr><br>
    <b-row v-for="(row, index) in pokemon" :key="index">
      <b-col v-for="(mon, index) in row" :key="index">
      <profile
        v-bind:id="mon.id" v-bind:pokemon="mon.name"
        v-bind:types="mon.types" v-bind:colors="mon.colors"
        v-bind:hp="mon.hp" v-bind:spd="mon.spd"
        v-bind:atk="mon.atk" v-bind:def="mon.def"
        v-bind:spAtk="mon.spAtk" v-bind:spDef="mon.spDef"
        />
      <br><br>
      </b-col>
    </b-row>
  </b-container>
  </div>
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
        name: '',
        types: [],
        message: '',
        options: [
          { text: 'Normal', value: 'normal' },
          { text: 'Fire', value: 'fire' },
          { text: 'Water', value: 'water' },
          { text: 'Grass', value: 'grass' },
          { text: 'Electric', value: 'electric' },
          { text: 'Ice', value: 'ice' },
          { text: 'Fighting', value: 'fighting' },
          { text: 'Poison', value: 'poison' },
          { text: 'Ground', value: 'ground' },
          { text: 'Flying', value: 'flying' },
          { text: 'Psychic', value: 'psychic' },
          { text: 'Bug', value: 'bug' },
          { text: 'Rock', value: 'rock' },
          { text: 'Ghost', value: 'ghost' },
          { text: 'Dark', value: 'dark' },
          { text: 'Dragon', value: 'dragon' },
          { text: 'Steel', value: 'steel' },
          { text: 'Fairy', value: 'fairy' },
        ]
      };
    },
    methods: {
      getPokemon(params) {
        const path = 'http://localhost:5000/pokedex'
        axios.post(path, params)
          .then((res) => {
            this.pokemon = res.data.pokemon;
            this.message = res.data.message;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
      initForm() {
        this.name = '';
        this.types = [];
      },
      onSubmit(evt) {
        evt.preventDefault();
        const params = {
          name: this.name,
          types: this.types
        };
        this.getPokemon(params);
      },
      onReset(evt) {
        evt.preventDefault();
        this.initForm();
        const params = {
          name: this.name,
          types: this.types
        };
        this.getPokemon(params);
      },
    },
    created() {
      const params = {
        name: this.name,
        types: this.types
      };
      this.getPokemon(params);
    },
  };
</script>
