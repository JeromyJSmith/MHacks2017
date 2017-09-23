$(document).ready(function() {


    $("#login-button").click(function(event){
        console.log("submitting login form")
        event.preventDefault();

      $('form').fadeOut(500);
      $('.wrapper').addClass('form-success');

    });


});