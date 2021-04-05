function checkRegister() {
    var usr = $("#ecode").val()
    console.log(usr);
    $.ajax({
        url:"/login/email_validate",
        type:"POST",
        data: {
            ecode:$("#ecode").val(),

        },
        dataType: "json",
        complete:function(data){
            console.log("complete");
        },
        success:function(data){
            console.log("success");
            if(data.status == 'ok') {
                window.location.href='/confirm';
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