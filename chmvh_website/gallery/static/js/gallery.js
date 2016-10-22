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
        var img = $(this).find('img');

        $.featherlight(img, {
            onResize: function() {
                var img = $('.featherlight-inner').removeClass('gallery__img');

                var prop = resizeWhich(img);
                var parent = img.parent();
                var padding = parseInt(parent.css('padding-top'));

                if (prop === 'height') {
                    var newHeight = parent.innerHeight() - 2 * padding;
                    img.css('height', newHeight + 'px');
                } else {
                    var newWidth = parent.innerWidth() - 2 * padding;
                    img.css('width', newWidth + 'px');
                }
            }
        });
    });
});
