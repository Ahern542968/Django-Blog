$('#I-wanna-comm').click(function () {
    $('html').animate({scrollTop: $('#comment-form').offset().top - 200}, 100);
    $('#id_content').focus();
});
$('#id_content').focus(function () {
    $('#comment-tips').text('');
    $('#id_p_comment_id').val(0);
    $('#id_content').addClass('open');
});
$('#id_content').focusout(function () {
    $('#id_content').removeClass('open').attr('placeholder', 'What do you want to say to the author');
});
$('#comment-form').submit(function () {
    if ($('#id_content').val().trim().length < 5) {
        $('#comment-tips').text('Valid characters cannot be less than 5');
        return false;
    }
    $.ajax({
        url: "/comment/create_comment",
        type: 'POST',
        data: $(this).serialize(),
        success: function (data) {
            if (data['status'] == 'success') {
                var id_p_comment_id = $('#id_p_comment_id').val();
                if (id_p_comment_id == 0) {
                    $("#no_comment").text('');
                    var comment_html = "<div id='root_" + data['root_id'] + "' class=\"comment\">\n<span>" +
                        data['c_user'] + "</span>\n<span>(" + data['date'] + "):</span>\n" +
                        "<div id=\"comment_" + data['id'] + "\">" + data['content'] + "&nbsp;&nbsp;&nbsp;&nbsp;<a\n" +
                        "href=\"javascript:reply(" + data['id'] + ");\">回复</a></div>\n" +
                        "</div>\n<div class=\"dropdown-divider\"></div>";
                    $('.comm-items').prepend(comment_html);
                } else {
                    var comment_html = "<span class=\"pl-5 text-muted\">-----------------------------------" +
                        "------------</span>\n<div class=\"reply pl-5\">\n<span>" + data['c_user'] +
                        "</span>\n<span>(" + data['date'] + "):</span>\n<span>回复</span>\n<span>" +
                        data['r_user'] + "</span>\n<div id=\"comment_" + data['id'] + "\">" + data['content'] +
                        "&nbsp;&nbsp;&nbsp;&nbsp;<a\nhref=\"javascript:reply(" + data['id'] + ")\">回复</a>" +
                        "</div>\n</div>";
                    $('#root_' + data['root_id']).append(comment_html);
                }
                $('.comment-content').val('');
                $('html').animate({scrollTop: $('#comment_' + data['id']).offset().top - 200}, 100);
                $('#comment-tips').text(data['msg']);
            } else {
                $('#comment-tips').text(data['msg']);
            }
        },
    });
    return false;
});

function reply(reply_id) {
    var username = $('#comment_' + reply_id).parent('div').find('span').eq(0).text();
    $('html').animate({scrollTop: $('#comment-form').offset().top - 200}, 100);
    $('#id_content').attr('placeholder', 'You want to reply ' + username + ' :').focus();
    $('#id_p_comment_id').val(reply_id);
}