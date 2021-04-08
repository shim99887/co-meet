<template>
  <div>
    <v-btn
      color="pink"
      style="position:fixed;right:5px; top:50%;"
      dark
      rounded
      @click.stop="drawer = !drawer"
      @click="drawerClick"
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
          <v-list-item-title style="font-size:40px;">{{
            $store.getters.getUserName
          }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>
      <v-subheader>최근 검색 목록</v-subheader>
      <v-list-item>
        <br />
        <v-list-item-content>
          <v-list-item-title v-for="(item, index) in logs" :key="index">
            <v-btn width="100%" class="listitem" @click="recentLogClick($event)" block tile outlined color="primary" style="text-align:left;">{{
              item
            }}</v-btn>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-img
        @click="drawerMove"
        width="30px"
        style="position:fixed;right:10px;top:50%;cursor:pointer;"
        src="../assets/X_icon.png"
      />
    </v-navigation-drawer>
  </div>
</template>
<script>
import axios from "axios";

const SERVER_URL = process.env.VUE_APP_SERVER_URL;

export default {
  data() {
    return {
      drawer: null,
      items: [],
      logs: [],
    };
  },
  computed:{
    addrList:function(){
      return this.$store.getters.addrLists;
    }
  },
  methods: {
    drawerMove() {
      this.drawer = false;
    },
    drawerClick() {
      this.logs = [];
      this.items = [];
      var self = this;
      axios
        .get(
          `${SERVER_URL}/user/searchlog/` + this.$store.getters.getUserEmail,
          {
            headers: {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "*",
            },
          }
        )
        .then((response) => {
          this.$store.commit("DELETE_SEARCH_LOG");
          for (var key in response.data["searchList"]) {
              self.items.push(response.data["searchList"][key]);
          }
              self.items.forEach(item => {
                var string = "";
                item.forEach(data => {
                  string += data.juso + " / ";
                })
                string = string.substring(0,string.length-2);
                this.logs.push(string);
              })
          this.logs = this.logs.reverse();
        })
        .catch((error) => {
          alert(error);
        });
        
    },
    recentLogClick(event){
      this.$store.commit('MAPCANCLE');
      this.$store.commit('SET_ADDRLIST', event.target.innerText.split(' / '));
      this.drawer = false;
    }
  },
};
</script>
<style scoped>
.listitem:hover {
  background: #89b9e8;
}
</style>
