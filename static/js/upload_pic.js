function loadImg(files){
    var file = files[0];
    var reader = new FileReader();
    var imgFile;
    reader.onload=function(e){
        imgFile = e.target.result;
        console.log(imgFile);
        $("#imgContent").attr('src', imgFile);
    }
    reader.readAsDataURL(file);
}

function upload_pic(){
    var $file = $("#img").val();
    if ($file == ""){
        alert("请选择上传的目标文件");
    } 
    var fileType = $file.substring($file.lastIndexOf(".") + 1).toLowerCase();
    var size = $("#img")[0].files[0].size;
    console.log(fileType);
    console.log(size);
    var formData = new FormData();
    formData.append("usr", "test");
    formData.append("picture", $("#img")[0].files[0]);
    $.ajax({
        url:"/login/upload_pic",
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