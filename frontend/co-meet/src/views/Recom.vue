<template>
  <div class="recom-body">
    <Navbar class="navbar"/>
    <video autoplay muted loop id="myVideo">
        <source src="../assets/sub2.mp4" type="video/mp4" />
    </video>    
    <div class="reccom">
        <right-nav v-if="$store.getters.getAccessToken" style="z-index:998 !important;"/>
        <Address />
        <Graph />
        <!-- <Explain /> -->
    </div>
  </div>
</template>

<script>
import Graph from "../components/Graph.vue"
import Address from "../components/Address.vue"
// import Explain from "../components/Explain.vue"
import Navbar from "../components/navbar.vue"
import RightNav from "../components/RightNav.vue"

export default {
  components: {
    Navbar,
    Address,
    Graph,
    RightNav,
  },
  computed: {
    gugun() {
      return this.$state.getters.get_gugun
    },
  },
   mounted(){

  },
}
</script>

<style lang="scss">
.recom-body{
  // background-color: #F7CAC9;
  .reccom {
    position: absolute; 
    top: 0; 
    left: 9.5%;
    width: 80vw;
    margin: 0 auto 0 auto;
    .navbar {
      margin-top: 5vh;
      z-index: 1;
    }
  }
}
  @media screen and (max-width: 48rem) {
  .reccom {
    width: 96vw;
    margin: 0 auto;
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
</style>
