$(document).ready(function () {
    var username = getCookie('username');
    retdata_user = get_recommend_by_usr(username);
    N_user = 0;
    list_user = Array();
    for(var r in retdata_user) {
        list_user.push(r);
        N_user++;
    }
    myRender();
});
var retdata_user;
var list_user;
var N_user;

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
    var N = N_user;
    var list = list_user;
    var retdata = retdata_user;
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
    console.log("sort part finish");
    list_user = list;
    myRender();
}

function myRender(){
    $('#show_container').empty();
    var list = list_user;
    var N = N_user;
    var retdata = retdata_user;
    for(var i = 0; i < N; i++) {
        console.log(list[i], typeof(list[i]), retdata[list[i]]);
        var val = list[i];
        console.log(retdata[val].piclist);
        var num = 1
        var rown = 0
        var piclist = JSON.parse(retdata[val].piclist);
        var picsrc = piclist['1'];
        console.log(picsrc);
        if(num % 3 === 1) {
            rown += 1;
            $('#show_container').append('<div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3" id="show_row' + rown.toString() + '">\n' +
                '\n' +
                '</div>');
        }
        $('#show_row'+rown.toString()).append('<div class="col">\n' +
            '                    <div class="card shadow-sm">\n' +
            '                        <img src="'+ '/media/recommend/' + picsrc+'" class="card-img-top" alt="Header">\n' +
            '\n' +
            '                        <div class="card-body">\n' +
            '                            <h3 class="card-text">' + retdata[val].title + '</h3>\n' +
            '                            <p class="card-text limit-line">' + retdata[val].text + '</p>\n' +
            '                            <div class="d-flex justify-content-between align-items-center">\n' +
            '                                <div class="btn-group">\n' +
            '                                    <a href="/show_recommend?rid=' + retdata[val].rid + '"><button type="button" class="btn btn-sm btn-outline-secondary">更多</button></a>\n' +
            '                                    <button type="button" class="btn btn-sm btn-danger" onclick="delete_recommend(\'' + retdata[val].rid +'\')">删除</button>\n' +
            '                                </div>\n' +
            '                                <small class="text-muted" id="click_number">'+ retdata[val].like.toString() +'</small>\n' +
            '                            </div>\n' +
            '                        </div>\n' +
            '                    </div>\n' +
            '                </div>');
        num += 1;
    }
}
