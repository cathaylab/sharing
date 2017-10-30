const routes = [
  { path: '/', component: require('../components/index/Index.vue') },
  
  // { path:'*', component:require('error')}  //404
]

const router = new VueRouter({
  routes
})

module.exports = router;
