function loadImg(files, imgbox){
    var file = files[0];
    var reader = new FileReader();
    var imgFile;
    reader.onload=function(e){
        imgFile = e.target.result;
        console.log(imgFile);
        imgbox.attr('src', imgFile);
    }
    reader.readAsDataURL(file);
}

function upload_pic(divname, url){
    var formData = new FormData();
    var piclist = $("div#"+divname).find("input");//piclist中包含所有divname下的input元素
    formData.append("usr", "test");
    var check = true;
    for (var i = 0; i < piclist.length; ++i){
        var p = piclist[i];
        if (p.type != "file" || p.value == "")
            continue;
        pic = p.files[0];
        check = false;
        //var size = pic.size;
        formData.append("piclist", pic);
    }
    if (check)
        alert("请选择文件！");
    
    $.ajax({
        url:url,
        type:"POST",
        dataType:"json",
        contentType: false,
        processData: false,
        data: formData,
        complete:function(data){
            console.log("complete");
        },
        success:function(data){
            console.log("success");
        },
        error:function(e){
            console.log("error");
        }
    })
}