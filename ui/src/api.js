import axois from 'axios'
import conf from './project-config'

const config = {
  baseURL: conf.apiPath,
  timeout: 100000
}

const client = axois.create(config)

export default {
  login: (account, password) =>
    client.post('/login', { username: account, password: password }),
  ManageLogin: (account, password) =>
    client.post('/manage/login', { username: account, password: password }),
  getStatus: (token) =>
    client.get('/user', { headers: { Authorization: `Bearer ${token}` } }),
  getManageStatus: (token) =>
    client.get('/manage/login', { headers: { Authorization: `Bearer ${token}` } }),
  getClubs: (id = '') =>
    client.get(`/clubs/${id}`),
  getChooses: (token) =>
    client.get('/chooses', { headers: { Authorization: `Bearer ${token}` } }),
  getNotChoose: (token) =>
    client.get('/manage/notchoose', { headers: { Authorization: `Bearer ${token}` } }),
  getStudents: (token, id = '') =>
    client.get(`/manage/students/${id}`, { headers: { Authorization: `Bearer ${token}` } }),
  saveStudents: (token, stu) =>
    client.post('/manage/students', stu, { headers: { Authorization: `Bearer ${token}` } }),
  getManageChoose: (token) =>
    client.get('/manage/choose/', { headers: { Authorization: `Bearer ${token}` } }),
  getSystemInfo: () =>
    client.get('/info'),
  setChoose: (token, choose) =>
    client.post('/chooses', choose, { headers: { Authorization: `Bearer ${token}` } }),
  saveSetting: (token, setting) =>
    client.post('/info', setting, { headers: { Authorization: `Bearer ${token}` } })
}
