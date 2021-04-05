function checkRegister() {
    $.ajax({
        url:"/login/email_validate",
        type:"POST",
        data: {
            email:$("#email").val()
        },
        dataType: "json",
        complete:function(data){
            console.log("complete");
        },
        success:function(data){
            console.log("success");
            if(data.status == 'ok') {
                window.location.href='/w';
            }
            else if(data.status == 'error'){
                console.log('error');
            }
        },
        error:function(e){
            console.log("error");
        }
    });
}