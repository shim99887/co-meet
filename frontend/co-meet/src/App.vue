<template>
  <v-app>
    <v-main>
      <Navbar />
      <landing-page/>
    </v-main>
  </v-app>
</template>

<script>
import LandingPage from './views/LandingPage.vue';
import Navbar from "@/components/navbar.vue"

export default {
  name: 'App',

  components: {
    LandingPage,
    Navbar,
  },

  data: () => ({
    //
  }),
};
</script>
