<template>
<div>
  <myHeader />
  <br>
  <div style="padding: 20px;">
  <b-container class="bv-example-row">
    <b-button pill v-b-toggle.collapse-1 variant="info" style="margin-right:10px;">Filters</b-button>
    <b-button pill v-b-toggle.collapse-2 variant="info">Create Pokémon</b-button>
    <b-collapse v-model="filtersVisible" id="collapse-1" class="mt-2">
      <b-card border-variant="dark">
        <b-form @submit="onSubmit" @reset="onReset" class="w-100">
          <b-form-row>
            <b-col><label class="mr-1">Nickname:</label><b-form-input type="text" v-model="pokemonInfo.nickname" placeholder="Enter a nickname" /></b-col>
            <b-col><label class="mr-1">Move:</label><br><b-form-input type="text" v-model="pokemonInfo.move" placeholder="Enter a move" /></b-col>
            <b-col><label class="mr-1">Ability:</label><b-form-input v-model="pokemonInfo.ability" placeholder="Enter an ability" /></b-col>
            <b-col><label class="mr-1">Gender:</label><br><b-form-radio-group style="width: 100%;" v-model="pokemonInfo.gender" :options="genderOptions" buttons button-variant="outline-secondary" /></b-col>
            <b-col><label class="mr-1">Shiny:</label><br><b-form-radio-group style="width: 100%;" v-model="pokemonInfo.shiny" :options="shinyOptions" buttons button-variant="outline-secondary" /></b-col>
          </b-form-row>
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


    <b-collapse v-model="createVisible" id="collapse-2" class="mt-2">
      <b-card border-variant="dark">
        <b-form @submit="onSubmitSpecies" v-show="!this.createInfo.species" class="w-100">
        <b-form-group id="form-name-group"
                      label="Enter a species:"
                      label-for="form-name-input">
            <b-form-input id="form-name-input"
                          type="text"
                          v-model="species"
                          placeholder="Enter Pokemon Name">
            </b-form-input>
          </b-form-group>
          <div style="color: red;" v-show="this.msg">{{ this.msg }}</div>
          <b-container class="bv-example-row">
            <b-row align-h="end">
              <b-col md="auto"><b-button type="submit" pill variant="success">Start</b-button></b-col>
            </b-row>
          </b-container>
        </b-form>
        <b-form @submit="onSubmitCreate" @reset="onResetCreate" v-show="this.createInfo.species" class="w-100">
          <b-form-row>
            <b-col><label class="mr-1">Nickname:</label><b-form-input type="text" v-model="createInfo.nickname" placeholder="Enter a nickname" /></b-col>
            <b-col><label class="mr-1">Ability:</label><b-form-select v-model="createInfo.ability" :options="abilityOptions" /></b-col>
            <b-col><label class="mr-1">Gender:</label><br><b-form-radio-group style="width: 100%;" v-model="createInfo.gender" :options="genderOptions" buttons button-variant="outline-secondary" /></b-col>
            <b-col><label class="mr-1">Shiny:</label><br><b-form-radio-group style="width: 100%;" v-model="createInfo.shiny" :options="shinyOptions" buttons button-variant="outline-secondary" /></b-col>
          </b-form-row>
          <br>
          <b-form-row>
            <b-col><label class="mr-1">Level:</label><b-form-input type="number" v-model="createInfo.level" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">HP:</label><b-form-input type="number" v-model="createInfo.hp" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Spd:</label><b-form-input type="number" v-model="createInfo.spd" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Atk:</label><b-form-input type="number" v-model="createInfo.atk" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Def:</label><b-form-input type="number" v-model="createInfo.def" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">SpAtk:</label><b-form-input type="number" v-model="createInfo.spAtk" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">SpDef:</label><b-form-input type="number" v-model="createInfo.spDef" placeholder="Enter #" /></b-col>
          </b-form-row>
          <br>
          <b-form-row>
            <b-col><label class="mr-1">Move 1:</label><b-form-input required type="text" v-model="createInfo.move1" placeholder="Enter a move" /></b-col>
            <b-col><label class="mr-1">Move 2:</label><b-form-input type="text" v-model="createInfo.move2" placeholder="Enter a move" /></b-col>
            <b-col><label class="mr-1">Move 3:</label><b-form-input type="text" v-model="createInfo.move3" placeholder="Enter a move" /></b-col>
            <b-col><label class="mr-1">Move 4:</label><b-form-input type="text" v-model="createInfo.move4" placeholder="Enter a move" /></b-col>
          </b-form-row>
          <div style="color: red;" v-show="this.error">{{ this.error }}</div>
          <br>
          <b-container class="bv-example-row">
            <b-row align-h="end">
              <b-col md="auto"><b-button type="reset" pill variant="danger">Change Species</b-button></b-col>
              <b-col md="auto"><b-button type="submit" pill variant="success">Create</b-button></b-col>
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
    <h1>My Pok&eacute;mon</h1>
    <hr>
    <h4>Click on a Pok&eacute;mon's image to learn more about its species.</h4>
    <br>
    <b-row v-for="(row, index) in ownedpokemon" :key="index">
      <b-col v-for="(mon, index) in row" :key="index">
      <ownedprofile
        v-bind:id="mon.species" v-bind:pokemon="mon.name"
        v-bind:speciesName="mon.speciesName"
        v-bind:types="mon.types" v-bind:colors="mon.colors"
        v-bind:hp="mon.hp" v-bind:spd="mon.spd"
        v-bind:atk="mon.atk" v-bind:def="mon.def"
        v-bind:spAtk="mon.spAtk" v-bind:spDef="mon.spDef"
        v-bind:isShiny="mon.isShiny" v-bind:ownedId="mon.ownedId"
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
  </b-container>
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
  import { mapState } from 'vuex';
  export default {
    computed: mapState({
      username: state => state.username
    }),
    data() {
      return {
        ownerID: 0,
        ownedpokemon: [],
        filtersVisible: false,
        createVisible: false,
        msg: "",
        error: '',
        species: '',
        pokemonInfo: {
            nickname: '',
            move: '',
            ability: '',
            gender: '',
            shiny: ''
        },

         createInfo: {
            nickname: '',
            id: '',
            gender: 'unknown',
            shiny: 'false',
            hp: '',
            level: '1',
            spd: '',
            atk: '',
            def: '',
            atk: '',
            spDef: '',
            ability: '',
            move1: '',
            move2: '',
            move3: '',
            move4: ''
            //evolutions: false
        },
        genderOptions: [
          { text: 'Unknown', value: 'unknown' },
          { text: 'Male', value: 'male' },
          { text: 'Female', value: 'female' },
        ],
        shinyOptions: [
          { text: 'No', value: 'FALSE' },
          { text: 'Yes', value: 'TRUE' },
        ],

        abilityOptions: [
        ],

        damageTypes: ['Physical', 'Special'],
      };
    },
    methods: {
      getPokemon() {
        var path = 'http://127.0.0.1:5000/ownedpokemon'
        console.log(path);
        axios.post(path, {username: this.username, info: this.pokemonInfo})
          .then((res) => {
            this.ownedpokemon = res.data.ownedpokemon;
            console.log(this.ownedpokemon)
            this.filtersVisible = false
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
      initCreateForm() {

        this.createInfo = {
            nickname: '',
            species: '',
            gender: 'unknown',
            shiny: 'false',
            level: '1',
            hp: '',
            spd: '',
            atk: '',
            def: '',
            atk: '',
            spDef: '',
            ability: '',
            move1: '',
            move2: '',
            move3: '',
            move4: ''
        };

        this.abilityOptions = [];

      },
      initPokemonForm() {
        this.pokemonInfo = {
            nickname: '',
            move: '',
            ability: '',
            gender: '',
            shiny: ''
        }
      },
      onSubmit(evt) {
        evt.preventDefault();
        this.getPokemon();
      },
      onReset(evt) {
        evt.preventDefault();
        console.log("reset")
        this.initPokemonForm();
        this.getPokemon();
      },
      onSubmitCreate(evt) {
        evt.preventDefault();
        var path = 'http://127.0.0.1:5000/createownedpokemon'
        console.log(path);
        axios.post(path, {username: this.username, createInfo: this.createInfo})
          .then((res) => {
            if (res.data.status == "failure") {
                this.error = res.data.error;
            } else {
                this.error = '';
                this.createVisible = false;
                this.initCreateForm();
                this.getPokemon();
            }
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
      onResetCreate(evt) {
        evt.preventDefault();
        this.initCreateForm();
      },
      onSubmitSpecies(evt) {
        evt.preventDefault();
        var path = 'http://127.0.0.1:5000/getspeciesinfo'
        console.log(path);
        axios.post(path, {species: this.species})
          .then((res) => {
            console.log(res.data.pokemon);
            if (res.data.pokemon.length > 0) {
              this.createInfo.id = res.data.pokemon[0]['id']
              this.createInfo.hp = res.data.pokemon[0]['hp']
              this.createInfo.spd = res.data.pokemon[0]['spd']
              this.createInfo.atk = res.data.pokemon[0]['atk']
              this.createInfo.def = res.data.pokemon[0]['def']
              this.createInfo.spAtk = res.data.pokemon[0]['spAtk']
              this.createInfo.spDef = res.data.pokemon[0]['spAtk']
              this.abilityOptions.push(
                { text: res.data.pokemon[0]['ability1'], value: res.data.pokemon[0]['ability1']})
              if (res.data.pokemon[0]['ability2']) {
                this.abilityOptions.push(
                { text: res.data.pokemon[0]['ability2'], value: res.data.pokemon[0]['ability2']})
              } else{
                this.createInfo.ability = res.data.pokemon[0]['ability1']
              }
              this.createInfo.species = this.species;
            } else {
              this.msg = "Invalid species, try again!"
            }
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
    },
    created() {
        //this.ownerID = 69 // replace with actual owner ID
        this.getPokemon();
    }
  };
</script>
