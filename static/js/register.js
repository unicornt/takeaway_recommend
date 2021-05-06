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
                window.location.href='/email_sent';
            }
            else if(data.status == 'error'){
                // alert(data.type);
                $("#badregister").text(data.type);
                $("#badregister").css({'visibility': 'visible'});
                console.log('error');
            }
        },
        error:function(e){
            console.log("error");
        }
    });
}