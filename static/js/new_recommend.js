function upload_recommend(textElement, url) {
    console.log(textElement[0]);
    var text = textElement[0].value;
    console.log(text);
    var formData = new FormData();
    formData.append("text", text);
    $.ajax({
        url:url,
        type:"POST",
        data: formData,
        dataType: "json",
        contentType: false,
        processData: false,
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
    });
}