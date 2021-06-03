$(document).ready(function () {
    var username = getCookie('username');
    var data = get_recommend_by_usr(username);
    myRender(data);
});
var retdata;
function sortAndRender(sortkey, order){
    var username = getCookie('username');
    var formData = new FormData();
    formData.append('is_all', '1');
    formData.append('type', sortkey);
    formData.append('user', 'admin');
    formData.append('order', order);
    console.log(typeof(sortkey));
    console.log(sortkey);
    $.ajax({
        url : "/recommend/sort",
        type : "POST",
        data : formData,
        dataType: "json",
        contentType: false,
        processData: false,
        async: false,
        success: function(data){
            retdata = data.content;
        },
    });
    myRender(retdata);
}

function mySort(type){
    $('show_container').empty();
    if(type == 0) {
        // sort with upload time
        for(var val in retdata){
            for(var val2 in retdata){
                if(val2 > val && retdata[val].timeRange > retdata[val2].timeRange) {
                    var tmp = retdata[val];
                    retdata[val] = retdata[val2];
                    retdata[val2] = tmp;
                }
            }
        }
    }
    else {
        for(var val2 in retdata){
            if(val2 > val && retdata[val].like > retdata[val2].like) {
                var tmp = retdata[val];
                retdata[val] = retdata[val2];
                retdata[val2] = tmp;
            }
        }
    }
    myRender(retdata);
}

function myRender(data){
    for(var val in data) {
        console.log(val);
        console.log(data[val].piclist);
        var num = 1
        var rown = 0
        var piclist = JSON.parse(data[val].piclist);
        var picsrc = piclist['0'];
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
            '                            <h3 class="card-text">' + data[val].title + '</h3>\n' +
            '                            <p class="card-text limit-line">' + data[val].text + '</p>\n' +
            '                            <div class="d-flex justify-content-between align-items-center">\n' +
            '                                <div class="btn-group">\n' +
            '                                    <a href="/show_recommend?rid=' + data[val].rid + '"><button type="button" class="btn btn-sm btn-outline-secondary">更多</button></a>\n' +
            '                                    <button type="button" class="btn btn-sm btn-outline-secondary">编辑</button>\n' +
            '                                    <button type="button" class="btn btn-sm btn-danger" onclick="delete_recommend(\'' + val +'\')">删除</button>\n' +
            '                                </div>\n' +
            '                                <small class="text-muted" id="click_number">'+ data[val].like.toString() +'</small>\n' +
            '                            </div>\n' +
            '                        </div>\n' +
            '                    </div>\n' +
            '                </div>');
        num += 1;
    }
}
