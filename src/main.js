import Vue from 'vue'
import main from './components/main'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueSweetAlert from 'vue-sweetalert'
import Meta from 'vue-meta'

// Add a request interceptor
axios.interceptors.request.use(function (config) {
    // Do something before request is sent
    config.headers['X-Token'] = localStorage.getItem('user');
    return config;
  }, function (error) {
    // Do something with request error
    return Promise.reject(error);
  });

Vue.use(VueSweetAlert)
Vue.use(VueAxios, axios)
Vue.use(Meta)

new Vue(main).$mount('#app')
