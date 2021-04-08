<template>
  <v-container fluid>
    <Navbar class="navbar1" @msg="getMsg"/>
    <video autoplay muted loop id="myVideo">
      <source src="../assets/sub2.mp4" type="video/mp4" />
    </video>
    <v-row no-gutters style="margin-top:60px">
      <v-col cols="5" class="ml-10">
        <div>
          <div v-if="wid > 1000" class="titles">
            <p>CO-MEET</p>
            <div v-if="wid > 1000" class="subtitles">
              <p id=comment style="text-align: left"><b>코</b>로나 피해 다시 일상으로</p>
              <p id=comment style="text-align: right"><b>밋</b>밋했던 하루를 활기차게</p>
            </div>
          </div>
          <div v-else class="mob_titles" style="">
            <p>CO-MEET</p>
          </div>
        </div>
      </v-col>
      <v-col v-if="wid > 1000" cols="4">
        <transition name="fade">
          <user-form v-if="login" :msg="'login'" class="form" />
          <user-form v-if="regist" :msg="'regist'" class="form" />
        </transition>
      </v-col>
    </v-row>
    <v-row style="margin-top:300px;margin-left: 50px;" v-if="wid <= 1000">
    <transition name="fade">
      <user-form v-if="login"/>
    </transition>
    </v-row>
  </v-container>
</template>
<script>
import UserForm from "../components/UserForm.vue";
import Navbar from "../components/navbar.vue";

export default {
  components: {
    UserForm,
    Navbar,
  },
  data() {
    return {
      wid: window.innerWidth,
      login: false,
      regist: false,
    };
  },
  created() {
    window.addEventListener("resize", this.resizeEventHandler);
  },
  destroyed() {
    window.removeEventListener("resize", this.resizeEventHandler);
  },
  methods: {
    resizeEventHandler(event) {
      this.wid = event.target.innerWidth;
    },
    getMsg(msg){
      if(msg == 'login'){
        this.login= !this.login;
        this.regist=false;
      }else{
        this.regist = !this.regist;
        this.login = false;
      }
    }
  },
};
</script>
<style scoped>
body {
  margin: 0px;
}

.fade-enter-active{
  /* transition: opacity .1s; */
  animation: anim3 forwards 2s;
}
 .fade-leave-active {
   animation: anim5 forwards 2s;
 }
@keyframes anim5{
  from{
    bottom:3%;
  }
  to{
    bottom:-100%;
  }
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
.form {
  position: absolute;
  z-index: 1;
  /* margin-top: 250px; */
  bottom:3%;
  left: 60%;
}
.titles {
  position: absolute;
  font-size: 8rem;
  /* color: #22223b;
  opacity: 0.75;
  text-shadow: 4px 4px 4px gray; */
  color : #f8cccc;
  text-shadow: 4px 4px 4px rgb(214, 107, 107);
  z-index: 1;
  font-family: "Bahnschrift Condensed";
  margin-left: 6vw;
  margin-top: 50%;
  bottom: -100%;
  animation: anim 2s forwards 0s;
}
.mob_titles {
  animation: anim2 2s forwards 0s;
  bottom: -100%;
  position: absolute;
  width : 300px;
  font-size: 5rem;
  margin-top: 50%;
  margin-left: 0.7em;
  color : #f8cccc;
  text-shadow: 4px 4px 4px rgb(214, 107, 107);
  z-index: 1;
  font-family: "Bahnschrift Condensed";
}
.subtitles {
  position: relative;
  font-size: 1.5rem;
  margin-left: 0.6em;
  color: #8e0038;
  opacity : 0.9;
  text-shadow: 4px 4px 4px rgb(214, 107, 107);
  z-index: 1;
  font-family: "Bahnschrift Condensed";
  animation: anim 2s forwards 0s;
}
@keyframes anim {
  from {
    bottom: -100%;
  }
  to {
    bottom: 30%;
  }
}
@keyframes anim2 {
  from {
    bottom: -100%;
  }
  to {
    bottom:60%;
  }
}
@keyframes anim3 {
  from {
    bottom: -100%;
  }
  to {
    bottom: 3%;
  }
}
#myVideo {
  object-fit: cover;
  width: 100%;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
}
#comment {
  text-shadow: #352824;
}
</style>
