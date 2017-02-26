
import Vue from "vue"
import axios from 'axios'

const tags_store = {
    state: {
        tags: [],
        errors: null
    },
    actions: {
        addTag({commit}, tag) {
            commit('ADD_TAG', tag)
        },
        loadTags({commit}) {
            commit('SET_ERRORS', null)
            axios.get('/api/v1/tags').then((response) => {
                commit('SET_TAGS', response.data)
              }, (err) => {
                commit('SET_ERRORS', err)
              })
        }
    },
    mutations: {
        ADD_TAG(state, tag) {
            state.tags.push(tag)
        },
        SET_TAGS(state, tags) {
            Vue.set(state,'tags',tags)
        },
        SET_ERRORS(state, errors) {
            Vue.set(state,'errors',errors)
        }
    },
    getters: {
        tags_dict(state) {
            var res={}
            state.tags.forEach((tag) =>{
                res[tag._id]=tag;
            })
            return res
        }
    }
}

export default tags_store
