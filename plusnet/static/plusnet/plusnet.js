function getBill() {
    $.getJSON('/plusnet/bill/get', null, function(data) {
        console.log('done');
        console.log(data);
    });
}