//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    $(".order-comment").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-comment").attr("order-id", orderId);
    });
    
    $.ajax({
        url: '/order/my_orders/',
        type: 'GET',
        dataType: 'JSON',
        success: function (data) {
            if(data['code'] == 1018){
                 $('.orders-list').append(
                        $('<li>').attr('order-id', '').append(
                            $('<span>').text('您还没有订单哦！')
                        )
                 )
            }else{
                $.each(data, function (index, order) {
                    $('.orders-list').append(
                        $('<li>').attr('order-id', '').append(
                            $('<div>').attr('class', 'order-title').append(
                                $('<h3>').html('订单编号：' + order['order_id']),
                                $('<div>').attr('class', 'fr order-operate').append(
                                    $('<button>').attr('type', 'button').attr('class', 'btn btn-success order-comment').attr('data-toggle', 'modal').attr(
                                        'data-target', '#comment-modal'
                                    ).text('发表评价').attr('onclick', 'comment(' + order['order_id'] + ')')
                                ).css('display', 'none').attr('id', 'operate' + order['order_id'])
                            ),
                            $('<div>').attr('class', 'order-content').append(
                                $('<img>').attr('src', '/static/media/' + order['images']),
                                $('<div>').attr('class', 'order-text').append(
                                    $('<h3>').text('订单'),
                                    $('<ul>').append(
                                        $('<li>').html('创建时间：' + order['create_date']),
                                        $('<li>').html('入住日期：' + order['begin_date']),
                                        $('<li>').html('离开日期：' + order['end_date']),
                                        $('<li>').html('合计金额：' + order['amount'] + '元(共' + order['days'] + '晚)'),
                                        $('<li>').html('订单状态：' + '<span>' + order['status'] + '</span>'),
                                        $('<li>').html('我的评价：<span id="comment' + order['order_id'] + '"></span>'),
                                        $('<li>').html('拒单原因：<span id="reject-reason' + order['order_id'] + '"></span>')
                                    )
                                )
                            )
                        )
                    );
                    if(order['status'] == '待评价'){
                        $('#operate' + order['order_id']).css('display', 'block');
                    }

                    if(order['status'] == '已拒单'){
                        if(order['comment'] != null){
                            $('#reject-reason' + order['order_id']).text(order['comment']);
                        }
                    }else{
                        if(order['comment'] != null){
                            $('#comment' + order['order_id']).text(order['comment']);
                        }
                    }

                });
            }
        },
        error: function (data) {
        }
    })
    
});

// $(".modal-comment").on('click', function () {
//     var oid = $()
//     $.ajax({
//         url: '/order/comment/',
//     })
// })

function comment(id) {
    $('.modal-comment').on('click', function () {
        var content = $('#comment').val();
        $.ajax({
            url: '/order/comment/',
            type: 'POST',
            dataType: 'JSON',
            data: {
                'id': id,
                'content': content
            },
            success: function (data) {
                if(data['code'] == 200){
                    location.reload();
                }
            },
            error: function (data) {

            }
        })
    })
}