$(document).ready(function () {
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
                            '<li><a href="#">上传推荐</a></li>\n' +
                            '<li class="divider"></li>\n' +
                            '<li><a href="#">登出</a></li>\n' +
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