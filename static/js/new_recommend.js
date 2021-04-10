function upload_recommend() {
    $.ajax({
        url:"/login/upload",
        type:"POST",
        data: {
            usr:$("#usr").val(),
            pwd:$("#pwd").val()
        },
        dataType: "json",
        complete:function(data){
            console.log("complete");
        },
        success:function(data){
            console.log("success");
            if(data.status == 'ok') {
                document.cookie='username='+$("#usr").val();
                window.location.href='/';
            }
            else if(data.status == 'error'){
                console.log('error');
                $('#badlogin').css({'visibility': 'visible'});
            }
        },
        error:function(e){
            console.log("error");
        }
    });
}