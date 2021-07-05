<template>
<div style="padding-bottom: 40px;">
    <myHeader />
    <div style="padding-top: 40px;">
    <b-container class="bv-example-row">
    <b-form @submit="onSubmit">
        <b-form-input v-model="pokemonNameFilter" placeholder="Enter a Pokemon Name" @input.native="onChange"></b-form-input>
        <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
    </b-container>
    </div>
    <br><br>
    <div>
    <b-container class="bv-example-row">
    <h1>Our Team Picks</h1>
    <hr><br>
    <b-row v-for="(team, index) in programGeneratedTeams" :key="index">
        <b-col v-for="(pokemon, index2) in team" :key="index2" md="auto">
            <a v-bind:href="'/pokemon/'+ pokemon[0]">
                <b-img center v-bind:src="require(`@/assets/pokemon/${pokemon[0]}.png`)" width="150%" height="150%" :id="`program-${index}-${index2}`" />
                <b-popover :target="`program-${index}-${index2}`" triggers="hover" placement="bottom">
                    {{pokemon[1]}}
                </b-popover>
            </a>
        </b-col>
    </b-row>
    </b-container>
    </div>
    <br><br>
    <div>
    <b-container class="bv-example-row">
    <h1>Users' Team Picks</h1>
    <hr><br>
    <b-row v-for="(team, index) in userGeneratedTeams" :key="index">
        <b-col v-for="(pokemon, index2) in team" :key="index2" md="auto">
            <a v-bind:href="'/pokemon/'+ pokemon[0]">
                <b-img center v-bind:src="require(`@/assets/pokemon/${pokemon[0]}.png`)" width="150%" height="150%" :id="`user-${index}-${index2}`" />
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
