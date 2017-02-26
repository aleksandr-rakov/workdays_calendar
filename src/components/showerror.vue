<template>
  <div class="notification is-danger" v-if="error">
    {{error_parsed}}
  </div>
</template>

<script>
export default {
  name: 'showerror',
  props: ['error'],
  computed:{
    error_parsed (){
      return this.parse_error()
    }
  },
  methods: {
    parse_error () {
      var error=this.error;
      if(!error){
        return null;
      }
      var response=error.response;
      if(response){
        if(typeof(response.data)=='object'&&response.data){
          return response.data;
        }else{
          if(response.status&&response.statusText){
            return response.status+' '+response.statusText;
          }else{
            return 'Ошибка...';
          }
        }
      }else{
        return error;
      }
    }
  }
}
</script>
