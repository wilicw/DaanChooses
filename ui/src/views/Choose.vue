<template>
  <v-container>
    <v-row class="justify-center wrap">
      <v-col xs="12" lg="4" cols="12" class="pa-2">
        <v-card>
          <v-card-title>
            <p>{{stu.name}}</p>
            <br>
            <br>
            <p class="subtitle-2">{{stu.class}}</p>
          </v-card-title>
          <v-card-text>
            <a target="_blank" rel="noopener noreferrer"
              href="https://drive.google.com/open?id=1iMs2avB3t6qdQLGG1Q2GaWudW16dlicX">課程總覽</a><br>
            <span v-html="announcement"></span><br>
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="logout">登出</v-btn>
          </v-card-actions>
          <v-divider class="mx-5"></v-divider>
          <div v-for="result in results" :key="result.id">
            <v-card-title class="pb-0">
              <p class="body-2 ma-0">{{result.year}}選修結果</p>
            </v-card-title>
            <v-card-title class="pt-0 mt-0">
              <p class="title my-0">{{result.name}}</p>
            </v-card-title>
            <v-card-text v-if="result.teacher || result.location || result.comment">
              <span v-if="result.teacher!=''">老師： {{result.teacher}}<br></span>
              <span v-if="result.location!=''">地點： {{result.location}}<br></span>
              <span v-if="result.comment!=''">備註： {{result.comment}}<br></span>
            </v-card-text>
            <v-card-text v-if="!(result.teacher || result.location || result.comment)">
              <span>無詳細資料<br></span>
            </v-card-text>
            <v-divider class="mx-5"></v-divider>
          </div>
        </v-card>
      </v-col>
      <v-col xs="12" lg="8" cols="12" class="pa-2">
        <v-card>
          <v-card-title>選擇志願</v-card-title>
          <v-card-text>
            <v-alert border="bottom" colored-border :type="status.type" elevation="2" v-if="status.show">
              {{status.msg}}
            </v-alert>
            <div v-for="(item, index) in alreadyChosen" :key="index" @click="openSelectDialog(index)">
              <v-overflow-btn :items="[]" :label="`第 ${index+1} 志願 - ${alreadyChosen[index].name}`" readonly
                target="#dropdown-example-1" :disabled="disableSystem"></v-overflow-btn>
            </div>
            <v-btn class="mr-4" @click="submit" color="primary" :disabled="disableSystem">儲存志願</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
      <v-dialog v-model="dialog" width="600px">
        <v-card>
          <v-card-title>
            <span class="headline">選擇社團</span>
          </v-card-title>
          <v-card-text>
            <v-radio-group v-model="tempSelect" @change="saveChoose(nowSelect, tempSelect)">
              <div class="">
                <v-radio label="未選擇" color="orange darken-3" value="-1"></v-radio>
                <br>
              </div>
              <div v-for="(item, index) in avaiableChoose" :key="index">
                <v-radio :label="item.name" color="orange darken-3" :value="item.id"
                  :disabled="item.selected!=-1&&item.selected!=nowSelect"></v-radio>
                <br>
              </div>
            </v-radio-group>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-row>
  </v-container>
</template>

<script>
  import api from '../api'
  import _ from 'lodash'
  export default {
    data: () => ({
      maxChoose: 0,
      alreadyChosen: [],
      avaiableChoose: [],
      allChoose: [],
      announcement: '',
      dialog: false,
      tempSelect: 0,
      nowSelect: 0,
      noFullError: false,
      disableSystem: false,
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
    async beforeMount() {
      let self = this
      try {        
        // Process system basic informations
        let today = new Date().getTime()
        self.disableSystem = false
        let systemInfo = (await api.getSystemInfo()).data
        self.announcement = systemInfo.systemAnnouncement
        self.maxChoose = systemInfo.maxChoose
        if (today > new Date(systemInfo.closeDate).getTime()) {
          self.disableSystem = true
        }

        // get user basic information
        let userStatus = (await api.getStatus(window.localStorage.getItem('token'))).data[0]
        let stuClass = userStatus.class[0] + userStatus.class[1]
        self.stu = {
          name: userStatus.name,
          class: userStatus.class,
          year: userStatus.year
        }
        // if already have result than disable system
        let result = userStatus.result
        if (result.length == 0) {
          self.results = []
        } else {
          self.setResult(result)
        }

        //get all clubs data
        let allClubs = (await api.getClubs()).data
        self.allChoose = allClubs.data
        allClubs.forEach(i => {
          // the right year for student
          if (i.student_year == self.stu.year) {
            self.avaiableChoose.push({
              name: i.name,
              id: i.id,
              reject: i.reject,
              classification: i.classification,
              selected: -1
            })
          }
        })

        // get user chooses data
        let choose = (await api.getChooses(window.localStorage.getItem('token'))).data
        // if has chooses data than push in to ui
        if (choose.length != 0) {
          self.alreadyChosen = choose
          let index = 0
          self.alreadyChosen.forEach(i => {
            if (i.club_id != -1) {
              self.avaiableChoose.forEach(item => {
                if (item.id == i.club_id) {
                  item.selected = index
                  i.name = item.name
                }
              })
            } else {
              i.name = "未選擇"
            }
            index++
          })
        } else {
          self.init()
        }
        self.avaiableChoose.forEach(i => {
          self.results.forEach(result => {
            if (result.name == i.name) {
              i.selected = 100
            }
            if (result.classification != 0 && i.classification != 0 && result.classification ==
              i.classification) {
              i.selected = 100
            }
          })
          if (i.reject != null) {
            i.reject.split(',').forEach(j => {
              if (j == stuClass) {
                i.selected = 100
              }
            })
          }
        })
        self.$emit('login', userStatus.name)
        if (result.name != '') {
          self.disabled = true
        }
      } catch (error) {
        window.console.log(error)
        self.showMsg('error', `發生錯誤`)
        self.$router.replace('/')
      }
    },
    methods: {
      init: function () {
        for (let i = 0; i < this.maxChoose; i++) {
          this.alreadyChosen.push({
            club_id: -1,
            name: '未選擇'
          })
        }
      },
      setResult: async function (results) {
        let self = this
        await results.forEach(async (item) => {
          let id = item.id
          let clubData = (await api.getClubs(id)).data[0]
          let year = String(item.year)
          clubData['year'] = `${year.slice(0, 3)}學年第${year.slice(4, 5)}學期第${year.slice(6, 7)}次`
          clubData['_year'] = year
          self.results.push(clubData)
        })
        self.results = _.sortBy(self.results, ['_year'])
      },
      openSelectDialog: function (index) {
        this.tempSelect = this.alreadyChosen[index].club_id
        this.nowSelect = index
        //if has result then disabled button
        this.dialog = !this.disableSystem
      },
      saveChoose: function (index, id) {
        if (id == -1) {
          //no choose
          this.alreadyChosen[index].club_id = -1
          this.alreadyChosen[index].name = '未選擇'
        } else {
          //put choose in alreadyChosen
          this.alreadyChosen[index].club_id = id
          this.allChoose.forEach(item => {
            if (item.id == id) {
              this.alreadyChosen[index].name = item.name
            }
          })

          this.avaiableChoose.forEach(item => {
            if (item.id == id) {
              item.selected = index
            }
          })
        }
        //clean old choose
        this.avaiableChoose.forEach(i => {
          if (i.selected == index && i.id != id) {
            i.selected = -1
          }
        })

        this.tempSelect = null
        this.nowSelect = 0
        this.dialog = false
      },
      showMsg: function (type, msg) {
        this.status = {
          type: type,
          msg: msg,
          show: true
        }
        this.$vuetify.goTo(0, 'easeInOutCubic')
      },
      submit: async function () {
        let self = this
        self.noFullError = false
        self.alreadyChosen.forEach(i => {
          if (i.club_id == -1) {
            self.noFullError = true
            self.showMsg('warning', `需要填滿 ${self.maxChoose} 個志願！`)
            return
          }
        })
        if (self.noFullError) {
          return
        }
        let sendData = []
        let j = 1
        self.alreadyChosen.forEach(i => {
          sendData.push({
            step: j,
            club_id: i.club_id
          })
          j++
        })
        let chooseData = (await api.setChoose(window.localStorage.getItem('token'), sendData)).data
        if (chooseData.status == 200) {
          self.showMsg('success', `儲存成功！`)
        } else {
          self.showMsg('error', `發生錯誤`)
        }
      },
      logout: function () {
        window.localStorage.removeItem('token')
        this.$router.replace('/')
        this.name = ''
      }
    }
  }
</script>