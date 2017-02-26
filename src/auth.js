import router from './router.js'
import store from './store'
import axios from 'axios'

export default {
    // authentication status
    authenticated: false,
    profile: null,
    checked: false,

    // Send a request to the login URL and save the returned JWT
    login(context, creds, redirect) {
        return axios.post('/api/v1/login', creds)
        .then(
         (response) => {
            const message=response.data.message;

            if (!message){
                this.authenticated = true
                localStorage.setItem('user',response.data.token)
            }else{
                context.errors=message;
            }
            // Redirect to a specified route
            if (redirect) {
                router.push(redirect)
            }
        },
        (errors) => {
            context.errors = errors;
        })
    },
    get_profile() {
        return axios.get('/api/v1/profile')
        .then(
         (response) => {
            this.profile=response.data;
            this.authenticated=true;
            this.checked=true;
            store.commit('set_profile',response.data)
        },
        (errors) => {
        })
    },
    // To log out
    logout: function() {
        this.authenticated = false;
        this.profile=null;
        this.checked=false;
        localStorage.removeItem('user')
        store.commit('set_profile',null)
        router.push('/login')
    }
}
