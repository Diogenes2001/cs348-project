<template>
<div style="padding-bottom: 40px;">
    <myHeader />
    <div style="padding-top: 40px;">
    <b-container class="bv-example-row">
    <b-form @submit="onSubmit">
        <b-form-row>
            <b-col><b-form-input v-model="pokemonNameFilter" placeholder="Enter a Pokemon Name"></b-form-input></b-col>
            <b-col md="auto"><b-button pill type="submit" variant="info">Submit</b-button></b-col>
        </b-form-row>
    </b-form>
    </b-container>
    </div>
    <br><br>
    <div>
    <b-container class="bv-example-row">
    <h1>Our Team Picks</h1>
    <hr><br>
    <b-row v-if="programGeneratedTeams.length == 0" align-h="center">(No Teams Found &#9785;)</b-row>
    <b-row v-for="(team, index) in programGeneratedTeams" :key="index" align-h="center" class="row-style">
        <b-col cols="0.1" :style="'color: DarkGray'">{{ index + 1 }}</b-col>
        <b-col v-for="(pokemon, index2) in team" :key="index2" md="auto">
            <a v-bind:href="'/pokemon/'+ pokemon[0]">
                <div class="bounce-container">
                <b-img center v-bind:src="require(`@/assets/pokemon/${pokemon[0]}.png`)" width="150%" height="150%" :id="`program-${index}-${index2}`" class="image-style bounce-item"/>
                </div>
                <b-popover :target="`program-${index}-${index2}`" triggers="hover" placement="bottom">
                    {{pokemon[1]}}
                </b-popover>
            </a>
        </b-col>
    </b-row>
    </b-container>
    </div>
    <br>
    <div>
    <b-container class="bv-example-row">
    <h1>Users' Team Picks</h1>
    <hr><br>
    <b-row v-if="userGeneratedTeams.length == 0" align-h="center">(No Teams Found &#9785;)</b-row>
    <b-row v-for="(team, index) in userGeneratedTeams" :key="index" align-h="center" class="row-style">
        <b-col cols="0.1" :style="'color: DarkGray'">{{ index + 1 }}</b-col>
        <b-col v-for="(pokemon, index2) in team" :key="index2" md="auto">
            <a v-bind:href="'/pokemon/'+ pokemon[0]">
                <div class="bounce-container">
                <b-img center v-bind:src="require(`@/assets/pokemon/${pokemon[0]}.png`)" width="150%" height="150%" :id="`user-${index}-${index2}`" class="bounce-item"/>
                </div>
                <b-popover :target="`user-${index}-${index2}`" triggers="hover" placement="bottom">
                    {{pokemon[1]}}
                </b-popover>
            </a>
        </b-col>
    </b-row>
    </b-container>
    </div>
</div>
</template>

<script>
export default {
  name: 'TeamGeneration'
}
</script>

<script>
    import axios from "axios";
    export default {
        data() {
            return {
                programGeneratedTeams: [],
                userGeneratedTeams: [],
                pokemonNameFilter: ""
            }
        },
        methods: {
            getTeams(programGenerated, params, callback) {
                var path = 'http://127.0.0.1:5000/'
                         + (programGenerated ? 'program_generated_teams' : 'user_generated_teams');
                axios.post(path, params)
                     .then((res) => {
                        callback(res.data.teams);
                     })
            },
            getParams() {
                const params = {
                    pokemonNameFilter: this.pokemonNameFilter
                };
                return params;
            },
            getProgramAndUserTeams() {
                const params = this.getParams();
                this.getTeams(true, params, (response) => {
                    this.programGeneratedTeams = response;
                    this.getTeams(false, params, (response) => {
                        this.userGeneratedTeams = response;
                    });
                });
            },
            onSubmit(event) {
                event.preventDefault()
                this.getProgramAndUserTeams();
            }
        },
        created() {
            this.getProgramAndUserTeams();
        },
    };
</script>

<style>
.row-style {
  padding: 1rem 0rem !important;
  margin-bottom: 2rem !important;
  background: WhiteSmoke;
  border-radius: 25px;
}
.image-style {
  -webkit-transform: translate3d(0,0,0);
  -webkit-backface-visibility: hidden;
  transform: translate3d(0,0,0);
}
.bounce-item {
    align-self: flex-end;
    animation-duration: 0.5s;
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
  100% { transform: translateY(-3px); }
}
</style>
