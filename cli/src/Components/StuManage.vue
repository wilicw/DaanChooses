<template>
<v-container>
  <v-footer class="text-center pa-0 ma-0">
    <v-card flat tile color="#fafafa" width="100vw" class="text-center">
      <v-card-text class="orange--text">
        {{ new Date().getFullYear() }} - <a target="_blank" rel="noopener noreferrer" href="https://dacsc.club" class="orange--text"><strong>DAAN Computer Study Club</strong></a>
      </v-card-text>
    </v-card>
  </v-footer>
</v-container>
</template>

<script>
export default {
  name: 'stuManage',
  data: () => ({

  })
}
</script>
