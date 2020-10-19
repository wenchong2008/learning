/**
 * Created by wenchong on 17/4/28.
 */


$(function () {

    //计算每个商品单价
    function checkSinglePrice(self){
            var price = $(self).find('.p-price span').text();
            var num = $(self).find('.p-quantity input').val();
            var prices = price*num;
            $(self).find('.p-num span').text(prices.toFixed(2));
    }
    // 先计算每一个商品的总价 = 数量 * 单价
    $('.item-single').each(function(){
        checkSinglePrice(this);
    });

    //默认商品全选，并计算总价格
    $(':checkbox').prop('checked', true);
    checkPrices();

    //计算已选择商品的总价
    function checkPrices(){
        var totalPrice = 0;
        $('.item-list').find(':checkbox').each(function(){
            if($(this).prop('checked')){
                v = $(this).parent().siblings('.p-num').children('span').text();
                console.log(v);
                totalPrice = parseFloat(totalPrice) + parseFloat(v);
            }
            $('.total-price span').text(totalPrice.toFixed(2))
        })
    }

    //全选标签绑定计算总价
    var allCheckBox = $('.t-checkbox').children('input');
    allCheckBox.on('click',function(){
        if(allCheckBox.prop('checked')){
            $('.item-list').find(':checkbox').prop('checked',true);
        }else{
            $('.item-list').find(':checkbox').prop('checked',false);
        }
        checkPrices()
    });

    //为商品单选时绑定事件
    $('.item-list').find(':checkbox').click(function(){
        checkPrices();
    });

    // 为 - 号绑定事件，变更时重新计算单价和总价
    $('.s-l').on('click',function(){
        var num = $(this).siblings('input').val();
        if(num <= '0'){
            $(this).siblings('input').val(1);
        }else{
            $(this).siblings('input').val(num-1);
        }
        checkSinglePrice($(this).parent().parent()[0]);
        checkPrices()
    });

    // 为 + 号绑定事件，变更时重新计算单价和总价
    $('.s-r').on('click',function(){
        var num = $(this).siblings('input').val();
        $(this).siblings('input').val(parseInt(num)+1);
        checkSinglePrice($(this).parent().parent()[0]);
        checkPrices()
    });


    // 为 input 标签绑定事件，变更时重新计算单价和总价
    $('.p-quantity input').on('blur',function(){
        var num = $(this).val();
        num = parseInt(num);
        if(num) {
            if (num < '0') {
                $(this).val(1);
            }else{
                $(this).val(num);
            }
        }else{
            $(this).val(1);
        }
        checkSinglePrice($(this).parent().parent()[0]);
        checkPrices()
    });

    //删除购物车
    $('.p-ops').click(function(){
        $(this).parent().remove();
        checkPrices()
    })

});