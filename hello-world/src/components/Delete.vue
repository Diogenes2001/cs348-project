<template>
<div class="bg">
  <myHeader />
    <b-container class="h-100">
    <b-row align-h="center" style="padding-top: 60px;">
    <b-card style="width: 400px;" header="Delete account" border-variant="dark" header-class="h1 text-center" header-bg-variant="white">
        <div>
            <b-form @submit="onSubmit" @reset="onReset">
                <b-form-group id="input-group-3" label="Password" label-for="input-3">
                    <b-form-input type="password" v-model="form.password" id="input-3" placeholder="Enter password" required></b-form-input>
                </b-form-group>

                <div style="color: red; padding-bottom: 5px;" v-show="this.msg == ''">Warning: If you delete your account, you will lose all your custom pokemon!</div>

                <div style="color: red; padding-bottom: 5px;" v-show="this.error">{{ this.error }}</div>
                <div style="color: green; padding-bottom: 5px;" v-show="this.msg">{{ this.msg }}</div>

                <b-button type="submit" variant="primary" class="w-100">Submit</b-button>
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
  import { mapState } from 'vuex'
  export default {
    computed: mapState({
      username: state => state.username
    }),
    data() {
      return {
          form: {
            password: ''
          },
          error: '',
          msg: ''
      }
    },
    methods: {
      onSubmit(event) {
        this.error = ''
        this.msg = ''
        event.preventDefault()
        const params = {
          username: this.username,
          password: this.form.password
        };
        var path = 'http://127.0.0.1:5000/deleteaccount';
        axios.post(path, params)
          .then((res) => {
            if (res.data.status == "failure") {
                this.error = res.data.error;
            } else {
                this.$store.commit('logout')
                this.msg = res.data.error;
            }
          })
          .catch((error) => {
            // eslint-disable-next-line
            this.error = "Problems contacting the server, please try again later!";
          });
          this.form.password = '';
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