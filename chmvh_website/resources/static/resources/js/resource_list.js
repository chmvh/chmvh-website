function collapseAll() {
    $('.resource-category').each(function() {
        var title = $(this).find('.resource-category__title-bar');
        var icon = title.find('i');
        var resources = $(this).find('.resources');

        title.css({
            'border-color': 'transparent',
            'padding-bottom': '0'
        });
        icon.removeClass('fa-minus').addClass('fa-plus');
        resources.css('display', 'none');
    });
}

function expandAll() {
    $('.resource-category').each(function() {
        var title = $(this).find('.resource-category__title-bar');
        var icon = title.find('i');
        var resources = $(this).find('.resources');

        title.css({
            'border-bottom': '',
            'padding-bottom': ''
        });
        icon.removeClass('fa-plus').addClass('fa-minus');
        resources.css('display', 'block');
    });
}

$(document).ready(function() {
    $('.resource-category__title-bar').css('cursor', 'pointer');
    $('.resource-category__toggle').css('display', 'inline-block');

    collapseAll();
});

$('.resource-category__title-bar').click(function(e) {
    e.preventDefault();

    var category = $(this).parent();
    var categoryTitle = category.find('> .resource-category__title-bar');
    var icon = $(this).find('i');
    var resources = category.find('> .resources');

    var collapsed = resources.is(':hidden');

    if (collapsed) {
        categoryTitle.css({
            'border-bottom': '',
            'padding-bottom': ''
        });
        resources.slideToggle();
        icon.removeClass('fa-plus').addClass('fa-minus');
    } else {
        categoryTitle.css({
            'border-color': 'transparent',
            'padding-bottom': '0'
        });
        resources.slideToggle();
        icon.removeClass('fa-minus').addClass('fa-plus');
    }
});
