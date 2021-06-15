function search(data, sentense){
    var word_list = word_separate(sentense);  
    var list = Array();
    var N = 0;
    for(var r in data) {
        list.push(r);
        N++;
    }
    for(var i = 0; i < N; i++){
        for(var j = i + 1; j < N; j++){
            if (match_cmp(data[list[j]].text + data[list[j]].title, data[list[i]].text + data[list[i]].title, sentense, word_list)){
                var tmp = list[i];
                list[i] = list[j];
                list[j] = tmp;
            }
        }
    }
    //console.log(list);
    return list;
}

function word_separate(sentense){
    console.log('word_separate sentense:', sentense);
    var word_list;
    var formData = new FormData();
    formData.append('sentense', sentense);
    $.ajax({
        url: '/recommend/word_separate',
        type: "POST",
        contentType: false,
        processData: false,
        async : false,
        data: formData,
        success:function(data){
            word_list = data.content['word_list'];
        }
    });
    console.log(word_list);
    return word_list;
}

function word_count(s, word_list){
    var cnt = 0;
    var us = encodeURI(s);
    for (var word in word_list){
        word = encodeURI(word);
        if (us.match(word) != null)
            cnt = cnt + 1;
    }
    //if (cnt > 0)
        //console.log("word_count:", s, " ", word_list, " ", cnt);
    return cnt;
}

function match_cmp(a, b, sentense, word_list){
    var ua = encodeURI(a);
    var ub = encodeURI(b);
    sentense = encodeURI(sentense);
    var ra = ua.match(sentense);
    if (ra != null){
        console.log(ra);
        console.log(a);
    }
    
    var rb = ub.match(sentense);
    if (ra != null && rb != null)
        return false;
    if (ra != null && rb == null)
        return true;
    if (ra == null && rb != null)
        return false;
    var cnt_a = word_count(a, word_list);
    var cnt_b = word_count(b, word_list);
    return (cnt_a > cnt_b);
}