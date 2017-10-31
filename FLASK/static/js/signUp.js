$(function() { 
    $('#btnSignUp').click(function() {
        console.log("This is working so far No 3");
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                var str1 = "/userHome/";
                var str2 = response;
                var path = str1.concat(str2);
                console.log(path);

                window.location = path;
            },
            error: function(error) {
                console.log(" Debug error in js");
            }
        });
    });
}); 