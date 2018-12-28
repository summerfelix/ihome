function logout() {
    $.get("/user/logout/", function(data){
        if (0 == data.errno) {
            location.href = "/user/login/";
        }
    })
}

$(document).ready(function(){
})