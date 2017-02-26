import Vue from 'vue'
import Router from 'vue-router'
import home from './components/home'
import users from './components/users'
import user from './components/user'
import calendar from './components/calendar'
import tags from './components/tags'
import login from './components/login'
import auth from './auth'

Vue.use(Router)

// application routes
const routes = [
    { 
      path: '/',
      component: home
    },
    { path: '/login',
      component: login
    },
    {
      path: '/users/',
      component: users,
      meta: { auth: true },
    },
    {
      path: '/users/add',
      component: user,
      meta: { auth: true },
    },
    {
      path: '/users/:id',
      component: user,
      meta: { auth: true },
    },
    {
      path: '/tags',
      component: tags,
      meta: { auth: true },
    },
    { 
      path: '/calendar', 
      redirect: to => {      
        // в функцию в качестве аргумента передаётся путь
        // возвращаемым значением должна быть строка или объект пути
        return '/calendar/'+(new Date()).getFullYear()
      }
    },
    {
      path: '/calendar/:year',
      name: 'calendar',
      component: calendar,
      meta: { auth: true },
    }
]

const router=new Router({
  mode: 'history',
  routes,
  linkActiveClass: 'is-active'
})

router.beforeEach((to, from, next) => {
    if (to.meta.auth && !auth.profile) {
        auth.get_profile().then( ( ) => {
            if(!auth.authenticated)
              next({ path: '/login' })
            else
               next()
        },()=>{
          next({ path: '/login' })
        })
    } else {
        if(!auth.checked){
          auth.get_profile()
        }
        next()
    }
})

// document.addEventListener('click',  function(e){
//   console.log(e)
//   var found=false;
//   for(let i=0;i<e.path.length;i++){
//     if(e.path[i].attributes['route-reload']){
//       found=e.path[i].href;
//       break;
//     }
//   }
//   console.log(found)
//   if(found){
//     if(location.href==found){
//       console.log(11)
//       router.push(location.pathname+'?ddd')
//     }
//   }
// });

// export router instance
export default router;
