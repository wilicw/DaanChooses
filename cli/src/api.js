import axois from 'axios'
import conf from '../project-config'

let config = {
  baseURL: conf.apiPath,
  timeout: 100000
}

let client = axois.create(config)

export default {
  login: (account, password)  => {
    return client.post('/login', {username: account, password: password})
  },
  ManageLogin: (account, password)  => {
    /*
      {
        "username": string,
        "password": string
      }
    */
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
  getStudents: (token) => {
    return client.get('/manage/students', { headers: {'Authorization': `Bearer ${token}`} })
  },
  getManageChoose: (token) => {
    return client.get('/manage/choose/', { headers: {'Authorization': `Bearer ${token}`} })
  },
  getSystemInfo: () => {
    return client.get('/info')
  },
  setChoose: (token, choose) => {
    /*
      [
        {
          "step": integer,
          "club_id": integer
        },
        {
          "step": integer,
          "club_id": integer
        },
        .
        .
        .
        {
          "step": integer,
          "club_id": integer
        }
      ]
    */
    return client.post('/chooses', choose, { headers: {'Authorization': `Bearer ${token}`} })
  },
  saveSetting: (token, setting) => {
    /*
      {
        "title": string,
        "maxChoose": integer,
        "systemAnnouncement": string,
        "closeDate": string,
        "year": integer
      }
    */
    return client.post('/info', setting, { headers: {'Authorization': `Bearer ${token}`} })
  }
}
