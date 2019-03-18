$("#filter-form input[name=tag]").each(function () {
    $(this).change(function () {
        $('#check_all').removeAttr("checked");
        $('#filter-form').submit();
    });
});
$("#check_all").change(function () {
    if ($("#check_all").is(':checked')) {
        $("#filter-form input[name=tag]").each(function () {
            $(this).removeAttr("checked");
        });
        $('#filter-form').submit();
    }
});

function blog_sort(sf) {
    $('#sort_filter').attr('value', sf);
    $('#filter-form').submit();
}

function set_sort_content() {
    var sf = $("input[name='sf']").attr('value');
    var content = $("button[name=" + sf + "]").text();
    var filter = $("#" + $("button[name=" + sf + "]").parent().attr('aria-labelledby')).text().trim();
    $("#sorted_by").text('by ' + filter + ' ' + content);
}

set_sort_content();
