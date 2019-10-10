import axois from 'axios'

let config = {
  baseURL: 'https://dacsc.club/chooseapi',
  timeout: 10000
}

let client = axois.create(config)

export default {
  login: (account, password)  => {
    return client.post('/login', {username: account, password: password})
  },
  getStatus: (token) => {
    return client.get('/user', { headers: {'Authorization': `Bearer ${token}`} })
  },
  getClubs: (id='') => {
    return client.get(`/clubs/${id}`)
  },
  getChooses: (token) => {
    return client.get('/chooses', { headers: {'Authorization': `Bearer ${token}`} })
  },
  setChoose: (token, choose) => {
    return client.post('/chooses', choose, { headers: {'Authorization': `Bearer ${token}`} })
  }
}
