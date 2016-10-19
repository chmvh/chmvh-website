function collapseAll() {
    $('.expanding-list').each(function() {
        var title = $(this).find('.expanding-list__title-bar');
        var icon = title.find('i');
        var items = $(this).find('.elist-items');

        title.css({
            'border-color': 'transparent',
            'padding-bottom': '0'
        });
        icon.removeClass('fa-minus').addClass('fa-plus');
        items.css('display', 'none');
    });
}

function expandAll() {
    $('.expanding-list').each(function() {
        var title = $(this).find('.expanding-list__title-bar');
        var icon = title.find('i');
        var items = $(this).find('.elist-items');

        title.css({
            'border-bottom': '',
            'padding-bottom': ''
        });
        icon.removeClass('fa-plus').addClass('fa-minus');
        items.css('display', 'block');
    });
}

$(document).ready(function() {
    $('.expanding-list__title-bar').css('cursor', 'pointer');
    $('.expanding-list__toggle').css('display', 'inline-block');

    collapseAll();
});

$('.expanding-list__title-bar').click(function(e) {
    e.preventDefault();

    var category = $(this).parent();
    var categoryTitle = category.find('> .expanding-list__title-bar');
    var icon = $(this).find('i');
    var items = category.find('> .elist-items');

    var collapsed = items.is(':hidden');

    if (collapsed) {
        categoryTitle.css({
            'border-bottom': '',
            'padding-bottom': ''
        });
        items.slideToggle();
        icon.removeClass('fa-plus').addClass('fa-minus');
    } else {
        categoryTitle.css({
            'border-color': 'transparent',
            'padding-bottom': '0'
        });
        items.slideToggle();
        icon.removeClass('fa-minus').addClass('fa-plus');
    }
});
