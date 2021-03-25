import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios"

Vue.use(Vuex)

const SERVER_URL = process.env.VUE_APP_SERVER_URL;

export default new Vuex.Store({
  state: {
    searchingCity: "",
    onSearching: false,
    gugun: [],
    gugunData: [],
    recomCity: [],
    mapToggle: false,
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
    },
    get_gugun(state) {
      return state.gugun
    },
    get_gugunData(state) {
      return state.gugunData
    },
    get_city(state) {
      return state.searchingCity
    },
    get_result(state) {
      return state.recomCity
    },
    get_mapToggle(state) {
      return state.mapToggle
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
    },
    MAPTOGGLE(state) {
      state.mapToggle = !state.mapToggle
    },
    ON_SEARCHING(state) {
      state.onSearching = true
    },
    OFF_SEARCHING(state) {
      state.onSearching = false
    },
    PUT_CITY(state, city) {
      state.searchingCity = city
    },
    PUT_RESULT(state, location) {
      state.recomCity.push(location)
    },
  },
  actions: {
    async GET_RECOM(context, city) {
      try {
        const res = await axios.post("https://j4a203.p.ssafy.io/api/recomm", {signgu_nm: city})
        context.commit('PUT_CITY', city)
        const data = res.data
        const location = {
          lat: data.recomm_lat,
          lng: data.recomm_lng,
          gu: data.signgu_nm,
        }
        context.commit("PUT_RESULT", location)
        context.commit("MAPTOGGLE")
      } catch(err) {
        console.log(err)
      }
    },
    async GET_CORONA_PER_CITY(context) {
      try {
        const res = await axios.get("https://j4a203.p.ssafy.io/api/corona-list")
        const data = res.data
        for (let key in data.gugun) {
          this.state.gugun.push(data.gugun[key])
        }
        for (let key in data.serial_number) {
          this.state.gugunData.push(data.serial_number[key])
        }
        console.log(this.state.gugun)
        console.log(this.state.gugunData)
        context.commit("OFF_SEARCHING")
        
      } catch (err) {
        console.log(err)
      }
    },
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
    },
})
