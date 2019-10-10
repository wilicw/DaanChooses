<template>
  <v-app>
    <v-app-bar app class="orange accent-3" style="color: white">
      <v-toolbar-title class="headline text-uppercase">
        <b>大安高工彈性學習選課系統</b>
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
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data: () => ({
    name: ''
  }),
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
