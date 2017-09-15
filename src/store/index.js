import Vue from 'vue'
import Vuex from 'vuex'
import * as getters from './getters'
import * as actions from './actions'
import chat from './modules/chat'
Vue.use(Vuex)

const store = new Vuex.Store({
  getters,
  actions,
  modules: {
    chat
  }
})

export default store
