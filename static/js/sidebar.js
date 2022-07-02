$('.order-like').on('click', function(){
    $('.empty-reply').fadeOut();
    var result = $('.reply').sort(function(a,b){
        var A = parseInt($(a).attr('reply-like-count'));
        var B = parseInt($(b).attr('reply-like-count'));
        console.log(A, B);
        return (A < B) ? 1 : (A > B) ? -1 : 0;
    });
    $('.reply-lists').html(result);
});

$('.radio-position').click(function(){
    var type = $('.dropdown-toggle').text();
    var position = $(this).attr('value');

    search_position_type(position, type);
});

$('.dropdown-item').click(function(){
    var type = $(this).attr('value');
    var position = $('.radio-position:checked').attr('value');

    $('.dropdown-toggle').text(type);
    search_position_type(position, type);

});

function search_position_type(position, type) {
    reply_type_id = ["つぶやき", "根拠", "確認", "要求", "現状", "その他"]
    
    $('.reply').fadeOut();
    var type_class = '';
    if ($.inArray(type, reply_type_id) != -1) {
        type_class = '.type-' + String($.inArray(type, reply_type_id));
    }
    $('.position-' + position + type_class).fadeIn();  
}