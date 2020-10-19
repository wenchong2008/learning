/**
 * Created by wenchong on 17/4/28.
 */

$(function(){

    var values = [];

    $('.form-item').children('input').each(function() {
        var name = $(this).attr('name');
        var msg = $(this).attr('placeholder');
        var info = $(this).parent().next().children('span').text();
        values[name] = [msg,info]
    });

    $('.form-item').children('input').on('focus', function(){
        var name = $(this).attr('name');
        $(this).removeAttr('placeholder');
        $(this).parent().next().children('span').removeClass('hide').html(
            '<i class="fa fa-info-circle" aria-hidden="true"></i>'+values[name][1]
        ).removeClass('war');
    });
    $('.form-item').children('input').on('blur',function(){
        var name = $(this).attr('name');
        $(this).attr('placeholder',values[name][0]);
        $(this).parent().next().children('span').addClass('hide');
    });

    $(':submit').on('click', function () {
        $('.form-item').children('input').each(
            function () {
                if($(this).val().length == 0){
                    var v = $(this).parent().next().children('span').removeClass('hide').html(
                        '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i> 不能为空'
                    ).addClass('war');
                    return false
                }
            }
        );
        return false;
    })
});