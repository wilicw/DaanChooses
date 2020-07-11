<template>
  <v-container>
    <v-row class="justify-center wrap">
      <v-col xs="12" lg="4" cols="12">
        <v-skeleton-loader
          class="mx-auto elevation-2 px-5 py-3"
          type="article, divider, list-item-three-line"
          v-if="loading && $vuetify.breakpoint.name != 'xs'"
        ></v-skeleton-loader>
        <v-card class="elevation-2" v-if="!loading">
          <v-card-title>
            <p class="title">{{stu.class}} {{stu.name}}</p>
          </v-card-title>
          <v-card-text>
            <span v-html="announcement"></span><br>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text><a target="_blank" rel="noopener noreferrer"
              href="https://drive.google.com/file/d/1C3CNrUveAy8rIdW-1R-kjx4U3lkj4wNz/view">課程總覽</a><br></v-btn>
            <v-btn class="mr-3" color="primary" text @click="logout">登出</v-btn>
          </v-card-actions>
          <v-divider class="mx-5"></v-divider>
          <div v-for="result in results" :key="result.id">
            <ResultPanel :result="result"></ResultPanel>
            <v-divider class="mx-5"></v-divider>
          </div>
        </v-card>
      </v-col>
      <v-col xs="12" lg="8" cols="12">
        <v-skeleton-loader
          class="mx-auto elevation-2 px-3 pb-5"
          type="article, list-item-three-line, list-item-three-line, heading"
          v-if="loading"
        ></v-skeleton-loader>
        <v-card class="elevation-5" v-if="!loading">
          <v-card-title>課程志願序</v-card-title>
          <v-card-text>
            <div v-for="(item, index) in alreadyChosen" :key="index" @click="openSelectDialog(index)">
              <v-overflow-btn :items="[]" :label="`第 ${index+1} 志願 - ${alreadyChosen[index].name}`" readonly
                target="#dropdown-example-1" :disabled="disableSystem"></v-overflow-btn>
            </div>
            <v-btn class="mr-4" @click="submit(false)" color="primary" :disabled="disableSystem">儲存志願</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
      <v-dialog v-model="dialog" width="600px">
        <ChoosesPanel
          :data="availableChooses"
          :selected="tempSelect"
          :selectedindex="nowSelect"
          @save="saveChoose"
        ></ChoosesPanel>
      </v-dialog>
    </v-row>
    <v-snackbar
      v-model="status.show"
      :color="status.type"
    >
      {{ status.msg }}
    </v-snackbar>
  </v-container>
</template>

<script>
import api from '../api'
import _ from 'lodash'
import ChoosesPanel from '../components/ChoosesPanel'
import ResultPanel from '../components/ResultPanel'
export default {
  components: {
    ChoosesPanel,
    ResultPanel
  },
  data: () => ({
    loading: true,
    maxChoose: 0,
    alreadyChosen: [],
    availableChooses: [],
    allChoose: [],
    announcement: '',
    dialog: false,
    tempSelect: 0,
    nowSelect: 0,
    disableSystem: false,
    nowYear: 0,
    status: {
      msg: '',
      type: '',
      show: false
    },
    stu: {
      name: '',
      class: '',
      year: 0
    },
    results: []
  }),
  async beforeMount () {
    const self = this
    try {
      // Process system basic informations
      const today = new Date().getTime()
      self.disableSystem = false
      const systemInfo = (await api.getSystemInfo()).data
      self.announcement = systemInfo.systemAnnouncement
      self.maxChoose = systemInfo.maxChoose
      self.nowYear = parseInt(systemInfo.year)
      if (today > new Date(systemInfo.closeDate).getTime()) {
        self.disableSystem = true
      }

      // get user basic information
      const userStatus = (await api.getStatus(window.localStorage.getItem('token'))).data[0]
      const stuDerpartment = userStatus.class[0] + userStatus.class[1]
      self.stu = {
        name: userStatus.name,
        class: userStatus.class,
        year: userStatus.year
      }
      // if already have result than disable system
      const result = userStatus.result
      result.length ? self.setResult(result) : self.results = []

      // get all clubs data
      const allClubs = (await api.getClubs()).data
      self.allChoose = allClubs
      self.availableChooses = _.reduce(allClubs, (result, club) => {
        // push this right stu year club into availableChooses
        console.log(club.year)
        if (club.student_year === self.stu.year && club.year === self.nowYear) {
          result.push({
            name: club.name,
            id: club.id,
            reject: club.reject,
            classification: club.classification,
            selected: -1
          })
        }
        return result
      }, [])

      // get user chooses data
      self.alreadyChosen = (await api.getChooses(window.localStorage.getItem('token'))).data
      if (!self.alreadyChosen.length) {
        self.alreadyChosen = _.times(self.maxChoose, () => ({
          club_id: -1,
          name: '未選擇'
        }))
      }
      // if has chooses data than push in to ui
      _.each(self.alreadyChosen, (i, index) => {
        if (i.club_id !== -1) {
          _.map(self.availableChooses, obj => {
            if (obj.id === i.club_id) {
              obj.selected = index
              i.name = obj.name
            }
            return obj
          })
        }
      })

      _.each(self.availableChooses, i => {
        _.each(self.results, result => {
          if (i.classification === -1 && i.selected === -1) {
            i.selected = -1
          } else if (
            (result.name === i.name) ||
            (result.classification && i.classification && result.classification === i.classification) ||
            (i.reject && _.includes(i.reject, stuDerpartment))
          ) { i.selected = Number.MAX_SAFE_INTEGER }
        })
      })
      self.$emit('login', userStatus.name)
      self.loading = false
    } catch (error) {
      console.log(error)
      self.showMsg('error', '發生錯誤')
      self.$router.replace('/')
    }
  },
  methods: {
    setResult: async function (results) {
      const self = this
      for (const club of results) {
        const id = club.id
        const clubData = (await api.getClubs(id)).data[0]
        const year = String(club.year)
        clubData.year = `${year.slice(0, 3)}學年第${year.slice(4, 5)}學期第${year.slice(6, 7)}次`
        clubData._year = parseInt(year)

        // if already have result in this year then disable system
        if (clubData._year === self.nowYear) {
          self.disableSystem = true
        }
        self.results.push(clubData)
      }
      self.results = _.sortBy(self.results, [obj => {
        // times -1 for reverse order
        return obj._year * -1
      }])
    },
    openSelectDialog: function (index) {
      this.tempSelect = this.alreadyChosen[index].club_id
      this.nowSelect = index
      // if has result then disabled button
      this.dialog = !this.disableSystem
    },
    saveChoose: function (index, id) {
      if (id === -1) {
        // no choose
        this.alreadyChosen[index].club_id = -1
        this.alreadyChosen[index].name = '未選擇'
      } else {
        // put choose in alreadyChosen
        this.alreadyChosen[index].club_id = id
        // set club name
        const club = _.findLast(this.allChoose, obj => {
          return obj.id === id
        })
        this.alreadyChosen[index].name = club.name

        _.map(this.availableChooses, obj => {
          if (obj.id === id) { obj.selected = index }
          return obj
        })
      }
      // clean old choose
      _.map(this.availableChooses, obj => {
        if (obj.selected === index && obj.id !== id) { obj.selected = -1 }
        return obj
      })

      // close dialog
      this.tempSelect = null
      this.nowSelect = 0
      this.dialog = false

      console.log(this.alreadyChosen)
      console.log(this.availableChooses)
      console.log(this.allChoose)
      // try to submit
      this.submit()
    },
    showMsg: function (type, msg) {
      this.status = {
        type: type,
        msg: msg,
        show: true
      }
      this.$vuetify.goTo(0, 'easeInOutCubic')
    },
    submit: async function (noPopUpMsg = true) {
      const self = this
      // is contain club_id == -1
      const noFullError = _.findKey(self.alreadyChosen, ['club_id', -1])
      if (noFullError) {
        if (!noPopUpMsg) {
          self.showMsg('warning', `需要填滿 ${self.maxChoose} 個志願！`)
        }
        return
      }
      const sendData = []
      _.each(self.alreadyChosen, (obj, index) => {
        sendData.push({
          step: index + 1,
          club_id: obj.club_id
        })
      })
      const chooseData = (await api.setChoose(window.localStorage.getItem('token'), sendData)).data
      if (noPopUpMsg) { return }
      if (chooseData.status === 200) {
        self.showMsg('success', '儲存成功！')
      } else {
        self.showMsg('error', '發生錯誤')
      }
    },
    logout: function () {
      window.localStorage.removeItem('token')
      this.$router.replace('/')
    }
  }
}
</script>
