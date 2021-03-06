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
            '          <a class="dropdown-item" href="/like_index">我的赞</a>\n' +
            '          <div class="dropdown-divider"></div>\n' +
            '          <a class="dropdown-item" onclick="Logout()">登出</a>\n' +
            '        </div>\n' +
            '      </li>' +
            '</ul>';
    } else {
        doc += '<ul class="nav navbar-nav navbar-right">\n' +
            '<li class="nav-item">' +
                '<a class="nav-link" href="login" id="login-button">登录</a></li>\n' +
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
    
    retdata_index = get_all_recommend();
    console.log(retdata_index);
    N_index = 0;
    list_index = Array();
    for(var r in retdata_index) {
        list_index.push(r);
        N_index++;
    }
    myRender();

    var recommend_data = do_recommended();
    console.log('recommend_data');
    console.log(recommend_data);
    for (var i = 1; i <= 3; ++i){
        var si = String(i);
        var item = recommend_data[si];
        var piclist = JSON.parse(item.piclist);
        var picsrc = piclist['1'];
        $('#recommend_img_'+si).attr('src', '/media/recommend/'+ picsrc);
        $('#recommend_title_'+si).html(item['title']);
        $('#recommend_text_'+si).html(item['text']);
        $('#recommend_href_'+si).attr('href', '/show_recommend?rid='+item['rid']);
    }
});

var retdata_index;
var list_index;
var N_index;

function cmp(a, b){
    aS = a.split('-')
    bS = b.split('-')
    for(var i=0; i < aS.length; i++) {
        if(parseInt(aS[i]) < parseInt(bS[i])){
            console.log('compare s', parseInt(aS[i]), parseInt(bS[i]));
            return 1
        }
        else if(parseInt(aS[i]) > parseInt(bS[i])){
            console.log('compare', parseInt(aS[i]), parseInt(bS[i]));
            return 0
        }
    }
    return 0
}

function mySort(type){
    var list = list_index;
    var retdata = retdata_index;
    var N = N_index;
    if(type == 0) {
        // sort with upload time
        console.log("sort with time");
        for(var i = 0; i < N; i++){
            for(var j = i + 1; j < N; j++){
                if(cmp(retdata[list[j]].rid, retdata[list[i]].rid)) {
                    console.log("exchange");
                    var tmp = list[i];
                    list[i] = list[j];
                    list[j] = tmp;
                }
            }
        }
    }
    else {
        console.log("sort with like");
        for(var i = 0; i < N; i++){
            for(var j = i + 1; j < N; j++){
                if(retdata[list[j]].like > retdata[list[i]].like) {
                    console.log("exchange");
                    var tmp = list[i];
                    list[i] = list[j];
                    list[j] = tmp;
                }
            }
        }
    }
    console.log("sort part finish")
    list_index = list;
    N_index = N;
    myRender();
}

function myRender(){
    $('#show_container').empty();
    var list = list_index;
    var retdata = retdata_index;
    var N = N_index;
    //console.log("recommend number:", N);
    for(var i = 0; i < N; i++) {
        var val = list[i];
        //console.log(retdata[val].piclist);
        var num = 1
        var rown = 0
        var piclist = JSON.parse(retdata[val].piclist);
        var picsrc = piclist['1'];
        //console.log(picsrc);
        if(num % 3 === 1) {
            rown += 1;
            $('#show_container').append('<div class="row row-cols-1 row-cols-sm-2 row-cols-md-3" id="show_row' + rown.toString() + '">\n' +
                '\n' +
                '</div>');
        }
        $('#show_row'+rown.toString()).append('<div class="col">\n' +
            '                    <div class="card shadow-sm">\n' +
            '                        <img src="'+ '/media/recommend/' + picsrc+'" aria-hidden="true" class="card-img-top top-img" alt="Header">\n' +
            '\n' +
            '                        <div class="card-body">\n' +
            '                            <h3 class="card-text">' + retdata[val].title + '</h3>\n' +
            '                            <p class="card-text limit-line">' + retdata[val].text + '</p>\n' +
            '                            <div class="d-flex justify-content-between align-items-center">\n' +
            '                                <div class="btn-group">\n' +
            '                                    <a href="/show_recommend?rid=' + retdata[val].rid + '"><button type="button" class="btn btn-sm btn-outline-secondary">更多</button></a>\n' +
            '                                </div>\n' +
            '                                <small class="text-muted" id="click_number">'+ retdata[val].like.toString() +'</small>\n' +
            '                            </div>\n' +
            '                        </div>\n' +
            '                    </div>\n' +
            '                </div>');
        num += 1;
    }
}

function do_search(sentense){
    list_index = search(retdata_index, sentense);
    console.log(list_index);
    myRender();
}
