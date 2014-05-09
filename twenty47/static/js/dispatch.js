$(document).ready(function() {
    $('.btn').button()


    $('#incidentTime').AnyTime_picker({
      format: "%Y-%m-%d %T",
      askSecond: false,
    });
    
   
    // GETS THE CSRF TOKEN SO THAT AJAX FORMS WORK start
    var csrftoken = $('meta[name=csrf-token]').attr('content')
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })
    // GETS THE CSRF TOKEN SO THAT AJAX FORMS WORK end
    
    // FOR THE ADMIN LIST VIEW start
    $('.btn-status-none').click(function () {
        var btn = $(this);
        if ( post_user_status_update(btn.data( "user" ), btn.data( "page" ), { action: "none" })  ){
            $("#glyph-status-none-" + btn.data( "user" )).addClass("glyphicon glyphicon-check")
            $("#glyph-status-denied-" + btn.data( "user" )).removeClass("glyphicon glyphicon-check")
            $("#glyph-status-pending-" + btn.data( "user" )).removeClass("glyphicon glyphicon-check")
            $("#glyph-status-approved-" + btn.data( "user" )).removeClass("glyphicon glyphicon-check")
        }
    });
    $('.btn-status-denied').click(function () {
        var btn = $(this);
        if ( post_user_status_update(btn.data( "user" ), btn.data( "page" ), { action: "denied" }) ){
            $("#glyph-status-none-" + btn.data( "user" )).removeClass("glyphicon glyphicon-check")
            $("#glyph-status-denied-" + btn.data( "user" )).addClass("glyphicon glyphicon-check")
            $("#glyph-status-pending-" + btn.data( "user" )).removeClass("glyphicon glyphicon-check")
            $("#glyph-status-approved-" + btn.data( "user" )).removeClass("glyphicon glyphicon-check")
        }
    });
    $('.btn-status-pending').click(function () {
        var btn = $(this);
        if ( post_user_status_update(btn.data( "user" ), btn.data( "page" ), { action: "pending" }) ){
            $("#glyph-status-none-" + btn.data( "user" )).removeClass("glyphicon glyphicon-check")
            $("#glyph-status-denied-" + btn.data( "user" )).removeClass("glyphicon glyphicon-check")
            $("#glyph-status-pending-" + btn.data( "user" )).addClass("glyphicon glyphicon-check")
            $("#glyph-status-approved-" + btn.data( "user" )).removeClass("glyphicon glyphicon-check")
        }
    });
    $('.btn-status-approved').click(function () {
        var btn = $(this);
        if ( post_user_status_update(btn.data( "user" ), btn.data( "page" ), { action: "approved" }) ){
            $("#glyph-status-none-" + btn.data( "user" )).removeClass("glyphicon glyphicon-check")
            $("#glyph-status-denied-" + btn.data( "user" )).removeClass("glyphicon glyphicon-check")
            $("#glyph-status-pending-" + btn.data( "user" )).removeClass("glyphicon glyphicon-check")
            $("#glyph-status-approved-" + btn.data( "user" )).addClass("glyphicon glyphicon-check")
        }
    });
    $('.btn-deactivate').click(function () {
        var btn = $(this);
        if ( post_user_status_update(btn.data( "user" ), btn.data( "page" ), { action: "deactivate" }) ){
            $("#btn-activate-" + btn.data( "user" )).removeClass("hide")
            $("#btn-deactivate-" + btn.data( "user" )).addClass("hide")
        }
    });
    $('.btn-activate').click(function () {  
        var btn = $(this);
        if ( post_user_status_update(btn.data( "user" ), btn.data( "page" ), { action: "activate" }) ){
            $("#btn-deactivate-" + btn.data( "user" )).removeClass("hide")
            $("#btn-activate-" + btn.data( "user" )).addClass("hide")
        }
    });
    // FOR THE ADMIN LIST VIEW end

})

function post_user_status_update(userid, submit_to, form_data) {
    var success = false;
    console.log(submit_to);
    console.log(form_data);
    success = $.post( submit_to, form_data, function(return_value) {
        console.log(return_value);
        if (return_value == "True"){
            return true;
        }
        alert(return_value);
        return false;
    });
    return success;
};
