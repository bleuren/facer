// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from 'vuex'
import VueSession from 'vue-session'
import VueSocketio from 'vue-socket.io'
import socketio from 'socket.io-client'
import App from './App'
import router from './router'
import store from './store'

Vue.use(Vuex)
Vue.use(VueSession)
Vue.use(VueSocketio, socketio('http://127.0.0.1:5000'), store)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
