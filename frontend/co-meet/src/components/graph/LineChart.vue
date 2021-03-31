
<script>
import { Line } from 'vue-chartjs'

export default {
  extends: Line,
  computed: {
    recomCity() {
      return this.$store.getters.get_resultCity
    },
  },
   mounted () {
    this.renderChart({
      labels: this.recomCity[0].date,
      datasets: [
        {
          label: `${this.recomCity[0].gu}의 확진자 수`,
          backgroundColor: '#ffb6c1',
          data: this.recomCity[0].patients
        }
      ]
    }, {
      responsive: true, 
      maintainAspectRatio: false,
      scales: {
        yAxes: [{
          ticks: {
            min: 0,
            stepSize: 10,
            max: 90,
          }
        }]
      },
      })

  },
}
</script>

<style>

</style>