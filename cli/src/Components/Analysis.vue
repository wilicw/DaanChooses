<template>
  <v-card flat style="width: 100%">
    <v-card-title class="justify-center">
      <p>資料統計</p>
    </v-card-title>

    <v-tabs
      v-model="tab"
      grow
    >
      <v-tab>未填志願</v-tab>
      <v-tab>志願分析</v-tab>
      <v-tab>社團分析</v-tab>
      <v-tab>班級分析</v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item>
        <NotChoose></NotChoose>
      </v-tab-item>

      <v-tab-item>
        <v-card flat>
          <v-card-text>志願</v-card-text>
        </v-card>
      </v-tab-item>

      <v-tab-item>
        <v-card flat>
          <v-card-text>社團分析</v-card-text>
        </v-card>
      </v-tab-item>

      <v-tab-item>
        <v-card flat>
          <v-card-text>班級分析</v-card-text>
        </v-card>
      </v-tab-item>

    </v-tabs-items>
  </v-card>
</template>

<script>
import NotChoose from './Analysis/NotChoose'
export default {
  name: 'analysis',
  components: {
    NotChoose
  },
  data () {
    return {
      tab: null
    }
  },
  methods: {
  }
}
</script>
