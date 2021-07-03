import Vue from 'vue'
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';

const state = {
    username: null
};
  
const mutations = {
    logout(state) {
      state.username = null;
    },
    login(state, username) {
      state.username = username;
    }
};
  
Vue.use(Vuex)
export default new Vuex.Store({
    state,
    plugins: [createPersistedState()],
    mutations
});