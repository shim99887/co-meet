import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import VueSimpleAlert from "vue-simple-alert";
 
Vue.use(VueSimpleAlert);
Vue.use(Vuex)

const SERVER_URL = process.env.VUE_APP_SERVER_URL;

export default new Vuex.Store({
  state: {
    accessToken: localStorage.getItem('accessToken'),
    userEmail: localStorage.getItem('email'),
    userName: localStorage.getItem('nickname'),
  },
  getters:{
    getAccessToken(state){
      return state.accessToken;
    },
    getUserEmail(state){
      return state.userEmail;
    },
    getUserName(state){
      return state.userName;
    }
  },
  mutations: {
    LOGIN(state){
      state.accessToken = localStorage.getItem('accessToken');
      state.nickname = localStorage.getItem('nickname');
      state.email = localStorage.getItem('email');
    },
    LOGOUT(state){
      state.accessToken = null;
      state.userEmail = '';
      state.userName = '';
      localStorage.removeItem('accessToken');
      localStorage.removeItem('nickname');
      localStorage.removeItem('email');
    }
  },
  actions: {
    LOGIN(context, user){
      const params = new URLSearchParams();
      params.append('email', user.email);
      params.append('password', user.password);

      axios.post(`${SERVER_URL}/user/login`, params)
      .then(response => {
        localStorage.setItem('accessToken', response.data.token);
        localStorage.setItem('nickname', response.data.nickname);
        localStorage.setItem('email', response.data.email);
        context.commit('LOGIN');
      })
      .catch(() => {
      })     
    },
    LOGOUT(context, email){
      axios.get(`${SERVER_URL}/user/logout/` + email)
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        alert(error);
      })

      context.commit('LOGOUT');
      // location.href = "/";
    }
  },
  modules: {
  }
})
