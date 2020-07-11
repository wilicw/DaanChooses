<template>
  <v-card flat>
    <v-card-title class="justify-center">
      <p>學生管理</p>
    </v-card-title>
    <studentTable :data="data" :file_url="url"></studentTable>
  </v-card>
</template>

<script>
import api from '../api'
import conf from '../project-config'
import studentTable from './StudentTable'
export default {
  name: 'students',
  components: {
    studentTable
  },
  data: () => ({
    data: [],
    url: null
  }),
  async beforeMount () {
    const stu = (await api.getStudents(window.localStorage.getItem('token'))).data
    this.url = conf.apiPath + '/file/allstudents/' + window.localStorage.getItem('token')
    this.data = stu
  },
  methods: {
  }
}
</script>
