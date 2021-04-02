console.log("script");
$(document).ready(function () {
    alert("OK!");
    var userName = getCookie("username");
    var doc = '';
    if (userName != "") {
        doc += '<ul class="nav navbar-nav navbar-right">\n' +
            '<li><a>' + userName + '</a></li>\n' +
            '</ul>';
    } else {
        doc += '<ul class="nav navbar-nav navbar-right">\n' +
            '<li><a href="login">登陆</a></li>\n' +
            '</ul>';
    }
    $("#navbar").append(doc);
});