function Logout() {
    $.ajax({
        url:"/login/log_out",
        type:"POST",
        data: {
        },
        dataType: "json",
        complete:function(data){
            console.log("complete");
        },
        success:function(data){
            console.log("success");
            console.log(data.status, data.type);
            if(data.status == 'ok') {
                document.cookie = "username=; ";
                window.location.href='/';
            }
            else if(data.status == 'error'){
                console.log('error');
                $('#badlogin').css({'visibility': 'visible'});
            }
        },
        error:function(e){
            console.log("error");
        }
    });
}

$(document).ready(function () {
    console.log(document.cookie);
    var userName = getCookie("username");
    var doc = '';
    if (userName != "") {
        doc += '<ul class="nav navbar-nav navbar-right">\n' +
                    '<li class="dropdown">' +
                        '<a href="#" class="dropdown-toggle" data-toggle="dropdown">\n' +
                        userName +
                        '<b class="caret"></b>\n' +
                        '</a>\n' +
                        '<ul class="dropdown-menu">\n' +
                            '<li><a href="/new_recommend">上传推荐</a></li>\n' +
                            '<li class="divider"></li>\n' +
                            '<li><a onclick="Logout()">登出</a></li>\n' +
                        '</ul>' +
                    '</li>' +
                 '</ul>';
    } else {
        doc += '<ul class="nav navbar-nav navbar-right">\n' +
            '<li><a href="login">登录</a></li>\n' +
            '</ul>';
    }
    $("#navbar").append(doc);
});

