function get_recommend(rid){
    var url = "recommend/get_recommend/?" + rid;
    console.log(url);
    $.ajax({
        url: url,
        type: "POST",
        contentType: false,
        processData: false,
        async : false,
        success:function(data){
            console.log(url);
            //$("#img1").src = 
        },
        error:function(data){
            console.log("get_recommend error");
        }
    });
}