<template>
  <v-container>
    <v-card flat>
    <v-data-table :headers="headers" :items="data" :search="search">
      <template v-slot:top>
      <v-toolbar flat color="white">
      <v-toolbar-title></v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          dark
          class="mb-2 pa-5"
          @click="open()"
        ><v-icon>mdi-file-download</v-icon> 匯出資料</v-btn>
        </v-toolbar>
        <v-text-field
          class="mx-3"
          prepend-icon="mdi-account-search"
          label="搜尋"
          v-model="search"
        ></v-text-field>
      </template>
      <template v-slot:item.action="{ item }">
        <v-icon @click="edit(item)">mdi-pencil</v-icon>
      </template>
    </v-data-table>
    </v-card>
    <v-row justify="center">
      <v-dialog v-model="dialog" max-width="600px">
        <v-card>
          <v-card-title>
            <span class="headline">學生資料</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    label="學號"
                    v-model="stu.account"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="班級"
                    v-model="stu.student_class"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="姓名"
                    v-model="stu.student_name"
                    required></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="座號"
                    v-model="stu.student_number"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    label="密碼"
                    v-model="stu.password"
                    required
                  ></v-text-field>
                </v-col>
                <v-subheader>
                  課程
                  <v-spacer></v-spacer>
                  <v-icon @click="newClub()" style="cursor: pointer">mdi-plus</v-icon>
                </v-subheader>
                <v-col cols="12">
                  <div v-for="result in stu.results" :key="result.id" @click="setClub(result)">
                    <v-hover v-slot:default="{ hover }" style="cursor: pointer">
                      <ResultPanel :result="result" :color="hover ? 'orange lighten-5' : 'white'"></ResultPanel>
                    </v-hover>
                  </div>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn class="mr-5" color="primary" @click="save()">儲存</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="selectDialog" width="600px">
        <ChoosesPanel
          :data="availableChooses"
          :selected="tempSelect"
          :selectedindex="nowSelect"
          @save="submit"
        ></ChoosesPanel>
      </v-dialog>
    </v-row>
  </v-container>
</template>

<script>
import ResultPanel from './ResultPanel'
import ChoosesPanel from './ChoosesPanel'
import api from '../api'
import _ from 'lodash'
// import _ from 'lodash'
export default {
  components: {
    ResultPanel,
    ChoosesPanel
  },
  name: 'studentTable',
  props: ['data', 'file_url'],
  data: () => ({
    dialog: false,
    selectDialog: false,
    stu: {},
    headers: [{
      text: '學號',
      align: 'left',
      value: 'account'
    },
    {
      text: '班級',
      value: 'class'
    },
    {
      text: '姓名',
      value: 'name'
    },
    {
      text: '編輯',
      value: 'action'
    }
    ],
    search: '',
    availableChooses: [],
    tempSelect: 0,
    nowSelect: 0
  }),
  methods: {
    edit: async function (item) {
      const stu = (await api.getStudents(window.localStorage.getItem('token'), item.id)).data
      this.stu = stu[0]
      const results = this.stu.results
      for (const [i, club] of results.entries()) {
        const year = String(club.year)
        const clubData = (await api.getClubs(club.club)).data
        this.stu.results[i].name = clubData[0].name
        this.stu.results[i]._year = year
        this.stu.results[i].year = `${year.slice(0, 3)}學年第${year.slice(4, 5)}學期第${year.slice(6, 7)}次`
      }
      this.stu.results = _.sortBy(this.stu.results, [obj => {
        // times -1 for reverse order
        return obj._year * -1
      }])
      this.dialog = true
    },
    open: function () {
      window.open(this.file_url, '_blank')
    },
    save: async function () {
      console.log(this.stu)
      _.each(this.stu.results, result => {
        result.year = result._year
      })
      const response = (await api.saveStudents(window.localStorage.getItem('token'), this.stu)).data
      console.log(response)
      this.dialog = false
    },
    setClub: async function (club, year = null) {
      if (!year) {
        console.log(club)
        const response = (await api.getClubs()).data
        this.availableChooses = _.filter(response, { year: parseInt(club._year) })
        _.each(this.availableChooses, club => {
          club.selected = -1
        })
        this.tempSelect = club.club
        this.nowSelect = club._year
        this.selectDialog = true
      } else {
        const response = (await api.getClubs()).data
        this.availableChooses = _.filter(response, { year: parseInt(year) })
        _.each(this.availableChooses, club => {
          club.selected = -1
        })
        this.tempSelect = 0
        this.nowSelect = year
        this.selectDialog = true
      }
    },
    submit: async function (year, id) {
      console.log(year, id)
      for (const [i, club] of this.stu.results.entries()) {
        console.log(year, club._year)
        if (year === club._year) {
          const clubData = (await api.getClubs(id)).data
          this.stu.results[i].name = clubData[0].name
          this.stu.results[i].club = id
          console.log(club)
        }
      }
      this.selectDialog = false
    },
    newClub: async function () {
      const nowYear = String((await api.getSystemInfo()).data.year)
      this.stu.results.push({
        club: 0,
        _year: nowYear
      })
      this.setClub(-1, nowYear)
    }
  }
}
</script>
