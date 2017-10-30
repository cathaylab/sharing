<style lang="scss" scoped>
@import "./css/component/loading.scss";
</style>

<template lang="pug">
transition(name="fade",mode="out-in")
  .loading(v-if="loadingShow")
    span {{ percent }}
</template>

<script>
export default {
  name: 'Loading',
  data(){
    return {
      num: 0,
      randomTime: 100,
      timerTimeout:'',
    }
  },
  computed: {
    ...Vuex.mapState({
        loadingShow: state => state.loadingShow
    }),
    percent(){
      return this.num + '%'
    }
  },
  mounted(){
    // this.randomTime = Math.floor(Math.random()*50 + 100)
    this.timer()
  },
  methods:{
    timer(){
      this.num == 0 ? this.num = 98 : this.num += 1
      if(this.num >= 100) return
      this.timerTimeout = setTimeout(()=>{ this.timer() }, this.randomTime)
    }
  },
}
</script>