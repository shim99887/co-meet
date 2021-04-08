
<script>
import { Line } from 'vue-chartjs'

export default {
  extends: Line,
  computed: {
    cities() {
      return this.$store.getters.get_result;
    },
    citiesDate() {
      return this.$store.getters.get_month;
    },
    citiesPatients() {
      return this.$store.getters.get_patients
    },
    citiesCoordinates() {
      return this.$store.getters.get_coordinates
    },
    targets() {
      return this.$store.getters.get_targets
    },
  },
   mounted () {
    this.renderChart({
      labels: this.citiesDate[0],
      datasets: [
        {
          label: `${this.cities[0]}의 확진자 수`,
          backgroundColor: 'rgba(0, 0, 0, 0.0)',
          borderColor: '#FF6384',
          data: this.citiesPatients[0],
        },
        {
          label: `${this.cities[1]}의 확진자 수`,
          backgroundColor: 'rgba(0, 0, 0, 0.0)',
          borderColor: '#36a2eb',
          data: this.citiesPatients[1],
        },
        {
          label: `${this.cities[2]}의 확진자 수`,
          backgroundColor: 'rgba(0, 0, 0, 0.0)',
          borderColor: '#4bc0c0',
          data: this.citiesPatients[2],
        },
        {
          label: `${this.cities[3]}의 확진자 수`,
          backgroundColor: 'rgba(0, 0, 0, 0.0)',
          borderColor: '#ffcd56',
          data: this.citiesPatients[3],
        },
      ]
    }, {
      responsive: true, 
      maintainAspectRatio: false,
    })

  },
}
</script>

<style>

</style>
