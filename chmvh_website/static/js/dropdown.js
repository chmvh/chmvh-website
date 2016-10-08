$(document).ready(function() {
    $('.dropdown__description').css({
        'cursor': 'pointer'
    });
    $('.dropdown__menu').css('display', 'none');
});

$('.dropdown__description').click(function(e) {
    e.preventDefault();

    var description = $(this);
    var container = description.parent();
    var items = container.find('.dropdown__menu');

    if (items.is(':hidden')) {
        description.css({
            'margin-bottom': '1em'
        });
    } else {
        description.css({
            'margin-bottom': '0'
        });
    }

    items.slideToggle();
})
