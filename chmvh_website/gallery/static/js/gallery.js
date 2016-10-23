function resizeWhich(img) {
    img.removeAttr('style');

    if (window.innerWidth / img.width() < window.innerHeight / img.height()) {
        return 'width';
        console.log('Set width to 100%')
    } else {
        return 'height';
        console.log('Set height to 100%')
    }
}

$(document).ready(function() {
    $('.gallery__item').css('cursor', 'pointer');
    $('.gallery__item').click(function() {
        var thumb = $(this).find('img');
        var fullImg = $('<img />').attr('src', thumb.data('full-size'));

        $.featherlight(fullImg, {
            onResize: function() {
                var img = $('.featherlight-inner').removeClass('gallery__img');

                var prop = resizeWhich(img);
                var winHeight = window.innerHeight;
                var winWidth = window.innerWidth;
                var parent = img.parent();
                var padding = parseInt(parent.css('padding-top'));

                if (prop === 'height') {
                    var newHeight = (winHeight * .95) - 2 * padding - 1;
                    img.css('max-height', newHeight + 'px');
                } else {
                    var newWidth = (winWidth * .95) - 2 * padding - 1;
                    img.css('max-width', newWidth + 'px');
                }
            }
        });
    });
});
