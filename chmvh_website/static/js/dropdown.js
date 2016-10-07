$(document).ready(function() {
    $('.dropdown__description').css({
        'border-width': '0',
        'cursor': 'pointer'
    });
    $('.dropdown__items').css('display', 'none');
});

$('.dropdown__description').click(function(e) {
    e.preventDefault();

    var description = $(this);
    var container = description.parent();
    var items = container.find('.dropdown__items');

    if (items.is(':hidden')) {
        description.css('border-width', '1px');
    } else {
        description.css('border-width', '0');
    }

    items.slideToggle();
})
