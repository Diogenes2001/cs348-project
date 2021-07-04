<template>
<div class="bg">
  <myHeader />
    <b-container class="h-100">
    <b-row align-h="center" style="padding-top: 60px;">
    <b-card style="width: 400px;" header="Login" border-variant="dark" header-class="h1 text-center" header-bg-variant="white">
        <div>
            <b-form @submit="onSubmit" @reset="onReset">
                <b-form-group id="input-group-1" label="Username" label-for="input-1">
                    <b-form-input
                    id="input-1"
                    v-model="form.username"
                    placeholder="Enter name"
                    required
                    ></b-form-input>
                </b-form-group>

                <b-form-group id="input-group-3" label="Password" label-for="input-3">
                    <b-form-input type="password" v-model="form.password" id="input-3" placeholder="Enter password" required></b-form-input>
                </b-form-group>

                <div style="color: red; padding-bottom: 5px;" v-show="this.error">{{ this.error }}</div>

                <b-button type="submit" variant="primary" style="width: 48%;">Submit</b-button>
                <b-button href="/signup" variant="secondary" style="margin-left: 10px; width: 48%;">Sign up</b-button>
                </b-form>
        </div>
    </b-card>
    </b-row>
    </b-container>
</div>
</template>

<script>
export default {
  name: 'Login'
}
</script>

<style>
  body, html {
    height: 100%;
  }
  .bg {
    /* The image used */
    background-image: url("https://assets.pokemon.com//assets/cms2/img/misc/virtual-backgrounds/sword-shield/pokemon-in-the-wild.png");

    /* Full height */
    height: 100%;

    /* Center and scale the image nicely */
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
  }
</style>

<script>
  import axios from "axios";
  export default {
    data() {
      return {
          form: {
            username: '',
            password: ''
          },
          error: ''
      }
    },
    methods: {
      onSubmit(event) {
        this.error = ''
        event.preventDefault()
        const params = {
          username: this.form.username,
          password: this.form.password
        };
        var path = 'http://127.0.0.1:5000/login';
        console.log(params);
        axios.post(path, params)
          .then((res) => {
            if (res.data.status == "failure") {
                this.error = res.data.error;
                this.form.username = '';
                this.form.password = '';
            } else {
                this.$store.commit('login', this.form.username)
                console.log(this.$store.username)
                this.$router.push({name: "Pokedex"})
            }
          })
          .catch((error) => {
            // eslint-disable-next-line
            this.error = "Problems contacting the server, please try again later!";
          });
      }, 
      onReset(event) {
        event.preventDefault()
        // Reset our form values
        this.form.username = ''
        this.form.password = ''
      }
    }
  }
</script>