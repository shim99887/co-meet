<template>
  <v-app>
    <v-main>
      <landing-page/>
    </v-main>
  </v-app>
</template>

<script>
import LandingPage from './views/LandingPage.vue';

export default {
  name: 'App',

  components: {
    LandingPage,
  },

  data: () => ({
    //
  }),
};
</script>
