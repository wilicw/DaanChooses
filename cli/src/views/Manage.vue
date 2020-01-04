<template>
<v-container>
  <v-card
    class="d-flex"
  >
  <v-card>
    <v-navigation-drawer permanent :mini-variant.sync="mini">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title">
            管理
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ name }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <v-list @click.stop="mini = !mini">
        <v-list-item v-for="item in items" :key="item.title" @click="switchTab(item.id)" link>
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item @click="logout">
          <v-list-item-icon>
            <v-icon>mdi-logout-variant</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>登出</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </v-card>
    <analysis @click="mini = true" v-if="tab==3"></analysis>
    <setting @click="mini = true" v-if="tab==0"></setting>
  </v-card>
</v-container>
</template>

<script>
import api from '../api'
import analysis from '../Components/Analysis'
import setting from '../Components/Setting'
export default {
  components: {
    analysis,
    setting
  },
  data: () => ({
    name: '',
    tab: 0,
    mini: true,
    items: [
      {
        title: '系統設定',
        icon: 'mdi-help-box',
        id: 0
      },
      {
        title: '學生管理',
        icon: 'mdi-account-edit',
        id: 1
      },
      {
        title: '社團管理',
        icon: 'mdi-account-group',
        id: 2
      },
      {
        title: '統計分析',
        icon: 'mdi-chart-line-variant',
        id: 3
      },
      {
        title: '分發',
        icon: 'mdi-help-box',
        id: 4
      }
    ]
  }),
  beforeMount() {
    let self = this
    api.getManageStatus(window.localStorage.getItem('token')).then(res => {
      let status = res.data.status
      if (status == 401) {
        self.logout()
      }
    })
  },
  methods: {
    switchTab: function (id) {
      this.tab = id
    },
    logout: function() {
      window.localStorage.removeItem('token')
      this.$router.replace('/')
      this.name = ''
    }
  }
}
</script>
