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


$(function() {

    $('#side-menu').metisMenu();

});

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size
$(function() {
    $(window).bind("load resize", function() {
        topOffset = 50;
        width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
        if (width < 768) {
            $('div.navbar-collapse').addClass('collapse')
            topOffset = 100; // 2-row-menu
        } else {
            $('div.navbar-collapse').removeClass('collapse')
        }

        height = (this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height;
        height = height - topOffset;
        if (height < 1) height = 1;
        if (height > topOffset) {
            $("#page-wrapper").css("min-height", (height) + "px");
        }
    })
});

function skill(){
  var box = '<select id="thedropdown"><option value ="JavaScript">JavaScript</option><option value ="Ruby">Ruby</option><option value="Java">Java</option><option value="PHP">PHP</option><option value="Python">Python</option><option value="C++">C++</option><option value="C">C</option><option value="Objective-C">Objective-C</option><option value="C#">C#</option><option value="Shell">Shell</option><option value="CSS">CSS</option><option value="Perl">Perl</option></select>';
       bootbox.dialog({
                title: "Select your favourite language",
                message: box,
                buttons: {
                    success: {
                        label: "Save",
                        className: "btn-success",
                        callback: function () {
                            var answer = $('#thedropdown').val();
                            console.log(answer);
                             $.ajax({
                        url: "/set_language",
                        type: "POST",
                        data : { 'username' : '{{username}}', 'language' : answer},
                        success: function (json) {
                            bootbox.alert("success.");     
                        },
                        error: function (xhr, errmsg, err) {
                            console.log('error');
                        }
                    });    
                        }
                    }
                }
            });
}

$(document).ready( function() {

    // // after a click action on the .list-group-item
    // $('#side-menu li').on('click',function(e){
    //     var previous = $('ul#side-menu').children(".active");
    //     previous.removeClass('active'); // previous list-item
    //     $(this).addClass('active'); // activated list-item
    //     // $(previous.attr("href")).attr('style','display:none'); // hide the content of the previous panel
    //     // $($(this).attr("href")).removeAttr('style'); // display the content
    //     return false;
    // });

    // $('#function-menu li.overview').on('click',function(e){
    //     $.get( "/profile-overview/"+$(".profile-main").attr("user"), function( data ) {
    //         $("#profile-right-bottom").html(data);
    //     });
    // });
    

    $('#side-menu li a.first').on('click',function(e){
        $.get( "/profile-analysis/"+$(".profile-main").attr("user"), function( data ) {
            $("#page-wrapper .row .col-lg-12").html(data);
            $.post( "/language/"+$(".profile-main").attr("user"), function( data2 ) {
                $(".tab-content").html(data2);  
            }); 
        });
        return false;
    });

    $('#side-menu li a.second').on('click',function(e){
        $.get( "/profile-analysis/"+$(".profile-main").attr("user"), function( data ) {
            $("#page-wrapper .row .col-lg-12").html(data);
            $("#analysis-title").html("Code Style");
            $.post( "/sex/"+$(".profile-main").attr("user"), function( data2 ) {
                $(".tab-content").html(data2);  
            }); 
        });
        return false;
    });

    $('#side-menu li a.third').on('click',function(e){
        $.get( "/profile-analysis/"+$(".profile-main").attr("user"), function( data ) {
            $("#page-wrapper .row .col-lg-12").html(data);
            $("#analysis-title").html("Day & Hour");
            $.post( "/day_hour/"+$(".profile-main").attr("user"), function( data2 ) {
                $(".tab-content").html(data2);  
            }); 
        });
        return false;
    });

    // $('#function-menu li.project').on('click',function(e){
    //     $("#profile-right-bottom").html("");
    // });

    // $('#function-menu li.friends').on('click',function(e){
    //     $("#profile-right-bottom").html("");
    // });

    // $('#face-edit-row #friend').on('click',function(e){
    //     $(this).attr('id', 'unfriend');
    //     if ($(this).html() === "Add Friend") {
    //         $(this).html("Unfriend");
    //     } else {
    //         $(this).html("Add friend");
    //     };
        
    // });

    $('button.github').on("click", function(event) {
        var host = window.location.hostname;
        var port = window.location.port;
        window.location.replace('https://github.com/login/oauth/authorize?client_id=9cb96333069fb96e1196&redirect_uri=http://'
         + host + ':' + port + '/profile/' + $(".profile-main").attr("user"));
    });
});