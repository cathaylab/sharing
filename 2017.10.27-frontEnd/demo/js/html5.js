$(function() {
  var hasClick = false;
  var aniHeight = 300;
  var sectionAni = new TimelineLite();
  
  $('aside a').on('click',function(){
    hasClick = !hasClick;
    
    if(hasClick) aniHeight = 500;
    else aniHeight = 50;

    sectionAni
      .play()
      .to('section.style1', 1, { height: aniHeight })
      .to('section.style2', 1, { height: aniHeight });
  });

  $('nav a').on('click', function(){
    if(sectionAni.paused()) sectionAni.play();
    else sectionAni.pause();
  })
});
