function search(data, keyword){
    
}

function similarity(s, t){
    
}

function match_cmp(a, b){
    aS = a.split('-')
    bS = b.split('-')
    for(var i=0; i < aS.length; i++) {
        if(parseInt(aS[i]) < parseInt(bS[i])){
            console.log('compare s', parseInt(aS[i]), parseInt(bS[i]));
            return 1
        }
        else if(parseInt(aS[i]) > parseInt(bS[i])){
            console.log('compare', parseInt(aS[i]), parseInt(bS[i]));
            return 0
        }
    }
    return 0
}