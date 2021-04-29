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

function validate() {

    var pwd = $("#pwd").val();
    var pwd1 = $("#pwd2").val();
    <!-- 对比两次输入的密码 -->
    if(pwd == pwd1)
    {
        $("#messg").html("两次密码相同");
        $("#messg").css("color","green");
    }
    else {
        $("#messg").html("两次密码不相同");
        $("#messg").css("color","red")
        $("button").attr("disabled","disabled");
    }
}