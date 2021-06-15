function create_recommend1(title, text, picdiv, tag) {
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
    tag = tag.toString();
    console.log(tag.split(" - "));
    formData.append('timeRange', tag.split(" - ")[0].toString());
    formData.append('catalog', tag.split(" - ")[1].toString());
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

var imgFile = []; //文件流
var imgSrc = []; //图片路径
var imgName = []; //图片名字
$(function(){
	// 鼠标经过显示删除按钮
	$('.content-img-list').on('mouseover','.content-img-list-item',function(){
		$(this).children('a').removeClass('hide');
	});
	// 鼠标离开隐藏删除按钮
	$('.content-img-list').on('mouseleave','.content-img-list-item',function(){
		$(this).children('a').addClass('hide');
	});
	// 单个图片删除
	$(".content-img-list").on("click",'.content-img-list-item a',function(){
	    	var index = $(this).attr("index");
			imgSrc.splice(index, 1);
			imgFile.splice(index, 1);
			imgName.splice(index, 1);
			var boxId = ".content-img-list";
			addNewContent(boxId);
			if(imgSrc.length<4){//显示上传按钮
				$('.content-img .file').show();
			}
	  });
	//图片上传
	$('#upload').on('change',function(){			
		
		if(imgSrc.length>=4){
			return alert("最多只能上传4张图片");
		}

		var imgBox = '.content-img-list';
		var fileList = this.files;
		for(var i = 0; i < fileList.length; i++) {
			var imgSrcI = getObjectURL(fileList[i]);
			imgName.push(fileList[i].name);
			imgSrc.push(imgSrcI);
			imgFile.push(fileList[i]);
		}
		if(imgSrc.length==4){//隐藏上传按钮
			$('.content-img .file').hide();
		}
		addNewContent(imgBox);
		this.value = null;//解决无法上传相同图片的问题
	})

	//提交请求
    //$('#title').val(), $('#editor').val(), 'pic_div', vm.$data.tag
    $('#btn-submit-upload').on('click',function(){
        // FormData上传图片
        var formData = new FormData();
        $.each(imgFile, function(i, file){
            formData.append('picture', file);
        });

        formData.append('title', $('#title').val());
        formData.append('text', $('#editor').val());
        tag = vm.$data.tag;
        tag = tag.toString();
        console.log(tag.split(" - "));
        formData.append('timeRange', tag.split(" - ")[0].toString());
        formData.append('catalog', tag.split(" - ")[1].toString());
        $.ajax({
            url: "recommend/new_recommend",
            type: "POST",
            dataType: "json",
            contentType: false,
            processData: false,
            async: false,
            data: formData,
            complete: function(data) {
                console.log(formData);
            },
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
    });

});

//删除
function removeImg(obj, index) {
	imgSrc.splice(index, 1);
	imgFile.splice(index, 1);
	imgName.splice(index, 1);
	var boxId = ".content-img-list";
	addNewContent(boxId);
}

//图片展示
function addNewContent(obj) {
	// console.log(imgSrc)
	$(obj).html("");
	for(var a = 0; a < imgSrc.length; a++) {
		var oldBox = $(obj).html();
		$(obj).html(oldBox + '<li class="content-img-list-item"><img src="'+imgSrc[a]+'" alt=""><a index="'+a+'" class="hide delete-btn"><i class="ico-delete"></i></a></li>');
	}
}

//建立一個可存取到該file的url
function getObjectURL(file) {
	var url = null ;
	if (window.createObjectURL!=undefined) { // basic
		url = window.createObjectURL(file) ;
	} else if (window.URL!=undefined) { // mozilla(firefox)
		url = window.URL.createObjectURL(file) ;
	} else if (window.webkitURL!=undefined) { // webkit or chrome
		url = window.webkitURL.createObjectURL(file) ;
	}
	return url ;
}