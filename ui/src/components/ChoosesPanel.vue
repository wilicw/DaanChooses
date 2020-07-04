<template>
<v-card>
  <v-card-title>
    <span class="headline">選擇課程</span>
  </v-card-title>
  <v-card-text>
    <v-radio-group v-model="_selected" @change="save(index, _selected)">
      <div class="mb-4">
        <v-radio label="未選擇" color="orange darken-3" :value="-1"></v-radio>
      </div>
      <div v-for="(item, index) in data" :key="index">
        <v-radio
          class="my-4"
          color="orange darken-3"
          :label="`${item.name}`"
          :value="item.id"
          :disabled="item.selected!=-1&&item.selected!=index"
        ></v-radio>
      </div>
    </v-radio-group>
  </v-card-text>
</v-card>
</template>

<script>
export default {
  name: 'ChoosesPanel',
  props: ['index', 'selected', 'data'],
  /*
    data format:
    {
      id:
      name:
      selected:
    }
  */
  data: () => ({
    _selected: null
  }),
  beforeMount () {
    this._selected = this.selected
  },
  methods: {
    save: function (index, _selected) {
      this.$emit('save', index, _selected)
    }
  }
}
</script>
