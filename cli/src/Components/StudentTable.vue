<template>
  <v-container>
    <v-card flat>
      <v-card-title>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="open(file_url)">
          <v-icon left>mdi-download</v-icon> 匯出資料
        </v-btn>
      </v-card-title>
      <v-row>
        <v-col xs="12" md="8" class="pa-2">
          <v-text-field label="搜尋" v-model="search"></v-text-field>
        </v-col>
        <v-col xs="12" md="4" class="pa-2">
          <v-select :items="year_list" label="屆數"></v-select>
        </v-col>
      </v-row>
    </v-card>
    <v-data-table :headers="headers" :items="data" :search="search"></v-data-table>

  </v-container>
</template>

<script>
  export default {
    name: 'studentTable',
    props: ['data', 'file_url'],
    data: () => ({
      year_list: [111, 112],
      headers: [{
          text: '學號',
          align: 'left',
          value: 'id',
        },
        {
          text: '班級',
          value: 'class'
        },
        {
          text: '姓名',
          value: 'name'
        }
      ],
      search: ""
    }),
    methods: {
      open: function () {
        window.open(this.file_url, "_blank")
      }
    }
  }
</script>