<template>
  <v-card flat :color="color">
    <v-card-title class="pb-0">
      <p class="body-2 ma-0">{{ result.year }}選修結果</p>
    </v-card-title>
    <v-card-title class="pt-0 mt-0 mb-0 pb-2">
      <p class="title my-0">{{ result.name }}</p>
    </v-card-title>
    <v-card-text v-if="result.teacher || result.location || result.comment">
      <span v-if="result.teacher != ''">老師： {{ result.teacher }}<br /></span>
      <span v-if="result.location != ''"
        >地點： {{ result.location }}<br
      /></span>
      <span v-if="result.comment != ''">備註： {{ result.comment }}<br /></span>
    </v-card-text>
    <v-card-text v-if="!(result.teacher || result.location || result.comment)">
      <span>無詳細資料<br /></span>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'ResultPanel',
  props: ['result', 'color'],
  data: () => ({})
}
</script>
