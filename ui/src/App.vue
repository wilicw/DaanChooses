<template>
  <v-app>
    <v-app-bar app class="orange accent-3" style="color: white">
      <v-toolbar-title class="headline text-uppercase">
        <b>{{title}}</b>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-app-bar>

    <v-content>
      <br>
      <router-view></router-view>
    </v-content>
    <bottom></bottom>
  </v-app>
</template>

<script>
import api from './api'
import bottom from './components/Footer'
import _ from 'lodash'
export default {
  name: 'App',
  components: {
    bottom
  },
  data: () => ({
    name: '',
    title: ''
  }),
  beforeMount: async function () {
    const self = this
    const systemInfo = _.findLast((await api.getSystemInfo()).data.data, ['_id', 0])
    self.title = systemInfo.title
    document.title = systemInfo.title
  }
}
</script>
<style>
  a {
    text-decoration: none;
  }

  * {
    font-family: 'Noto Sans', sans-serif;
  }

  ::-moz-selection {
    background: #FFE0B2;
  }

  ::selection {
    background: #FFE0B2;
  }
</style>
