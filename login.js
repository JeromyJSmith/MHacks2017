$(document).ready(function() {


    $("#login-button").click(function(event){
        console.log("submitting login form")
        event.preventDefault();

        $('form').fadeOut(500);
        $('.wrapper').addClass('form-success');
        var RESPONSE = true;
        if (RESPONSE == true) {
            //login success, wait for animation then go to account page
            setTimeout(function(){
                $(".container").fadeOut(1000);
                location.href = "account.html";
            }, 1000);
        } else {
            //login failed

        }
    });


});