<template>
  <div class="reccom">
    <Navbar />
    <Address />
    <Graph />
    <Reason />
  </div>
</template>

<script>
import Graph from "../components/Graph.vue"
import Address from "../components/Address.vue"
import Reason from "../components/Reason.vue"
import Navbar from "../components/navbar.vue"

export default {
  components: {
    Navbar,
    Address,
    Graph,
    Reason,
  },

}
</script>

<style>
  .reccom {
    width: 94vw;
    margin: 10% auto 0 auto;
  }
</style>