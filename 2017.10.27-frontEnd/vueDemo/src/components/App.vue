<style lang="scss">
@import "../css/app.scss";
</style>

<template lang="pug">
#app
  Loading
  transition(name="fade",mode="out-in")
    router-view
</template>

<script>
const Loading = require('./component/Loading.vue')

export default {
  name: 'app',
  data(){
    return {
      
    }
  },
  computed: {
    ...Vuex.mapState({
        loadingShow: state => state.loadingShow,
    }),
  },
  mounted(){
    
  },
  methods:{
    ...Vuex.mapActions(['changeLoading']),
  },
  watch:{
    
  },
  components:{
    Loading,
  }
}
</script>