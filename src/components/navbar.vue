<template lang="html">
  <nav class="nav has-shadow" >
    <div class="nav-left">
      <router-link class="nav-item is-brand" to="/">
        Vue Project
      </router-link>
      <router-link class="nav-item is-tab" to="/users">
        Пользователи
      </router-link>
      <router-link class="nav-item is-tab" to="/tags">
        Теги
      </router-link>
      <router-link class="nav-item is-tab" :to="{ path: '/calendar'}">
        Календарь
      </router-link>
    </div>
    <div class="nav-right">
      <span class="nav-item">
        {{profile&&profile.name||''}}
        <a class="button" @click.prevent="logout" v-show="profile">
          Выйти
        </a>
        <router-link class="button" :to="{ path: '/login/'}" v-show="!profile">
          Войти
        </router-link>
      </span>
    </div>
  </nav>
</template>

<script>
import auth  from '../auth'
import { mapState } from 'vuex'

export default {
  name: 'navbar',
  data: function () {
    return {
    }
  },
  methods: {
    logout () {
      auth.logout()
    }
  },
  computed: {
    ...mapState({
      profile: state => state.auth.profile
    })
  }
}
</script>
