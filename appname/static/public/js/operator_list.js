$(".operator-state-btn").click(function() {
    var v = $(this).val()
    var id = $(this).attr('data-id')
    $.post('update_operator_status', {'id': id
                                      ,'state': v})
    $(this).offsetParent().children('button').each(function(index, elem) {
        $(elem).removeClass('active')
    })
})
