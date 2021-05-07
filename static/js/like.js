function like(rid){
    var url = '/recommend/like/?rid=' + rid + '&otype=like';
    $.get(url);
}

function cancel_like(rid){
    var url = '/recommend/like/?rid=' + rid + '&otype=cancel';
    $.get(url);
}