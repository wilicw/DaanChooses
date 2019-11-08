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
          class="text-center"
        >
          <v-card-title>學生登入</v-card-title>
          <v-card-text>
            <v-alert v-if="isError" type="error">
              {{errorMsg}}
            </v-alert>
            <form>
              <v-text-field
                v-model="id"
                label="學號"
                required
              ></v-text-field>
              <v-text-field
                v-model="password"
                label="身份證字號後四碼"
                type="password"
                required
              ></v-text-field>
              <v-btn class="mr-4" @click="submit" color="primary">登入</v-btn>
            </form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import api from '../api'
export default {
  data: () => ({
    id: '',
    password: '',
    isError: false,
    errorMsg: ''
  }),
  methods: {
    submit () {
      let self = this
      api.login(self.id, self.password).then(function (res) {
        let rsp = res.data
        if (rsp.status == 200) {
          window.localStorage.setItem('token', rsp.token)
          self.$router.replace('/choose')
        } else {
          self.errorMsg = "學號或身份證字號後四碼錯誤"
          self.isError = true
        }
      })
    }
  }
}
</script>
