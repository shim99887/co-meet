<template>
  <div class="reccom">
    <Navbar class="navbar"/>
    <Address />
    <Graph/>
    <Explain />
  </div>
</template>

<script>
import Graph from "../components/Graph.vue"
import Address from "../components/Address.vue"
import Explain from "../components/Explain.vue"
import Navbar from "../components/navbar.vue"

export default {
  components: {
    Navbar,
    Address,
    Graph,
    Explain,
  },
}
</script>

<style lang="scss">
  .reccom {
    width: 80vw;
    margin: 0 auto 0 auto;
    .navbar {
      margin-top: 5vh;
    }
  }
  @media screen and (max-width: 48rem) {
    .reccom {
    width: 93vw;
    margin: 0 auto 0 auto;
  }
  }
</style>