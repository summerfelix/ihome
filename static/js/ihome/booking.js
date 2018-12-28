function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });

    var search_url = location.search;
    var house_id = search_url.split('=')[1];
    $.ajax({
        url: '/order/booking_house/' + house_id,
        type: 'GET',
        dataType: 'JSON',
        success: function (data) {
            if(data['code'] == 200){
                $('#house-id').val(data['house']['id']);
                $('.house-info').append(
                    $('<img>').attr('src', '/static/media/' + data['house']['images']),
                    $('<div>').attr('class', 'house-text').append(
                        $('<h3>').text(data['house']['title']),
                        $('<p>').html('￥<span>' + data['house']['price'] + '</span>/晚')
                    )
                )
            }
        },
        error: function (data) {
            alert('失败')
        }
    })
})

$('.submit-btn').on('click', function () {
    var house_id = $('#house-id').val();
    var sd = $('#start-date').val();
    var ed = $('#end-date').val();
    if(house_id && sd && ed){
        $.ajax({
            url: '/order/create_order/',
            type: 'POST',
            dataType: 'JSON',
            data: {
                'house_id': house_id,
                'sd': sd,
                'ed': ed
            },
            success: function (data) {
                if (data['code'] == 1014) {
                    $('.popup p').text('还没有登录，先去登录吧');
                    showErrorMsg();
                }else if(data['code'] == 1016){
                    $('.popup p').text('日期填写有误');
                    showErrorMsg();
                } else if(data['code'] == 1017){
                    $('.popup p').text('预定天数超过限住天数');
                    showErrorMsg();
                } else{
                    window.location.href = '/order/orders/';
                }

            },
            error: function (data) {

            }

        })
    }else{
        showErrorMsg();
    }
})
