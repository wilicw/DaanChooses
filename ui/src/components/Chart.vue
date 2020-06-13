<script>
  //Importing Bar class from the vue-chartjs wrapper
  import { Bar, mixins } from 'vue-chartjs'
  const { reactiveProp } = mixins
  //Exporting this so it can be used in other components
  export default {
    extends: Bar,
    props: ['options'],
    mixins: [reactiveProp],
    data () {
      return {

      }
    },
    watch: {
      chartData () {
        this.$data._chart.update()
      }
    },
    mounted () {
      //renderChart function renders the chart with the datacollection and options object.
      this.renderChart(this.chartData, this.options)
    }
  }
</script>
