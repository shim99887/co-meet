<template>
  <div class="reccom">
    <Address />
    <Graph />
    <Reason />
  </div>
</template>

<script>
import Graph from "../components/Graph.vue"
import Address from "../components/Address.vue"
import Reason from "../components/Reason.vue"

export default {
  components: {
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