<template>
  <v-container>
    <v-row
      class="justify-center"
    >
      <v-col
        md="4"
        xs="12"
      >
        <v-card
          class="text-center elevation-8 pa-5"
        >
          <v-card-title>登入</v-card-title>
          <v-card-text>
            <v-form>
              <v-text-field
                v-model="id"
                label="帳號（學號）"
                required
              ></v-text-field>
              <v-text-field
                v-model="password"
                label="密碼（身份證字號後四碼）"
                type="password"
                required
              ></v-text-field>
              <v-btn class="mr-4" @click="submit" color="primary">登入</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-snackbar
      v-model="status.show"
      :color="status.type"
    >
      {{ status.msg }}
    </v-snackbar>
  </v-container>
</template>

<script>
import api from '../api'
export default {
  data: () => ({
    password: '',
    status: {
      type: '',
      msg: '',
      show: false
    }
  }),
  methods: {
    async submit () {
      const self = this
      const normalResponse = (await api.login(self.id, self.password)).data
      if (normalResponse.status === 200) {
        window.localStorage.setItem('token', normalResponse.token)
        self.$router.replace('/choose')
        return
      }
      const manageResponse = (await api.ManageLogin(self.id, self.password)).data
      if (manageResponse.status === 200) {
        window.localStorage.setItem('token', manageResponse.token)
        self.$router.replace('/control')
        return
      }
      self.status = {
        type: 'red',
        msg: '帳號或密碼錯誤，若無法登入請至教務處或學務處反應',
        show: true
      }
    }
  }
}
</script>
