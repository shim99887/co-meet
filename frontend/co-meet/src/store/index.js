import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios"

Vue.use(Vuex)

const SERVER_URL = process.env.VUE_APP_SERVER_URL;

export default new Vuex.Store({
  state: {
    searchingCity: "",
    onSearching: false,
    // 이전 달 구별 코로나
    gugun: [],
    gugunData: [],
    // 장소들 추천 리스트
    recomCity: [],
    recomCityMonth: [],
    recomCityPatients: [],
    coordinates: [],
    targets: [],
    // 상태 정의들
    mapToggle: false,
    reRecom : false,
    // 로그인 상태 관리
    accessToken: localStorage.getItem('accessToken'),
    userEmail: localStorage.getItem('email'),
    userName: localStorage.getItem('nickname'),
    searchLog:[],
    // 요청 데이터 폼
    targetCities: {
      email: '',
      searchList: [],
    },
    nextCoord: [],
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
    // 결과 관련
    get_result(state) {
      return state.recomCity
    },
    get_month(state) {
      return state.recomCityMonth
    },
    get_patients(state) {
      return state.recomCityPatients
    },
    get_coordinates(state) {
      return state.coordinates
    },
    get_targets(state) {
      let searchResult = []
      state.targets.forEach((item) => {
        if (item in searchResult) {
          return
        } else {
          searchResult.push(item)
        }
      })
      return searchResult
    },
    //
    get_mapToggle(state) {
      return state.mapToggle
    },
    get_reRecom(state){
      return state.reRecom;
    },
    get_resultCity(state) {
      return state.recomCity
    },
    get_onSearching(state) {
      return state.onSearching
    },
    getSearchLog(state){
      return state.searchLog;
    },
    get_FlyTo(state) {
      return state.nextCoord
    },
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
    MAPCANCLE(state) {
      state.mapToggle = false
      state.targetCities.searchList = []
      state.recomCity = []
      state.recomCityMonth = []
      state.recomCityPatients = []
      state.coordinates = []
      state.targets = []
      state.gugun= []
      state.gugunData= []
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
    ON_RERECOM(state){
      state.reRecom = true;
    },
    OFF_RERECOM(state){
      state.reRecom = false;
    },
    GET_SEARCH_LOG(state, log){
      state.searchLog.push(log);
    },
    DELETE_SEARCH_LOG(state){
      state.searchLog = [];
    },
    PUT_TARGETCITIES(state, data){
      state.targetCities.searchList.push(data)
    },
    FLYTO(state, idx) {
      state.nextCoord = this.state.coordinates[idx]
    }
  },
  actions: {
    async GET_RECOM(context) {
      try {
        if (this.state.userEmail) {
          this.state.targetCities.email = this.state.userEmail
        } else {
          this.state.targetCities.email = 123
        }
        const res = await axios.post("https://j4a203.p.ssafy.io/recomm/recommend", this.state.targetCities)
        const data = res.data
        for (let idx = 0; idx < 4; idx++) {
          this.state.recomCityMonth.push(data[idx].date)
          this.state.recomCityPatients.push(data[idx].patients)
          this.state.coordinates.push([Number(data.lng[idx]), Number(data.lat[idx])])
          this.state.recomCity.push(data.signgu_nm[idx])
        }
        data.target.forEach((item) => {
          this.state.targets.push(item)
        })
        context.commit("OFF_SEARCHING")
      } catch(err) {
        context.commit("OFF_SEARCHING")
      }
      context.commit("MAPTOGGLE")
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
        context.commit("OFF_SEARCHING")
        
      } catch (err) {
        console.log(err)
        context.commit("OFF_SEARCHING")
      }
    },
    LOGIN(context, user){
      context.commit("ON_SEARCHING")
      const params = new URLSearchParams();
      params.append('email', user.email);
      params.append('password', user.password);

      axios.post(`${SERVER_URL}/user/login`, params)
      .then(response => {
        localStorage.setItem('accessToken', response.data.token);
        localStorage.setItem('nickname', response.data.nickname);
        localStorage.setItem('email', response.data.email);
        context.commit('LOGIN');
        context.commit("OFF_SEARCHING")
      })
      .catch(() => {
        context.commit("OFF_SEARCHING")
      })     
    },
    LOGOUT(context, email){
      axios.get(`${SERVER_URL}/user/logout/` + email)
      .then(() => {
      })
      .catch(error => {
        context.commit("OFF_SEARCHING")
        alert(error);
      })

      context.commit('LOGOUT');
      location.href = "/";
    },
    GET_SEARCH_LOG(context, log){
      context.commit('GET_SEARCH_LOG', log);
    }
  }
})
