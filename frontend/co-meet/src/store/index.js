import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    accessToken: null,
    userEmail: '',
  },
  getters:{
    getAccessToken(state){
      return state.accessToken;
    },
    getUserEmail(state){
      return state.userEmail;
    }
  },
  mutations: {
    LOGIN(state, payload){
      state.accessToken = payload['auth-token'];
      state.userEmail = payload['user-email'];
    },
    LOGOUT(state){
      state.accessToken = null;
      state.userEmail = '';
    }
  },
  actions: {
    LOGIN(context, user){
      const params = new URLSearchParams();
      params.append('email', user.email);
      params.append('pwd', user.pwd);
    },
    LOGOUT(context){
      context.commit('LOGOUT');
      location.href = "/";
    }
  },
  modules: {
  }
})
