import axois from 'axios'
import conf from '../project-config.js'

let config = {
  baseURL: conf.apiPath,
  timeout: 10000
}

let client = axois.create(config)

export default {
  login: (account, password)  => {
    return client.post('/login', {username: account, password: password})
  },
  ManageLogin: (account, password)  => {
    return client.post('/manage/login', {username: account, password: password})
  },
  getStatus: (token) => {
    return client.get('/user', { headers: {'Authorization': `Bearer ${token}`} })
  },
  getManageStatus: (token) => {
    return client.get('/manage/login', { headers: {'Authorization': `Bearer ${token}`} })
  },
  getClubs: (id='') => {
    return client.get(`/clubs/${id}`)
  },
  getChooses: (token) => {
    return client.get('/chooses', { headers: {'Authorization': `Bearer ${token}`} })
  },
  getNotChoose: (token) => {
    return client.get('/manage/notchoose', { headers: {'Authorization': `Bearer ${token}`} })
  },
  getManageChoose: (token) => {
    return client.get('/manage/choose/', { headers: {'Authorization': `Bearer ${token}`} })
  },
  getSystemInfo: () => {
    return client.get('/info')
  },
  setChoose: (token, choose) => {
    return client.post('/chooses', choose, { headers: {'Authorization': `Bearer ${token}`} })
  }
}
