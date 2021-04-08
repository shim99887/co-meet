<template>
  <v-app>
    <v-main>
      
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
import Loading from "@/components/loading/LoadingModal.vue"

export default {
  name: 'App',

  components: {
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