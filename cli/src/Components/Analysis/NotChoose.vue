<template>
  <v-card flat>
    <v-card-title>
      <v-spacer></v-spacer>
      <v-btn color="primary"><v-icon left>mdi-download</v-icon> 匯出資料</v-btn>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="data"
    ></v-data-table>
  </v-card>
</template>

<script>
import api from '../../api'
export default {
  name: 'NotChoose',
  data () {
    return {
      search: '',
      headers: [
        {
          text: '學號',
          align: 'left',
          value: 'id',
        },
        { text: '班級', value: 'class' },
        { text: '姓名', value: 'name' }
      ],
      data: []
    }
  },
  beforeMount() {
    let self = this
    api.getNotChoose(window.localStorage.getItem('token')).then(res => {
      self.data = res.data
    })
  }
}
</script>
