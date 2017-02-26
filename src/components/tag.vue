<template>
  <form @submit.prevent="save">
    <div class="columns">
      <div class="column">
        <label class="label">name</label>
        <p class="control">
          <input class="input" v-model="tag.name" type="text" required>
        </p>
      </div>
      <div class="column">
        <label class="label">color</label>
        <p class="control">
          <input class="input" v-model="tag.color" type="text" required>
        </p>
      </div>
      <div class="column">
        <label class="label">&nbsp;</label>
        <p class="control">
          <button class="button is-primary" :class="{'is-loading':busy}">{{create_mode&&'Добавить'||'Сохранить'}}</button>
        </p>
      </div>
    </div>
    <showerror :error="errors"></showerror>
  </form>
</template>

<script>
import Vue from "vue"
import showerror from "./showerror"

export default {
  name: 'tag',
  props: ['tag'],
  data () {
    return {
      busy: false,
      errors: null,
      create_mode: false
    }
  },
  mounted: function () {
    if(!this.tag._id){
      this.create_mode=true
    }
  },
  methods: {
    save () {
      if(this.busy) return;
      this.errors=null;
      this.busy=true;
      (this.tag._id?
            this.axios.post('/api/v1/tags/'+this.tag._id,this.tag):
            this.axios.put('/api/v1/tags',this.tag))
        .then((response) => {
          Vue.set(this,'tag',{})
          this.busy=false
          this.$store.dispatch('loadTags');
        },(error) => {
          this.errors=error
          this.busy=false
        })
    }
  },
  components: {
    showerror
  }
}
</script>
