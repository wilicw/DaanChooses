<template>
  <v-card flat style="width: 100%">
    <v-card-title class="justify-center">
      <p>學生管理</p>
    </v-card-title>
    <v-row class="pa-3 justify-center">
      <v-col xs="12" md="8">
        <v-data-table
          :headers="headers"
          :items="students"
          :search="search"
        ></v-data-table>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import api from '../api'
export default {
  name: 'students',
  components: {},
  data () {
    return {
      headers: [
        {
          text: '學號',
          align: 'left',
          sortable: false,
          value: 'account',
        },
        { text: '姓名', value: 'student_name' },
        { text: '座號', value: 'student_number' }
      ],
      search: "",
      students: [],
      status: {
        msg: '',
        type: '',
        show: false
      }
    }
  },
  beforeMount() {
    let self = this
    
  },
  methods: {
    //self.showMsg('success', `儲存成功`)
    showMsg: function (type, msg) {
      this.status = {
        type: type,
        msg: msg,
        show: true
      }
      this.$vuetify.goTo(0, 'easeInOutCubic')
    }
  }
}
</script>
