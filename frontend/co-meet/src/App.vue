<template>
  <v-app>
    <v-main>
      <right-nav style="z-index:1;"/>
      <div class="text-center">
    <v-dialog
      v-model="loading"
      width="200"
    >
      <v-card>
        <Loading />
      </v-card>
    </v-dialog>
  </div>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import RightNav from "@/components/RightNav.vue";
import Loading from "@/components/loading/LoadingModal.vue"

export default {
  name: 'App',

  components: {
    RightNav,
    Loading,
  },
  data: () => ({
    
  }),
  computed:{
    loading() {
      return this.$store.getters.get_onSearching
    },
  },
};


</script>

<style scoped>

</style>