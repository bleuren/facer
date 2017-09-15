import Vue from 'vue'
import * as types from '../mutation-types'
import moment from 'moment'
const actions = {
  sendmsg ({ commit }, message) {
    commit(types.SENDMSG, message)
  },
  signout ({ commit }) {
    commit(types.SIGNOUT)
  }
}
const getters = {
  message: state => state.message,
  items: state => state.items
}
const state = {
  message: null,
  items: [],
  history: []
}
const mutations = {
  SOCKET_CONNECT: (state, status) => {
    state.connect = true
  },

  SOCKET_MESSAGE: (state, message) => {
    state.items.push(message)
    state.message = message
  },
  [types.SENDMSG] (state, message) {
    (new Vue()).$socket.emit('sendmsg', {'id': new Date().getTime().toString(), 'user': message.user, 'content': message.content, 'dtime': moment().format('hh:mm')})
    state.value = null
    state.history.push('sendmsg')
  },

  [types.SIGNOUT] (state) {
    (new Vue()).$session.destroy()
    state.history.push('signout')
  }
}
export default {
  state,
  getters,
  actions,
  mutations
}
