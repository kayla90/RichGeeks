function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready( function() {
	$(".me-nav-btn").addClass("active");

	// after a click action on the .list-group-item
	$('#function-menu li').on('click',function(e){
		var previous = $(this).parent().children(".active");
		previous.removeClass('active'); // previous list-item
		$(this).addClass('active'); // activated list-item
		// $(previous.attr("href")).attr('style','display:none'); // hide the content of the previous panel
		// $($(this).attr("href")).removeAttr('style'); // display the content
		return false;
	});

	$('#function-menu li.overview').on('click',function(e){
		$.get( "/profile-overview/"+$(".profile-main").attr("user"), function( data ) {
			$("#profile-right-bottom").html(data);
		});
	});

	$('#function-menu li.analysis').on('click',function(e){
		$.get( "/profile-analysis/"+$(".profile-main").attr("user"), function( data ) {
			$("#profile-right-bottom").html(data);
			$.post( "/language/kayla90", function( data2 ) {
				$(".tab-content").html(data2);	
			});	
		});
	});

	$('#function-menu li.project').on('click',function(e){
		$("#profile-right-bottom").html("");
	});

	$('#function-menu li.friends').on('click',function(e){
		$("#profile-right-bottom").html("");
	});

	$('#face-edit-row #friend').on('click',function(e){
		$(this).attr('id', 'unfriend');
		if ($(this).html() === "Add Friend") {
			$(this).html("Unfriend");
		} else {
			$(this).html("Add friend");
		};
		
	});

	// $('#edit').on('click',function(e){
	// 	// $(this).html("Save");
	// 	// $(this).attr("id", "save");
	// 	$.get( "/edit", function( data ) {
	// 		$("#profile-right-bottom").html(data);	
	// 	});
	// });


	// $('.add-image').on('click',function(e){
	// 	console.log('success');
	// 	$("#id_image").click();
	// 	$("#id_image").removeAttr('style');
	// });

	// setInterval(getLastestGrumbls, 10000);
});


	$(document).on('click', 'li .gender', function (event) {
		console.log("1");
		$.post( "/language/kayla90", function( data ) {
			$(".tab-content").html("");	
		});	
	});