<template>
  <div>
    <v-btn
      color="pink"
      style="position:fixed;right:5px; top:50%;"
      dark
      rounded
      @click.stop="drawer = !drawer"
    >
      최근목록
    </v-btn>
    <v-navigation-drawer
      width="500px"
      style="background:#fadde1;"
      v-model="drawer"
      absolute
      temporary
      right
    >
      <v-list-item class="mt-10">
        <v-list-item-content>
          <v-list-item-title style="font-size:40px;">{{$store.getters.getUserName}}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>
      <v-subheader>최근 검색 목록</v-subheader>
      <v-list-item>
        <br />
        <v-list-item-content>
          <v-list-item-title v-for="(item, index) in logs" :key="index">

            <v-btn class="listitem" block tile outlined color="primary">{{item}}</v-btn>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-img @click="drawerMove" style="position:fixed;right:0px;top:50%;pointer:cursor;" src="../assets/X_icon.png"/>
      <!-- <button @click="drawerMove" styl e="font-family:verdana;font-size:35px;position:fixed;right:0px;top:50%;background:#fadde1;">x</button> -->
    </v-navigation-drawer>
  </div>
</template>
<script>
import axios from 'axios';

const SERVER_URL = process.env.VUE_APP_SERVER_URL;

export default {
  data() {
    return {
      drawer: null,
      items: ["서울 강남구 압구정동 386-1", "서울 노원구 월계동 472-31", "서울 강남구 신사동 537-5"],
      logs:[],
    };
  },
  mounted(){
        axios.get(`${SERVER_URL}/user/searchlog/` + this.$store.getters.getUserEmail,{
      headers:{
        'Content-Type' : 'application/json',
         'Access-Control-Allow-Origin': '*'
      }
    })
    .then(response => {
      this.$store.commit('DELETE_SEARCH_LOG');
      for(var key in response.data['searchList']){
          this.$store.commit('GET_SEARCH_LOG', response.data['searchList'][key]);
      }
    })
    .catch(error => {
      alert(error);
    })
    this.items = this.$store.getters.getSearchLog;
      console.log(this.items);
    for(var item in this.items){
    //   // console.log(this.items[item]);
      var string = '';
      for(var value in this.items[item]){
        string += this.items[item][value].juso + " / ";
      }
      // if()
      string = string.substring(0, string.length-2);
      this.logs.push(string);
    }
    
  },
  methods:{
    drawerMove(){
      this.drawer = false;
    }
  }
  
};
</script>
<style scoped>
.listitem:hover {
  background: #89b9e8;
}
</style>
