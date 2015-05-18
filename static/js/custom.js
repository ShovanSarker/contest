/**
 * Created by shovan on 3/23/15.
 */
$(document).ready(function(){
    var modalMsg = '';
    var modalFoot = '';



    $('#btn-submit-from').click(function(e){
        var email = $('#email').val();
        var phone = $('#phone').val();
        var fblink = $('#fblink').val();
        if(email == '' && phone == '' && fblink == ''){
            e.preventDefault();
        }

    });


});