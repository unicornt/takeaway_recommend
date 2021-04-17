function upload_recommend(title, text, picdiv){
    create_recommend("recommend/create_recommend");
    upload_text(title, text, "recommend/upload_recommend");
    upload_pic_indiv(picdiv, "");
}

function create_recommend(url){
    $.ajax({
        url: url,
        type: "POST",
        success:function(data){
            console.log("create_recommend : " + data.key);
        }
    });
}

function upload_text(title, text, url){
    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        contentType: false,
        processData: false,
        data:{
            title: title,
            text: text,
        },
        success:function(data){
            console.log("upload title and text success");
        }
    });
}

function upload_pic_indiv(divname, url){
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
            $('.toast').toast('show');
            if(data.status == 'ok') {
                //console.log();
                //document.cookie='username='+$("#usr").val();
                setTimeout(function (){window.location.href='/';}, 3000);
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
        console.log(imgFile);
        imgbox.attr('src', imgFile);
    }
    reader.readAsDataURL(file);
}