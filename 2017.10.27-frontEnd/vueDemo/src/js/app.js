require('../index.pug');
require('es6-promise').polyfill();
const store = require('../js/store/store.js');
const router = require('../js/router.js');
const App = require('../components/App.vue');


$(()=>{
  new Vue({
    el: '#app',
    store,
    router,
    render: h => h(App)
  })
});

