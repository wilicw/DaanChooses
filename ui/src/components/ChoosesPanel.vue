<template>
<v-card>
  <v-card-title>
    <span class="headline">選擇課程</span>
  </v-card-title>
  <v-card-text>
    <v-radio-group v-model="_selected" @change="save(selectedindex)">
      <div class="mb-4">
        <v-radio label="未選擇" color="orange darken-3" :value="-1"></v-radio>
      </div>
      <div v-for="(item, index) in data" :key="index">
        <v-radio
          class="my-4"
          color="orange darken-3"
          :label="`${item.name} ${(item.selected !== -1 && item.selected !== Number.MAX_SAFE_INTEGER) ? '- 第 '+parseInt(item.selected+1)+' 志願' : ''}`"
          :value="item.id"
          :disabled="item.selected!=-1&&item.selected!=selectedindex"
        ></v-radio>
      </div>
    </v-radio-group>
  </v-card-text>
</v-card>
</template>

<script>
export default {
  name: 'ChoosesPanel',
  props: ['selectedindex', 'selected', 'data'],
  /*
    data format:
    {
      id:
      name:
      selected:
    }
  */
  data: () => ({
    _: -1
  }),
  computed: {
    _selected: {
      get: function () {
        return this.selected
      },
      set: function (val) {
        this._ = val
      }
    }
  },
  methods: {
    save: function (selectedindex) {
      this.$emit('save', selectedindex, this._)
    }
  }
}
</script>
