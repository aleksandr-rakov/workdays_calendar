<template lang="html">
  <div>
    <h1 class="title">
      <router-link class="button is-active is-pulled-right" :to="{ path: '/users/add'}">
        Создать пользователя
      </router-link>
      Пользователи
    </h1>

    <showerror :error="errors"></showerror>

    <div class="columns" v-for="user in users">
      <div class="column">
        <router-link :to="{ path: '/users/'+user._id}" v-bind:class="{user_disabled:user.disabled}">
          {{user.name}}
        </router-link>
      </div>
    </div>

  </div>
</template>

<script>
import showerror from "./showerror"

export default {
  name: 'users',
  metaInfo: {
    title: 'Users'
  },
  data: function () {
    return {
      users: [],
      errors: ''
    }
  },
  methods: {
    loadUsers: function () {
      this.errors=null
      this.axios.get('/api/v1/users').then((response) => {
        this.users=response.data;
      }, (err) => {
        this.errors=err;
      })
    }
  },
  mounted: function () {
    this.loadUsers()
  },
  components:{
    showerror
  }
}
</script>

<style>
.user_disabled{
  color: #ccc;
}
</style>
