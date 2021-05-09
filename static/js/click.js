function clickplus(rid){
    var url = '/recommend/click/?rid=' + rid;
    $.get(url);
}