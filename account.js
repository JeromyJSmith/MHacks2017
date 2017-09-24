$(document).ready(function() {

    $('.container').css('visibility','visible').hide().fadeIn(1000);

    $("#save-button").click(function(event){
        console.log("submitting login form")
        event.preventDefault();

        //AJAX CALL TO save, response is RESPONSE

        var RESPONSE = true;
        if (RESPONSE == true) {
            if ($(this).text() == "Save") {
                $(this).fadeTo(500, .1);
                setTimeout(function(){
                    $("#save-button").html('Successful Save!');
                    $("#save-button").fadeTo(500, 1);
                }, 500);
            }
        } else {
            //save failed
            $(this).html('Save failed');
        }
    });

    $("#attributes").click(function() {
        if ($("#save-button").text() == "Successful Save!") {
            $("#save-button").text("Save").fadeIn(500);
        }
    });

});