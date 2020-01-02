<template>
<v-card flat>
  <v-card-title>
    <v-select
      v-model="value"
      :items="classList"
      attach
      chips
      label="選擇分析課程"
      multiple
    ></v-select>
    <v-spacer></v-spacer>
    <v-btn color="primary" dark @click="analysis">
      分析
    </v-btn>
  </v-card-title>
  <Chart v-if="chartData.datasets.length!=0" :chart-data="chartData" :options="options" style="width: 100%;"></Chart>
</v-card>
</template>

<script>
import api from '../../api'
import Chart from '../Chart'

export default {
  name: 'ClassAnalysis',
  components: {
    Chart
  },
  data() {
    return {
      value: [],
      classList: [],
      stepData: [],
      chartData: {
        labels: ['第一志願', '第二志願', '第三志願', '第四志願', '第五志願', '第六志願', '第七志願', '第八志願', '第九志願', '第十志願', '第十一志願', '第十二志願', '第十三志願', '第十四志願', '第十五志願'],
        datasets: []
      },
      options: {
        responsive: true,
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Result'
        },
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        }
      }
    }
  },
  beforeMount() {
    let self = this
    let step = []
    let clubsNumber = 0
    let choosesMax = 0
    api.getSystemInfo().then(dt => {
      choosesMax = dt.data.maxChoose
    }).then(() => {
      api.getClubs().then(dt => {
        clubsNumber = dt.data.length
        for (let i = 0; i < clubsNumber; i++) {
          step.push([])
          for (let j = 0; j < choosesMax; j++) {
            step[i].push(0)
          }
        }
      }).then(() => {
        api.getManageChoose(window.localStorage.getItem('token')).then(dt => {
          console.log(dt)
          dt.data.forEach(j => {
            step[j.club][j.step-1]++
          })
          self.stepData.push(step)
        })
      })
    })
  },
  methods: {
    analysis: function () {
      console.log(this.stepData)
      let self = this
      self.chartData.datasets = []
      self.value.forEach(i => {
        let step = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        let id = self.classList.indexOf(i)+1
        let color = [
          (Math.floor(Math.random() * Math.floor(255))),
          (Math.floor(Math.random() * Math.floor(255))),
          (Math.floor(Math.random() * Math.floor(255)))
        ]
        return {
          backgroundColor: `rgb(${color[0]}, ${color[1]}, ${color[2]}, 0.6)`,
          maxBarThickness: 30,
          label: self.classList[id-1],
          data: self.stepData[id-1]
        }
      })
    }
  }
}
</script>
