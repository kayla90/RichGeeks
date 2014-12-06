$("#change-name").focusout( function() {
	var fullname = $(".intro-header").find("input").val();
	var full_name_table = $("#profile_form").find("#fullname");
	full_name_table.attr('value',fullname);
});