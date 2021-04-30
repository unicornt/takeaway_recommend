function create_recommend1(title, text, picdiv) {
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

    formData.append('title', title);
    formData.append('text', text);
    console.log(text);
    $.ajax({
        url: "recommend/new_recommend",
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

function loadImg(file, imgbox){
    var reader = new FileReader();
    var imgFile;
    reader.onload=function(e){
        imgFile = e.target.result;
        //console.log(imgFile);
        imgbox.attr('src', imgFile);
    }
    reader.readAsDataURL(file);
}