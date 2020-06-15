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
  data () {
    return {
      search: '',
      url: '',
      headers: [
        {
          text: '學號',
          align: 'left',
          value: 'id'
        },
        { text: '班級', value: 'class' },
        { text: '姓名', value: 'name' }
      ],
      data: []
    }
  },
  async beforeMount () {
    const self = this
    self.url = conf.apiPath + '/file/notchooses'
    self.data = (await api.getNotChoose(window.localStorage.getItem('token'))).data
  }
}
</script>
