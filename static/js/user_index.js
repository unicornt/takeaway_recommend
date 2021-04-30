$(document).ready(function () {
    var username = getCookie('username');
    var data = get_recommend_by_usr(username);
    for(var val in data) {
        console.log(data);
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
            '                            <h3 class="card-text">店铺名-美食</h3>\n' +
            '                            <p class="card-text">介绍</p>\n' +
            '                            <div class="d-flex justify-content-between align-items-center">\n' +
            '                                <div class="btn-group">\n' +
            '                                    <a href="/show_recommend"><button type="button" class="btn btn-sm btn-outline-secondary">更多</button></a>\n' +
            '                                    <button type="button" class="btn btn-sm btn-outline-secondary">编辑</button>\n' +
            '                                    <button type="button" class="btn btn-sm btn-danger">删除</button>\n' +
            '                                </div>\n' +
            '                                <small class="text-muted">点击量</small>\n' +
            '                            </div>\n' +
            '                        </div>\n' +
            '                    </div>\n' +
            '                </div>');
        num += 1;
    }
});