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
                          v-model="pokemonInfo.name"
                          placeholder="Enter Pokemon Name">
            </b-form-input>
          </b-form-group>
          <b-form-checkbox
            id="checkbox-1"
            v-model="pokemonInfo.evolutions"
            name="checkbox-1"
            value=true
            unchecked-value=false
          >
            Show Evolutions
          </b-form-checkbox>
          <br>
          <b-form-row>
            <b-col><label class="mr-1">ID:</label><b-form-input type="number" v-model="pokemonInfo.id" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">HP:</label><b-form-input type="number" v-model="pokemonInfo.hp" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Spd:</label><b-form-input type="number" v-model="pokemonInfo.spd" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Atk:</label><b-form-input type="number" v-model="pokemonInfo.atk" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Def:</label><b-form-input type="number" v-model="pokemonInfo.def" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">SpAtk:</label><b-form-input type="number" v-model="pokemonInfo.spAtk" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">SpDef:</label><b-form-input type="number" v-model="pokemonInfo.spDef" placeholder="Enter #" /></b-col>
          </b-form-row>
          <br>
          <b-form-group label="Type:">
            <b-form-checkbox-group
              id="checkbox-group-1"
              v-model="pokemonInfo.types"
              :options="options"
              name="types"
            ></b-form-checkbox-group>
          </b-form-group>
          <b-form-group id="form-move-group"
                        label="Move Name:"
                        label-for="form-move-input">
              <b-form-input id="form-move-input"
                            type="text"
                            v-model="moveInfo.name"
                            placeholder="Enter Move Name">
              </b-form-input>
            </b-form-group>
          <b-form-row>
            <b-col><label class="mr-1">PP:</label><b-form-input type="number" v-model="moveInfo.pp" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Power:</label><b-form-input type="number" v-model="moveInfo.power" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Accuracy:</label><b-form-input type="number" v-model="moveInfo.accuracy" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Damage Type:</label><b-form-input v-model="moveInfo.damageType" placeholder="Select Type" list="damage-type-list"></b-form-input>
              <datalist id="damage-type-list">
                <option v-for="(type, index) in damageTypes" :key="index">{{ type }}</option>
              </datalist>
            </b-col>
          </b-form-row>
          <br>
          <b-form-group label="Move Type:">
              <b-form-checkbox-group
                id="checkbox-group-2"
                v-model="moveInfo.types"
                :options="options"
                name="moveTypes"
              ></b-form-checkbox-group>
            </b-form-group>
          <br>
          <b-container class="bv-example-row">
            <b-row align-h="end">
              <b-col md="auto"><b-button type="reset" pill variant="danger">Reset</b-button></b-col>
              <b-col md="auto"><b-button type="submit" pill variant="success">Submit</b-button></b-col>
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
    <h1>Pok&eacute;dex</h1>
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
        pokemonInfo: {
            name: '',
            id: '',
            hp: '',
            spd: '',
            atk: '',
            def: '',
            spAtk: '',
            spDef: '',
            types: [],
            evolutions: false
        },
        moveInfo: {
            name: '',
            type: '',
            pp: '',
            power: '',
            damageType: '',
            accuracy: '',
        },
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
        ],
        damageTypes: ['Physical', 'Special'],
      };
    },
    methods: {
      getPokemon(params) {
        var path = 'http://localhost:5000/pokedex'
        if (this.name && this.evolutions == "true") {
          path = 'http://localhost:5000/evolutions'
        }
        console.log(path);
        axios.post(path, params)
          .then((res) => {
            this.pokemon = res.data.pokemon;
            console.log(res.data.message);
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
      initForm() {
        this.pokemonInfo.name = '';
        this.pokemonInfo.types = [];
        this.pokemonInfo.id = '';
        this.pokemonInfo.hp = '';
        this.pokemonInfo.spd = '';
        this.pokemonInfo.atk = '';
        this.pokemonInfo.def = '';
        this.pokemonInfo.spAtk = '';
        this.pokemonInfo.spDef = '';
        this.pokemonInfo.evolutions = false;

        this.moveInfo.name = '';
        this.moveInfo.types = [];
        this.moveInfo.PP = '';
        this.moveInfo.power = '';
        this.moveInfo.damageType = '';
        this.moveInfo.accuracy = '';
      },
      getParams() {
        const params = {
          pokemonInfo: this.pokemonInfo,
          moveInfo: this.moveInfo
        };
        return params;
      },
      onSubmit(evt) {
        evt.preventDefault();
        const params = this.getParams();
        this.getPokemon(params);
      },
      onReset(evt) {
        evt.preventDefault();
        this.initForm();
        const params = this.getParams();
        this.getPokemon(params);
      },
    },
    created() {
      const params = this.getParams();
      this.getPokemon(params);
    },
  };
</script>
