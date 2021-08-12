<template>
<div>
  <myHeader />
  <div style="padding-top: 20px;">
  <b-container class="bv-example-row">
    <b-button pill v-b-toggle.collapse-1 variant="info">Filters</b-button>
    <b-collapse v-model="visible" id="collapse-1" class="mt-2">
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
          <!-- <b-form-checkbox
            id="checkbox-1"
            v-model="pokemonInfo.evolutions"
            name="checkbox-1"
            value=true
            unchecked-value=false
          >
            Show Evolutions
          </b-form-checkbox> -->
          <br>
          <b-form-row>
            <b-col><label class="mr-1">ID:</label><b-form-input type="number" v-model="pokemonInfo.id" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Max HP:</label><b-form-input type="number" v-model="pokemonInfo.maxBaseHp" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Max Spd:</label><b-form-input type="number" v-model="pokemonInfo.maxBaseSpd" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Max Atk:</label><b-form-input type="number" v-model="pokemonInfo.maxBaseAtk" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Max Def:</label><b-form-input type="number" v-model="pokemonInfo.maxBaseDef" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Max SpAtk:</label><b-form-input type="number" v-model="pokemonInfo.maxBaseSpAtk" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Max SpDef:</label><b-form-input type="number" v-model="pokemonInfo.maxBaseSpDef" placeholder="Enter #" /></b-col>
          </b-form-row>
          <br>
          <b-form-row>
            <b-col><label class="mr-1">Min HP:</label><b-form-input type="number" v-model="pokemonInfo.minBaseHp" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Min Spd:</label><b-form-input type="number" v-model="pokemonInfo.minBaseSpd" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Min Atk:</label><b-form-input type="number" v-model="pokemonInfo.minBaseAtk" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Min Def:</label><b-form-input type="number" v-model="pokemonInfo.minBaseDef" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Min SpAtk:</label><b-form-input type="number" v-model="pokemonInfo.minBaseSpAtk" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Min SpDef:</label><b-form-input type="number" v-model="pokemonInfo.minBaseSpDef" placeholder="Enter #" /></b-col>
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
                            v-model="moveInfo.moveName"
                            placeholder="Enter Move Name">
              </b-form-input>
            </b-form-group>
          <b-form-row>
            <b-col><label class="mr-1">Max PP:</label><b-form-input type="number" v-model="moveInfo.maxPp" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Max Power:</label><b-form-input type="number" v-model="moveInfo.maxPower" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Max Accuracy:</label><b-form-input type="number" v-model="moveInfo.maxAccuracy" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Damage Type:</label><b-form-input v-model="moveInfo.damageType" placeholder="Select Type" list="damage-type-list"></b-form-input>
              <datalist id="damage-type-list">
                <option v-for="(type, index) in damageTypes" :key="index">{{ type }}</option>
              </datalist>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col><label class="mr-1">Min PP:</label><b-form-input type="number" v-model="moveInfo.minPp" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Min Power:</label><b-form-input type="number" v-model="moveInfo.minPower" placeholder="Enter #" /></b-col>
            <b-col><label class="mr-1">Min Accuracy:</label><b-form-input type="number" v-model="moveInfo.minAccuracy" placeholder="Enter #" /></b-col>
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
          <b-form-group label="Weaknesses:">
              <b-form-checkbox-group
                id="checkbox-group-3"
                v-model="effectiveness.weaknesses"
                :options="options"
                name="weaknesses"
              ></b-form-checkbox-group>
            </b-form-group>
          <br>
          <b-form-group label="Resistances:">
              <b-form-checkbox-group
                id="checkbox-group-4"
                v-model="effectiveness.resistances"
                :options="options"
                name="resistances"
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
    <hr>
    <h4>Click on a Pok&eacute;mon's image to learn more.</h4>
    <br>
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
        visible: false,
        pokemonInfo: {
            name: '',
            id: '',
            maxBaseHp: '',
            maxBaseSpd: '',
            maxBaseAtk: '',
            maxBaseDef: '',
            maxBaseSpAtk: '',
            maxBaseSpDef: '',
            minBaseHp: '',
            minBaseSpd: '',
            minBaseAtk: '',
            minBaseDef: '',
            minBaseSpAtk: '',
            minBaseSpDef: '',
            types: [],
            //evolutions: false
        },
        moveInfo: {
            name: '',
            types: [],
            damageType: '',
            maxPp: '',
            maxPower: '',
            maxAccuracy: '',
            minPp: '',
            minPower: '',
            minAccuracy: '',
        },
        effectiveness: {
            weaknesses: [],
            resistances: [],
        },
        options: [
          { text: 'Normal', value: 'Normal' },
          { text: 'Fire', value: 'Fire' },
          { text: 'Water', value: 'Water' },
          { text: 'Grass', value: 'Grass' },
          { text: 'Electric', value: 'Electric' },
          { text: 'Ice', value: 'Ice' },
          { text: 'Fighting', value: 'Fighting' },
          { text: 'Poison', value: 'Poison' },
          { text: 'Ground', value: 'Ground' },
          { text: 'Flying', value: 'Flying' },
          { text: 'Psychic', value: 'Psychic' },
          { text: 'Bug', value: 'Bug' },
          { text: 'Rock', value: 'Rock' },
          { text: 'Ghost', value: 'Ghost' },
          { text: 'Dark', value: 'Dark' },
          { text: 'Dragon', value: 'Dragon' },
          { text: 'Steel', value: 'Steel' },
          { text: 'Fairy', value: 'Fairy' },
        ],
        damageTypes: ['Physical', 'Special'],
      };
    },
    methods: {
      getPokemon(params) {
        var path = 'http://127.0.0.1:5000/pokedex'
        if (this.name && this.evolutions == "true") {
          path = 'http://127.0.0.1:5000/evolutions'
        }
        console.log(path);
        axios.post(path, params)
          .then((res) => {
            this.pokemon = res.data.pokemon;
            console.log(res.data.message);
            this.visible = false;
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
        this.pokemonInfo.maxBaseHp = '';
        this.pokemonInfo.maxBaseSpd = '';
        this.pokemonInfo.maxBaseAtk = '';
        this.pokemonInfo.maxBaseDef = '';
        this.pokemonInfo.maxBaseSpAtk = '';
        this.pokemonInfo.maxBaseSpDef = '';
        this.pokemonInfo.minBaseHp = '';
        this.pokemonInfo.minBaseSpd = '';
        this.pokemonInfo.minBaseAtk = '';
        this.pokemonInfo.minBaseDef = '';
        this.pokemonInfo.minBaseSpAtk = '';
        this.pokemonInfo.minBaseSpDef = '';
        //this.pokemonInfo.evolutions = false;

        this.moveInfo.moveName = '';
        this.moveInfo.types = [];
        this.moveInfo.damageType = '';
        this.moveInfo.maxPp = '';
        this.moveInfo.maxPower = '';
        this.moveInfo.maxAccuracy = '';
        this.moveInfo.minPP = '';
        this.moveInfo.minPower = '';
        this.moveInfo.minAccuracy = '';

        this.effectiveness.weaknesses = []
        this.effectiveness.resistances = []
      },
      getParams() {
        const params = {
          pokemonInfo: this.pokemonInfo,
          moveInfo: this.moveInfo,
          effectiveness: this.effectiveness
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
