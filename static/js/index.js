$(document).ready(function () {
    var userName = getCookie("username");
    var doc = '';
    userName = 'unicront';
    if (userName != "") {
        doc += '<ul class="nav navbar-nav navbar-right">\n' +
                    '<li class="dropdown">' +
                        '<a href="#" class="dropdown-toggle" data-toggle="dropdown">\n' +
                        userName +
                        '<b class="caret"></b>\n' +
                        '</a>\n' +
                        '<ul class="dropdown-menu">\n' +
                            '<li><a href="#">jmeter</a></li>\n' +
                            '<li><a href="#">EJB</a></li>\n' +
                            '<li><a href="#">Jasper Report</a></li>\n' +
                            '<li class="divider"></li>\n' +
                            '<li><a href="#">分离的链接</a></li>\n' +
                            '<li class="divider"></li>\n' +
                            '<li><a href="#">另一个分离的链接</a></li>\n' +
                        '</ul>' +
                    '</li>' +
                 '</ul>';
    } else {
        doc += '<ul class="nav navbar-nav navbar-right">\n' +
            '<li><a href="login">登陆</a></li>\n' +
            '</ul>';
    }
    $("#navbar").append(doc);
});