$(function(){
    function displayError(msg){
        $(".wrong-msg").html("&nbsp;<i class='fa fa-exclamation-triangle' aria-hidden='true'></i>&nbsp;" + msg).removeClass('hide');
    }
    $(":submit").on("click",function(){
        $(".wrong-msg").text("").addClass('hide');
        var username = $(":text").val();
        var password =$(":password").val();
        var msg;
        if ( username.length == 0 && password.length == 0){
            displayError("请输入用户名和密码!");
            return false;
        }else if(username.length == 0 && password.length != 0){
            displayError("请输入用户名!");
            return false;
        }else if(username.length != 0 && password.length == 0){
            displayError("请输入密码!");
            return false;
        }else{
            return true;
        }
   })
});