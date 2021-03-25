import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios"

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    searchingCity: "",
    onSearching: false,
    gugun: [],
    gugunData: [],
    recomCity: [],
    mapToggle: false,
  },
  getters:{
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
  },
})
