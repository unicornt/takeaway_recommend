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
    console.log(userName);
    var doc = '';
    if (userName != "") {
        console.log(userName);
        doc += '<ul class="navbar-nav navbar-right">' +
            '<li class="nav-item dropdown">\n' +
            '<a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="true" >\n' +
            userName +
            '</a>\n' +
            '        <div class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">\n' +
            '          <a class="dropdown-item" href="/new_recommend">提交测评</a>\n' +
            '          <a class="dropdown-item" href="/user_index">个人主页</a>\n' +
            '          <div class="dropdown-divider"></div>\n' +
            '          <a class="dropdown-item" onclick="Logout()">登出</a>\n' +
            '        </div>\n' +
            '      </li>' +
            '</ul>';
    } else {
        doc += '<ul class="nav navbar-nav navbar-right">\n' +
            '<li class="nav-item">' +
                '<a class="nav-link" href="login">登录</a></li>\n' +
            '</ul>';
    }
    $("#navbarSupportedContent").append(doc);

    var $win = $(window);
    var $backToTop = $('.js-back-to-top');
    // 当用户滚动到离顶部100像素时，展示回到顶部按钮
    $win.scroll(function() {
        if ($win.scrollTop() > 100) {
            $backToTop.show();
        } else {
            $backToTop.hide();
        }
    });
    // 当用户点击按钮时，通过动画效果返回头部
    $backToTop.click(function() {
        $('html, body').animate({
            scrollTop: 0
        }, 200);
    });
});
