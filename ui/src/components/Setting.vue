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
          <v-text-field
            v-model="setting.doc"
            label="課程總覽網址"
            required
          ></v-text-field>
          <div class="mb-3">
            <p class="data">公告文字</p>
            <ckeditor
              :editor="editor"
              v-model="setting.systemAnnouncement"
              :config="editorConfig"
            ></ckeditor>
          </div>
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
import _ from 'lodash'
import CKEditor from '@ckeditor/ckeditor5-vue'
import ClassicEditor from '@ckeditor/ckeditor5-build-classic'

export default {
  name: 'setting',
  components: {
    ckeditor: CKEditor.component
  },
  data () {
    return {
      form: true,
      setting: {},
      status: {
        msg: '',
        type: '',
        show: false
      },
      editor: ClassicEditor,
      editorConfig: {
        language: 'zh'
      }
    }
  },
  async beforeMount () {
    const self = this
    const managerInfo = (await api.getManageStatus(window.localStorage.getItem('token'))).data
    if (managerInfo.status !== 200) {
      window.localStorage.removeItem('token')
      this.$router.replace('/')
    }
    const systemInfo = (await api.getSystemInfo()).data
    self.setting = _.findLast(systemInfo.data, ['_id', managerInfo.permission])
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
