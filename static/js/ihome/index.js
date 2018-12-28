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

function setStartDate() {
    var startDate = $("#start-date-input").val();
    if (startDate) {
        $(".search-btn").attr("start-date", startDate);
        $("#start-date-btn").html(startDate);
        $("#end-date").datepicker("destroy");
        $("#end-date-btn").html("离开日期");
        $("#end-date-input").val("");
        $(".search-btn").attr("end-date", "");
        $("#end-date").datepicker({
            language: "zh-CN",
            keyboardNavigation: false,
            startDate: startDate,
            format: "yyyy-mm-dd"
        });
        $("#end-date").on("changeDate", function() {
            $("#end-date-input").val(
                $(this).datepicker("getFormattedDate")
            );
        });
        $(".end-date").show();
    }
    $("#start-date-modal").modal("hide");
}

function setEndDate() {
    var endDate = $("#end-date-input").val();
    if (endDate) {
        $(".search-btn").attr("end-date", endDate);
        $("#end-date-btn").html(endDate);
    }
    $("#end-date-modal").modal("hide");
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){});
        },1000)
    });
}

function goToSearchPage(th) {
    var url = "/house/search/?";
    var aid = $(th).attr("area-id");
    var areaName = $(th).attr("area-name");
    var sd = $(th).attr("start-date");
    var ed = $(th).attr("end-date");
    if(aid && areaName && sd && ed){
        url += ("aid=" + aid);
        url += "&";
        if (undefined == areaName) areaName="";
        url += ("aname=" + areaName);
        url += "&";
        url += ("sd=" + sd);
        url += "&";
        url += ("ed=" + ed);
        location.href = url;
    }else{
        showErrorMsg();
    }

}

$(document).ready(function(){
    $(".top-bar>.register-login").show();

    var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationClickable: true
    });

    $(".area-list a").click(function(e){
        $("#area-btn").html($(this).html());
        $(".search-btn").attr("area-id", $(this).attr("area-id"));
        $(".search-btn").attr("area-name", $(this).html());
        $("#area-modal").modal("hide");
    });
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);               //当窗口大小变化的时候
    $("#start-date").datepicker({
        language: "zh-CN",
        keyboardNavigation: false,
        startDate: "today",
        format: "yyyy-mm-dd"
    });
    $("#start-date").on("changeDate", function() {
        var date = $(this).datepicker("getFormattedDate");
        $("#start-date-input").val(date);
    });

    $.ajax({
        url: '/house/get_area/',
        type: 'GET',
        dataType: 'JSON',
        success: function (data) {
            $.each(data, function (index, area) {
                $('.area-list').append(
                    $('<a>').attr('href', '#').attr('area-id', index).text(area)
                )
            });
            $(".area-list a").click(function(e){
                $("#area-btn").html($(this).html());
                $(".search-btn").attr("area-id", $(this).attr("area-id"));
                $(".search-btn").attr("area-name", $(this).html());
                $("#area-modal").modal("hide");
            });
        },
        error: function (data) {

        }
    });

    $.ajax({
        url: '/house/login_status/',
        type: 'GET',
        dataType: 'JSON',
        success: function (data) {
            if(data['code'] == 1013){
                $('.register-login').hide();
                if(data['username']){
                    $('.user-name').text(data['username']);
                }else{
                    $('.user-name').text(data['phone']);
                }

                $('.user-info').show();
            }else if(data['code'] == 1014){
                $('.register-login').show();
                $('.user-info').hide();
            }
        },
        error: function (data) {
        }
    });


    $.ajax({
        url: '/house/swiper/',
        type: 'GET',
        dataType: 'JSON',
        success: function (data) {
            $.each(data['house'], function (index, house) {
                // console.log(house);
                $('.swiper-wrapper').append(
                    $('<div>').attr('class', 'swiper-slide').append(
                        $("<a>").attr('href', '/house/detail/?house_id=' + house['id']).append(
                            $('<img>').attr('src', '/static/media/' + house['images'])
                        ),
                        $('<div>').attr('class', 'slide-title').text(house['title'])
                    )
                )
            })
        },
        error: function (data) {
        }
    })

    var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationClickable: true
    });


})