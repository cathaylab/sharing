$(function() {
	var helloWorld = ['Hello world!','Hello everyone!']
	
	$('button').on('click',function(){
		if($('p').text() === helloWorld[0]){
			$('p').text(helloWorld[1])
		}else{
			$('p').text(helloWorld[0])
		}
	})
});
