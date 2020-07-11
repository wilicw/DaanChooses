<template>
  <v-card flat style="width: 100%">
    <v-card-title class="justify-center">
      <p>系統設定</p>
    </v-card-title>
    <v-row class="pa-3 justify-center">
      <v-col xs="12" md="8">
        <v-form
          ref="form"
          v-model="form"
        >
          <v-text-field
            v-model="setting.title"
            label="標題"
            required
          ></v-text-field>
          <v-text-field
            v-model="setting.maxChoose"
            label="志願數"
            required
          ></v-text-field>
          <v-text-field
            v-model="setting.year"
            label="學期"
            required
          ></v-text-field>
          <v-text-field
            v-model="setting.closeDate"
            label="關閉日期"
            required
          ></v-text-field>
          <v-textarea
            label="公告文字"
            v-model="setting.systemAnnouncement"
          ></v-textarea>
        </v-form>
         <v-btn
          color="primary"
          class="mr-4"
          @click="saveSetting"
        >
          儲存
        </v-btn>
      </v-col>
    </v-row>
    <v-snackbar
      v-model="status.show"
      :color="status.type"
    >
      {{ status.msg }}
    </v-snackbar>
  </v-card>
</template>

<script>
import api from '../api'
export default {
  name: 'setting',
  data () {
    return {
      form: true,
      setting: {
        title: '',
        maxChoose: 0,
        systemAnnouncement: '',
        closeDate: '',
        year: 0
      },
      status: {
        msg: '',
        type: '',
        show: false
      }
    }
  },
  async beforeMount () {
    const self = this
    const systemInfo = (await api.getSystemInfo()).data
    self.setting = systemInfo
  },
  methods: {
    saveSetting: async function () {
      const self = this
      const response = (await api.saveSetting(window.localStorage.getItem('token'), self.setting)).data
      if (response.status === 401) {
        window.localStorage.removeItem('token')
        this.$router.replace('/')
      } else {
        self.showMsg('success', '儲存成功')
      }
    },
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
