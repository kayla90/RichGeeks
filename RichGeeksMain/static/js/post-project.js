$("#project-title").focusout( function() {
	var title = $(".intro-header").find("input").val();
	var hidden_form = $(".panel-body").find("#title");
	hidden_form.attr('value',title);
});