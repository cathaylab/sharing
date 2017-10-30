<style lang="scss" scoped>
@import "./css/index/index.scss";
</style>

<template lang="pug">
  .wrapper.index
      
</template>

<script>

export default {
  name: 'Index',
  data(){
    return {
      
    }
  },
  computed: {
    ...Vuex.mapState({
      loadingShow: state => state.loadingShow,
    }),
  },
  methods:{
    ...Vuex.mapActions(['changeLoading']),
  },
  watch:{
    
  },
  beforeCreate(){

  },
  created(){

  },
  beforeMount(){
    
  },
  mounted(){
		this.changeLoading(false)
  },
  beforeUpdate(){

  },
  updated(){

  },
  beforeDestroy(){

  },
  destroyed(){
    
  },
  components:{

  }
}
</script>