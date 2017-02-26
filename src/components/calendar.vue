<template lang="html">
  <div>
    <h1 class="title calendar-title">
      <router-link :to="{ name: 'calendar', params: { year: year-1 }}" class="year-link">
        ◀
      </router-link>
      {{year}}
      <router-link :to="{ name: 'calendar', params: { year: year+1 }}" class="year-link">
        ▶
      </router-link>
    </h1>

    <showerror :error="errors"></showerror>

    <div class="columns is-multiline">
      <div class="column is-4" v-for="item in months">
        <month v-bind:month="item"/>
      </div>
    </div>

  </div>
</template>

<script>
import month from './month'
import showerror from "./showerror"

export default {
  name: 'calendar',
  metaInfo() { 
    return{
      title: this.year+' год'
    }
  },
  data: function () {
    return {
      months: [],
      year: (new Date()).getFullYear(),
      errors: ''
    }
  },
  methods: {
    loadYear: function () {
      this.errors=null
      this.year=parseInt(this.$route.params.year);
      this.axios.get('/api/v1/calendar/'+this.year).then((response) => {
        this.months=response.data;
      }, (err) => {
        this.errors=err
      })
    }
  },
  mounted: function () {
    this.loadYear()
    this.$store.dispatch('loadTags');
  },
  watch: {
    // в случае изменения маршрута запрашиваем данные вновь
    '$route': 'loadYear'
  },
  components:{
    month,
    showerror
  }
}
</script>

<style>
.calendar-title{
  text-align: center;
}
.year-link:hover{
  text-decoration: none !important;
  border-bottom: none !important;
}
</style>