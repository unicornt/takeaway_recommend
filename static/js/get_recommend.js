function get_recommend(rid){
    var url = "recommend/get_recommend/?id=" + rid;
    console.log(url);
    $.ajax({
        url: url,
        type: "GET",
        contentType: false,
        processData: false,
        async : false,
        success:function(data){
            retData = data.content;
            console.log(retData.title);
            console.log(retData.text);
            console.log(retData.pic_url);
            var src = "\{\% static \"{url}\" \%\}";
            console.log(src);
            src = src.format({url:retData.pic_url[0]});
            console.log(src);
            $("#img1").attr('src',  src); 
        },
        error:function(data){
            console.log("get_recommend error");
        }
    });
}