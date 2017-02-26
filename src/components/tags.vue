<template lang="html">
  <div>
    <h1 class="title">
      Теги
    </h1>

    <showerror :error="errors"></showerror>

    <div class="columns" v-for="tag in tags">
      <div class="column">
        <tag :tag="tag"></tag>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <tag :tag="{}"></tag>
      </div>
    </div>

  </div>
</template>

<script>
import showerror from "./showerror"
import tag from "./tag"
import Vue from "vue"
import { mapState } from 'vuex'

export default {
  name: 'tags',
  metaInfo: {
    title: 'Tags'
  },
  data: function () {
    return {
    }
  },
  methods: {
    addTag: function () {
      Vue.set(this,'new_tag',{
        name: '',
        color: '#eb0000'
      })
      this.show_add_tag=true;
    }
  },
  mounted: function () {
    this.$store.dispatch('loadTags');
  },
  computed: {
    ...mapState({
      tags: state => state.tags.tags,
      errors: state => state.tags.errors
    })
  },
  components:{
    showerror,
    tag,
  }
}
</script>
