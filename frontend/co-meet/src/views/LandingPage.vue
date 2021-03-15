<template>
  <v-container fluid>
  <Navbar />
    <video autoplay muted loop id="myVideo">
      <source src="../assets/sub2.mp4" type="video/mp4" />
    </video>
    <v-row no-gutters style="margin-top:60px">
      <v-col cols="5" class="ml-10">
        <div>
          <div v-if="wid>1000" class="titles">
            <p>CO-MEET</p>
          </div>
          <div v-else style="position:absolute;font-size:80px; z-index:1;">
            <p>CO-MEET</p>
          </div>
        </div>
      </v-col>
      <v-col v-if="wid>1000" cols="4">
        <user-form style="position:absolute;z-index:1; margin-top:250px;left:60%;" class="form" />
      </v-col>
    </v-row>
    <v-row style="margin-top:300px" v-if="wid<=1000">
      <user-form/>
    </v-row>
  </v-container>
</template>
<script>
import UserForm from "../components/UserForm.vue";
import Navbar from "../components/navbar.vue"

export default ({
  components: {
    UserForm,
    Navbar,
  },
  data(){
    return{
      wid:window.innerWidth,
    };
  },
  created(){
    window.addEventListener("resize", this.resizeEventHandler);
  },
  destroyed(){
    window.removeEventListener("resize", this.resizeEventHandler);
  },
  methods:{
    resizeEventHandler(event){
      // console.log(event);
      this.wid = event.target.innerWidth;
    },
  },
});
</script>
<style scoped>
body {
  margin: 0px;
}
.titles{
  position:absolute;
  font-size:10rem;
  color:#22223b;
  opacity:0.75;
  text-shadow: 4px 4px 4px gray;
  z-index:1; 
  font-family: "Bahnschrift Condensed";
  margin-left:50px; 
  margin-top:150px;
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
