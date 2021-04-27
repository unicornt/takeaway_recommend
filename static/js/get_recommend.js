/*
    可以用recommend_pic中的photo_url函数得到图片实体的url
    用这个url放进img元素的src属性中，会发送一个GET请求，django中的serve函数会进行处理
*/
function get_recommend_by_rid(rid){
    var url = "/recommend/get_recommend/?id=" + rid;
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
            console.log(retData.piclist);
            var piclist = JSON.parse(retData.piclist);
            console.log(retData.picnum);
            //var src = "\{\% static \"{" + url+ "}\" \%\}";
            var src = "/media/recommend/2021-04-27-113302-0.bmp";
            console.log(src);
            $("#img1").attr('src',  src); 
        },
        error:function(data){
            console.log("get_recommend error");
        }
    });
}

function get_recommend_by_usr(username){
    var formData = new FormData();
    formData.append("username", username);
    console.log(username);
    $.ajax({
        url: "/recommend/user_recommend",
        type: "POST",
        contentType: false,
        processData: false,
        async: false,
        data: formData,
        success:function(data){
            console.log(data.content);
            console.log(typeof(data.content));
            /*
                自己上localhost:8000/test上跑一下就知道格式了
            */
        },
    });
}

