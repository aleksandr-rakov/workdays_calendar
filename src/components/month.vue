<template lang="html">
  <div>
    <table class="table is-bordered">
        <tr>
          <th colspan="7" class="month-header">
              {{month_name}}
          </th>
        </tr>
        <tr v-for="week in month.weeks">
          <td v-for="day in week" 
            v-bind:class="{ day:day.day, has_tags: day.tags.length}" 
            v-on:click="swal(day)"
          >
            <span>
              {{day.day || ''}}
            </span>
            <div class="ind" v-for="(tag,index) in day.tags" v-bind:style="{bottom: index*3+'px','background-color': tags_dict[tag]&&tags_dict[tag].color}">
            </div>
          </td>
        </tr>
    </table>
  </div>
</template>

<script>
import { default as swal } from 'sweetalert2'
import { mapState, mapGetters } from 'vuex'
import Vue from "vue"

export default {
  name: 'month',
  props: ['month'],
  methods: {
    swal_inputs: function(day){
      var res='';
      this.tags.forEach((tag) => {
        let checked=day.tags.indexOf(tag._id)!=-1?'checked':''
        res+=[
          '<label class="swal2-label">',
            '<input type="checkbox" lass="swal2-input" '+checked+' value="'+tag._id+'"> ',
            tag.name,
          '</label>',
        ].join('');
      })
      return res;
    },
    swal: function (day) {
      if(!day.day){
        return;
      }
      var that=this;
      this.$swal({
        title: 'Редактирование дня',
        showCancelButton: true,
        confirmButtonText: 'Да',
        cancelButtonText: 'Отмена',
        showLoaderOnConfirm: true,
        html: this.swal_inputs(day),
        preConfirm: function () {
          var tags=[]
          document.querySelectorAll('.swal2-label input').forEach((el) => {
            if(el.checked){
              tags.push(el.value)
            }
          })
          return new Promise(function (resolve, reject) {
            that.axios.post('/api/v1/calendar/day/'+day.day_int,{
              tags
            })
              .then(function(response) {
                Vue.set(day,'tags',tags)
                resolve(tags)
              },function(error){
                reject(error)
              })
          })
        },
        allowOutsideClick: false
      })
    }
  },
  computed:{
    month_name(){
      var objDate = new Date(this.month.month+"/01/2000"),
      locale = navigator.languages[0]||"en-us",
      month = objDate.toLocaleString(locale, { month: "long" });
      return month;
    },
    ...mapState({
      tags: state => state.tags.tags,
    }),
    ...mapGetters([
      'tags_dict'
    ]),
  }
}
</script>

<style>
.day{
  cursor: pointer;
  text-align: center;
  position: relative;
}
.day > span{
  z-index: 2;
  position: relative;
}
.has_tags{
  font-weight: bold;
}

.month-header{
  text-align: center !important;
}
.table tr:hover{
  background-color: #fff;
}
.swal2-modal .swal2-spacer{
  background-color: transparent;
}
.swal2-label{
  display: block;
  font-weight: bold;
  text-align: left;
  margin-left: 35%;
}
.ind{
  z-index: 1;
  height: 3px;
  margin: 0 -10px;
  position: absolute;
  width: 100%;
}
</style>