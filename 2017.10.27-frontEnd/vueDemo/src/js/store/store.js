const store = new Vuex.Store({
  state: {
    loadingShow: true,
  },

  mutations: {
    changeLoading (state, show) {
      state.loadingShow=show
    },
    
  },

  getters: {

  },

  actions: {
    changeLoading ({ commit }, show) {
      commit('changeLoading',show)
    },
    // tracker_pg({ commit }, value ){
    //   let valueFin = value
    //   if(!device.desktop()) valueFin = '/m' + value

    //   ga('send', 'pageview',valueFin);
    //   ga('eventSite.send', 'pageview',valueFin);
    // },
    // tracker_btn({ commit }, valuebt ){
    //   let valueFin = valuebt
    //   if(!device.desktop()) valueFin = '/m' + valuebt

    //   ga('send', 'event', 'button', 'click', valueFin);
    //   ga('eventSite.send', 'event', 'button', 'click', valueFin);
    // },
  },
  modules:{
    
  }
})

module.exports = store;

