$(document).ready( function() {
	$(".home-nav-btn").addClass("active");

	$(".say a").on('click',function(e){
		var previous = $(".say").children(".active");
		previous.removeClass('active'); // previous list-item
		$(e.target).addClass('active'); // activated list-item
		return true;
	});

	$('#post-picture').on('click',function(e){
		console.log('success');
		$("#id_image").click();
		$("#id_image").removeAttr('style');
		return true;
	});
});