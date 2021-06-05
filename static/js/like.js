function like(rid){
    var url = '/recommend/like/?rid=' + rid + '&otype=like';
    $.get(url);
}

function cancel_like(rid){
    var url = '/recommend/like/?rid=' + rid + '&otype=cancel';
    $.get(url);
}

function is_like(rid){
    var result = false;
    var url = '/recommend/check_like/?rid=' + rid;
    $.ajax({
        url : url,
        type : "GET",
        async : false,
        success : function(data){
            console.log(data.content);
            if (data.content['result'] == 'YES')
                result = true;
        }
    });
    console.log(result);
    return result;
}