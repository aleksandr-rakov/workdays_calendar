import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import auth_store from './modules/auth'
import tags_store from './modules/tags'

const store = new Vuex.Store({
  modules: {
    auth: auth_store,
    tags: tags_store
  }
})

export default store;
