function create_recommend(title, text, picdiv){
    //console.log(url);
    $.ajax({
        url: "recommend/new_recommend",
        type: "POST",
        contentType: false,
        processData: false,
        async : false,
        success:function(data){
            console.log("create_recommend : " + data.key);
            upload_text(title, text, picdiv);
        },
        error:function(data){
            console.log("create_recommend error");
        }
    });
}

function create_recommend1(title, text, picdiv){
    var formData = new FormData();
    var piclist = $("div#"+picdiv).find("input");//piclist中包含所有divname下的input元素
    var check = true;
    for (var i = 0; i < piclist.length; ++i){
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
        async : false,
        data: formData,
        success:function(data){
            console.log("create recommend 1 success");
            console.log(String(data.content.key));
        },
        error:function(data){
            console.log("error");
        }
    });
}

function upload_text(title, text, picdiv){
    console.log(text);
    var formData = new FormData();
    formData.append('text', text);
    formData.append('title', title);
    $.ajax({
        url: "recommend/upload_recommend",
        type: "POST",
        dataType: "json",
        contentType: false,
        processData: false,
        async : false,
        data: formData,
        success:function(data){
            console.log("upload title and text success");
            upload_pic_indiv(picdiv);
        }
    });
}

function upload_pic_indiv(divname){
    var formData = new FormData();
    var piclist = $("div#"+divname).find("input");//piclist中包含所有divname下的input元素
console.log(piclist.length);
    var check = true;
    for (var i = 0; i < piclist.length; ++i){
        var p = piclist[i];
        if (p.type != "file" || p.value == "")
            continue;
        pic = p.files[0];
        check = false;
        //var size = pic.size;
        formData.append("picture", pic);
    }
    if (check)
        alert("请选择文件！");
    
    $.ajax({
        url: "recommend/recommend_addpic",
        type:"POST",
        dataType:"json",
        contentType: false,
        processData: false,
        async : false,
        data: formData,
        complete:function(data){
            console.log("complete");
        },
        success:function(data){
            console.log("success");
            $('.toast').toast('show');
            if(data.status == 'ok') {
                //console.log();
                //document.cookie='username='+$("#usr").val();
                //setTimeout(function (){window.location.href='/';}, 3000);
            }
            else if(data.status == 'error'){
                console.log('error');
                $('#badlogin').css({'visibility': 'visible'});
            }
        },
        error:function(e){
            console.log("error");
        }
    })
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