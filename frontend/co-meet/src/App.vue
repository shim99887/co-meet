<template>
  <v-app>
    <v-main>
      <right-nav style="z-index:1;"/>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import RightNav from "@/components/RightNav.vue";

export default {
  name: 'App',

  components: {
    RightNav,
  },

  data: () => ({
    //
  }),
};
</script>

<style>

</style>