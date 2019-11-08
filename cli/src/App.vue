<template>
  <v-app>
    <v-app-bar app class="orange accent-3" style="color: white">
      <v-toolbar-title class="headline text-uppercase">
        <b>{{title}}</b>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text color="white" v-if="false&&name!=''">
        <span class="mr-2">{{name}}</span>
      </v-btn>
    </v-app-bar>

    <v-content>
      <br>
      <router-view @login="display"></router-view>
    </v-content>
    <bottom></bottom>
  </v-app>
</template>

<script>
import api from './api'
import bottom from './Components/Footer'
export default {
  name: 'App',
  components: {
    bottom
  },
  data: () => ({
    name: '',
    title: ''
  }),
  beforeMount: function () {
    let self = this
    api.getSystemInfo().then(res => {
      self.title = res.data.title
      document.title = res.data.title
    })
  },
  methods: {
    display: function (name) {
      this.name = `你好 ${name}`
    }
  }
}
</script>
<style>
  a {
   text-decoration: none;
  }
</style>
