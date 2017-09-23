$(document).ready(function() {


    $("#login-button").click(function(event){
        console.log("submitting login form")
        event.preventDefault();

        $('form').fadeOut(500);
        $('.wrapper').addClass('form-success');

        //AJAX CALL TO LOGIN, response is RESPONSE

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

    $("#sign-up-button").click(function(event){
        console.log("submitting sign up form")
        event.preventDefault();

        $('form').fadeOut(500);
        $('.wrapper').addClass('form-success');

        //AJAX CALL TO CREATE ACCOUNT, response is RESPONSE

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