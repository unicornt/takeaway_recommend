function get_edit_index(recommend_id) {
    var url = "/recommend/edit_recommend/?key=" + recommend_id;
    $.get(url);
}

function delete_recommend(recommend_id) {
    console.log(recommend_id);
    $.ajax({
        url: "/recommend/delete_recommend/?key=" + recommend_id,
        type: "GET",
        contentType: false,
        processData: false,
        async : false,
        success:function (data) {
            alert("删除成功");
            window.location.href='/user_index';
        },
        error:function(data){
            console.log("get_recommend error");
        }
    });
}

function update_recommend(recommend_id, titie, text, picdiv){
    var formData = new FormData();
    var piclist = $("div#" + picdiv).find("input");//piclist中包含所有divname下的input元素
    var check = true;
    for (var i = 0; i < piclist.length; ++i) {
        var p = piclist[i];
        if (p.type != "file" || p.value == "")
            continue;
        pic = p.files[0];
        check = false;
        //var size = pic.size;
        formData.append("picture", pic);
    }

    formData.append('key', recommend_id);
    formData.append('title', title);
    formData.append('text', text);
    console.log(text);
    $.ajax({
        url: "recommend/update_recommend",
        type: "POST",
        dataType: "json",
        contentType: false,
        processData: false,
        async: false,
        data: formData,
        success: function (data) {
            // console.log("create recommend 1 success");
            // console.log(String(data.content.key));
            alert("提交成功");
            window.location.href='/user_index';
        },
        error: function (data) {
            console.log("error");
            alert("提交出现错误，请重新提交");
        }
    });
}