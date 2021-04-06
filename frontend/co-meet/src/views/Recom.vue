<template>
<div class="recom-body">
  <Navbar class="navbar"/>
  <div class="reccom">
    <right-nav v-if="$store.getters.getAccessToken" style="z-index:1;"/>
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
    // Explain,
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
    width: 93vw;
    margin: 0 auto 0 auto;
  }
  }
</style>