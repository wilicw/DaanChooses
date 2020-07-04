<template>
  <studentTable :data="data" :file_url="url"></studentTable>
</template>

<script>
import api from '../../api'
import conf from '../../project-config'
import studentTable from '../StudentTable'
export default {
  name: 'NotChoose',
  components: {
    studentTable
  },
  data: () => ({
    data: [],
    url: null
  }),
  async beforeMount () {
    const self = this
    self.url = conf.apiPath + '/file/notchooses/' + window.localStorage.getItem('token')
    self.data = (await api.getNotChoose(window.localStorage.getItem('token'))).data
  }
}
</script>
