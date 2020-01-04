<template>
  <v-container>
    <v-row
      class="justify-center wrap"
    >
      <v-col
        xs="12"
        sm="12"
        md="4"
        class="pa-2"
      >
        <v-card>
          <v-card-title>{{stu.class}} {{stu.name}}</v-card-title>
          <v-card-text><br>
            <a target="_blank" rel="noopener noreferrer" href="allClass.pdf">課程總覽</a><br>
            {{announcement}} <br>
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="logout">登出</v-btn>
          </v-card-actions>
        </v-card>
        <div v-for="result in results" :key="result.id">
          <br>
          <v-card v-if="result.name!=''">
            <v-card-title class="title">{{result.year}} 選修課程結果： {{result.name}}</v-card-title>
            <v-card-text>
              老師： {{result.teacher}}<br>
              地點： {{result.location}}<br>
              備註： {{result.comment}}<br>
            </v-card-text>
          </v-card>
        </div>
      </v-col>
      <v-col
        xs="12"
        sm="12"
        md="8"
        class="pa-2"
      >
        <v-card>
          <v-card-title>選擇志願</v-card-title>
          <v-card-text>
            <v-alert
              border="bottom"
              colored-border
              :type="status.type"
              elevation="2"
              v-if="status.show"
            >
              {{status.msg}}
            </v-alert>
            <div v-for="(item, index) in alreadyChosen" :key="index" @click="openSelectDialog(index)">
              <v-overflow-btn
                :items="[]"
                :label="`第 ${index+1} 志願 - ${alreadyChosen[index].name}`"
                readonly
                target="#dropdown-example-1"
                :disabled="disableSystem"
              ></v-overflow-btn>
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
                <v-radio
                  label="未選擇"
                  color="orange darken-3"
                  value="-1"
                ></v-radio>
                <br>
              </div>
              <div v-for="(item, index) in avaiableChoose" :key="index">
                <v-radio
                  :label="item.name"
                  color="orange darken-3"
                  :value="item.id"
                  :disabled="item.selected!=-1&&item.selected!=nowSelect"
                ></v-radio>
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
      class: ''
    },
    results: []
  }),
  beforeMount() {
    let self = this
    let today = new Date()
    self.disableSystem = false
    api.getSystemInfo().then(res => {
      self.announcement = res.data.systemAnnouncement
      self.maxChoose = res.data.maxChoose
      if(today.valueOf() > Date.parse(res.data.closeDate).valueOf()){
        self.disableSystem = true
      }
    })
    api.getClubs().then((res) => {
      self.allChoose = res.data
      res.data.forEach(i=>{
        self.avaiableChoose.push({
          name: i.name,
          id: i.id,
          reject: i.reject,
          selected: -1
        })
      })
      api.getStatus(window.localStorage.getItem('token')).then((res) => {
        let data = res.data[0]
        let stuClass = data.class[0]+data.class[1]
        self.stu = {
          name: data.name,
          class: data.class
        }
        let result = data.result
        if (result.length==0) {
          self.results = []
        } else {
          self.setResult(result)
        }
        let choose
        api.getChooses(window.localStorage.getItem('token')).then((res) => {
          choose = res.data
          if (choose.length!=0) {
            self.alreadyChosen = choose
            let index = 0
            self.alreadyChosen.forEach(i=>{
              if (i.club_id != -1) {
                self.avaiableChoose[i.club_id-1].selected = index
                i.name = self.avaiableChoose[i.club_id-1].name
              } else {
                i.name = "未選擇"
              }
              index++
            })
          } else {
            self.init()
          }
          self.avaiableChoose.forEach(i=>{
            if (i.reject!=null) {
              i.reject.split(',').forEach(j=>{
                if (j==stuClass) {
                  i.selected = 100
                }
              })
            }
          })
          self.$emit('login', data.name)
          if (result.name != '') {
            self.disabled = true
          }
        })
      }).catch((error) => {
        window.console.log(error)
        self.showMsg('error', `發生錯誤`)
        self.$router.replace('/')
      })
    }).catch((error) => {
      window.console.log(error)
      self.showMsg('error', `發生錯誤`)
      self.$router.replace('/')
    })
  },
  methods: {
    init: function () {
      for (let i = 0; i < this.maxChoose; i++) {
        this.alreadyChosen.push({club_id: -1, name: '未選擇'})
      }
    },
    setResult: function (array) {
      let self= this
      array.forEach(item => {
        let id = item.id
        api.getClubs(id).then((res) => {
          let data = res.data[0]
          data['year'] = item.year
          data.comment = data.comment!='' ? data.comment : '無'
          self.results.push(data)
        })
        self.avaiableChoose.forEach(i=>{
          if (id == i.id) {
            i.selected = 100
          }
        })
      })
      //this.disableSystem = true
    },
    openSelectDialog: function (index) {
      this.tempSelect=this.alreadyChosen[index].club_id
      this.nowSelect=index
      //if has result then disabled button
      this.dialog=!this.disableSystem
    },
    saveChoose: function (index, id) {
      if (id==-1) {
        //no choose
        this.alreadyChosen[index].club_id = -1
        this.alreadyChosen[index].name = '未選擇'
      } else {
        //put choose in alreadyChosen
        this.alreadyChosen[index].club_id = id
        this.alreadyChosen[index].name = this.allChoose[id-1].name
        this.avaiableChoose[id-1].selected = index
      }
      //clean old choose
      this.avaiableChoose.forEach(i=>{
        if (i.selected==index&&i.id!=id) {
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
    submit: function () {
      let self = this
      self.noFullError = false
      self.alreadyChosen.forEach(i=>{
        if (i.club_id==-1) {
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
      self.alreadyChosen.forEach(i=>{
        sendData.push({
          step: j,
          club_id: i.club_id
        })
        j++
      })
      api.setChoose(window.localStorage.getItem('token'), sendData).then((res) => {
        if (res.data.status==200) {
          self.showMsg('success', `儲存成功！`)
        } else {
          self.showMsg('error', `發生錯誤`)
        }
      })
    },
    logout: function () {
      window.localStorage.removeItem('token')
      this.$router.replace('/')
      this.name = ''
    }
  }
}
</script>
