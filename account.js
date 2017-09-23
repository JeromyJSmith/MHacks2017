$(document).ready(function() {

    $('.container').css('visibility','visible').hide().fadeIn(1000);

    $("#save-button").click(function(event){
        console.log("submitting login form")
        event.preventDefault();

        //AJAX CALL TO save, response is RESPONSE

        var RESPONSE = true;
        if (RESPONSE == true) {
            //save success, wait for animation then go to account page
            $(this).fadeTo(400, 0, function () {
                $(this).delay(400);
                $(this).html('Successful Save!');
                $(this).fadeTo(400, 1);
            });


            //$(this).text().fadeOut(500);
            //$(this).text("Successful Save!").fadeIn(500);
        } else {
            //save failed

        }
    });

    $(".attributes").click(function() {
        if ($("save-button").text() == "Successful Save!") {
            $("save-button").text().fadeOut(500);
            $("#save-button").text("Save").fadeIn(500);
        }
    });

});