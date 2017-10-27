$(function() {
  var hasClick = false;
  var aniHeight = 300;

  $('.aside a').on('click',function(){
    hasClick = !hasClick;
    
    if(hasClick) aniHeight = 500;
    else aniHeight = 50;

    $('.section.style1')
      .stop()
      .animate({'height':aniHeight},300);
  })
});
