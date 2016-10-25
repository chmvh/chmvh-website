function calcMaxHeight(parent) {
    var winHeight = window.innerHeight;
    var padding = parseInt(parent.css('padding-top')) + parseInt(parent.css('margin-top'));

    return parseInt((winHeight * .95) - (2 * padding) - 1);
}

function calcMaxWidth(parent) {
    var winWidth = window.innerWidth;
    var padding = parseInt(parent.css('padding-left')) + parseInt(parent.css('margin-left'));

    return parseInt((winWidth * .95) - (2 * padding) - 1);
}

function resizeImg(img) {
    img.removeAttr('style');

    var parent = img.parent();
    var maxHeight = calcMaxHeight(parent);
    var maxWidth = calcMaxWidth(parent);

    if (maxWidth / img.width() < maxHeight / img.height()) {
        img.css('max-width', maxWidth + 'px');
    } else {
        img.css('max-height', maxHeight + 'px');
    }
}

$(document).ready(function() {
    $('.gallery__item').css('cursor', 'pointer');
    $('.gallery__item').click(function() {
        var thumb = $(this).find('img');
        var fullImg = $('<img />').attr('src', thumb.data('full-size'));

        $.featherlight(fullImg, {
            beforeOpen: function() {
                $('.featherlight-inner').removeClass('gallery__img');
            },
            onResize: function() {
                var img = $('.featherlight-inner');
                resizeImg(img);
            }
        });
    });
});
