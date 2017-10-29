$(function() { 
    $('#btnSignUp').click(function() {
        console.log("This is working so far No 2");
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                // window.location = '/display';
            },
            error: function(error) {
                console.log(" Debug error in js");
            }
        });
    });
}); 