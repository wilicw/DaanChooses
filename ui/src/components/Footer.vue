<template>
<v-container>
  <v-footer class="text-center pa-0 ma-0">
    <v-card flat tile width="100vw" class="text-center">
      <v-card-text class="orange--text">
        Made by <a target="_blank" rel="noopener noreferrer" href="https://github.com/wilicw">@wilicw</a>. Source Code on <a target="_blank" rel="noopener noreferrer" href="https://github.com/daancsc/DaanChoose-Flask"><strong>Github</strong></a><br>
        {{ new Date().getFullYear() }} - <a target="_blank" rel="noopener noreferrer" href="https://dacsc.club"><strong>DAAN Computer Study Club</strong></a>
      </v-card-text>
    </v-card>
  </v-footer>
</v-container>
</template>

<script>
export default {
  name: 'bottom',
  data: () => ({

  })
}
</script>
