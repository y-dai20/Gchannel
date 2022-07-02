function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('.agreebutton').on('click', function(){
    var id = $(this).attr('data-catid');
    var state = $(this).attr('value');
    $.ajax({
        url: '/post/' + state + '/' + id + '/',
        type:'GET',
        dataType:'json'
    }).done(function (data) {
        if (data['state'] == 'agree') {
            $('#agree' + String(data['post_id'])).removeClass("btn-outline-success").addClass("btn-success");
            $('#disagree' + String(data['post_id'])).removeClass("btn-danger").addClass("btn-outline-danger");
        } else if (data['state'] == 'disagree') {
            $('#agree' + String(data['post_id'])).removeClass("btn-success").addClass("btn-outline-success");
            $('#disagree' + String(data['post_id'])).removeClass("btn-outline-danger").addClass("btn-danger");
        } else {
            $('#agree' + String(data['post_id'])).removeClass("btn-success").addClass("btn-outline-success");
            $('#disagree' + String(data['post_id'])).removeClass("btn-danger").addClass("btn-outline-danger");
        }
        
        $('#agree_count' + String(data['post_id'])).text(data['agree_count']);
        $('#disagree_count' + String(data['post_id'])).text(data['disagree_count']);
    });
});

$('.favoritebutton').on('click', function(){
    var id = $(this).attr('data-catid');
    $.ajax({
        url: '/post/favorite/' + id + '/',
        type:'GET',
        dataType:'json'  
    }).done(function (data) {
        if (data['is_favorite']) {
            $('#favorite' + String(data['post_id'])).removeClass('fa-regular').addClass('solid-star fa-solid');
        } else {
            $('#favorite' + String(data['post_id'])).removeClass('solid-star fa-solid').addClass('fa-regular');
        }
    });
});

$('.likebutton').on('click', function(){
    var id = $(this).attr('data-catid');
    console.log("likebutton");
    $.ajax({
        url: '/reply/like/' + id + '/',
        type:'GET',
        data:{status: $(this).attr('value')},
        dataType:'json'  
    }).done(function (data) {
        var tag = $('#like_count' + String(data['reply_id']));
        var like_count = parseInt(tag.text());
        
        if (data['is_like']) {
            like_count = like_count + 1;
        } else {
            like_count = like_count - 1;
        }
        tag.text(like_count);

        $('#like' + String(data['reply_id'])).toggleClass('like-reply');
    });
});


// $(window).on('scroll', function(){
//     var bottom = $(document).innerHeight() - $(window).innerHeight();
//     if (bottom * 0.8 <= $(window).scrollTop()) {
//         var post_count = $('.post-for-count').length;
//         $.ajax({
//             url: '/',
//             type:'POST',
//             data:{start_idx:post_count},
//             dataType:"json"
//         }).done(function (json_htmls) {
            
//             // for (var i in json_htmls) {
//             //     $('.container').append(json_htmls[i].html);
//             // }
            
//             $('.container').append(json_htmls.a);
//         })
//     }
// })

$('.follow-button').on('click', function(){
    var username = $(this).attr('data-catid');
    $.ajax({
        url: '/follow/user/' + username + '/',
        type:'GET',
        dataType:'json'
    }).done(function (data) {
        if (data["is_done"]) {
            $('#follow-' + data['username']).removeClass('btn-outline-secondary').addClass('btn-secondary')
        } else {
            $('#follow-' + data['username']).removeClass('btn-secondary').addClass('btn-outline-secondary')
        } 
        $('#follow-' + data['username']).text(data["text"])
    });
});
