<template lang="html">
  <div class="site">
    <navbar />
    <section class="section site-content">
      <div class="container is-fluid">
        <router-view></router-view>
      </div>
    </section>
  </div>
</template>

<script>
import navbar from './navbar'
import router from '../router'
import store from '../store'

export default {
  name: 'main',
  router: router,
  components: {
    navbar: navbar,
  },
  store: store,
  metaInfo: {
    // if no subcomponents specify a metaInfo.title, this title will be used
    title: 'Default Title',
    // all titles will be injected into this template
    titleTemplate: '%s | Workday Calendar'
  }
};
</script>

<style>
.site{
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}
.site-content{
  flex: 1;
}
</style>