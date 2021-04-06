function checkRegister() {
    var usr = $("#ecode").val()
    console.log(usr);
    $.ajax({
        url:"/login/register",
        type:"POST",
        data: {
            usr:$("#usr").val(),
            pwd: $("#pwd").val(),
            email: $("#email").val()
        },
        dataType: "json",
        complete:function(data){
            console.log("complete");
        },
        success:function(data){
            console.log("success");
            if(data.status == 'ok') {
                window.location.href='/';
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
