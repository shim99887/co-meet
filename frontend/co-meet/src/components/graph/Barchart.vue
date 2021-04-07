
<script>
import { Bar } from 'vue-chartjs'

export default {
  extends: Bar,
  computed: {
    gugun() {
      return this.$store.getters.get_gugun
    },
    gugunData() {
      return this.$store.getters.get_gugunData
    },
  },
  mounted () {
    this.renderChart({
      labels: this.gugun,
      datasets: [
        {
          label: '구별 확진자 발생 수',
          backgroundColor: '#ffb6c1',
          data: this.gugunData
        }
      ]
    }, {responsive: true, maintainAspectRatio: false})

  },
  

}
</script>

<style>

</style>