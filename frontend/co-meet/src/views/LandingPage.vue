<template>
  <v-container fluid>
    <video autoplay muted loop id="myVideo">
      <source src="../assets/sub2.mp4" type="video/mp4" />
    </video>
    <div style="position:absolute;z-index:1">{{wid}}</div>
    <v-row no-gutters style="margin-top:150px">
      <v-col cols="5" class="ml-10">
        <div>
          <div style="position:absolute;font-size:100px; z-index:1; margin-top:100px;">
            <p>CO-MEET</p>
          </div>
        </div>
      </v-col>
      <v-col v-if="wid>1000" cols="4">
        <user-form style="position:absolute;z-index:1;" class="form" />
      </v-col>
    </v-row>
    <v-row style="margin-top:300px" v-if="wid<=1000">
      <user-form/>
    </v-row>
    <v-btn @click="temp">asd</v-btn>
  </v-container>
</template>
<script>
import UserForm from "../components/UserForm.vue";
import $ from 'jquery';

export default {
  components: {
    UserForm,
  },
  data(){
    return{
      wid:0,
    };
  },
  methods:{
    temp(){
      console.log(this.wid);

    }
  },
  mounted() {
    $(window).resize(function(event){
      this.wid = event.target.innerWidth;
    })
  },
};
</script>
<style scoped>
body {
  margin: 0px;
}

#myVideo {
  object-fit: cover;
  width: 100%;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
}

</style>
