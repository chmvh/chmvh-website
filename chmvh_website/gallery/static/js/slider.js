function resizeSlider() {
    var container = $('.slider');

    var maxHeight = 0;
    container.find('.slider__item').each(function() {
        maxHeight = Math.max(maxHeight, $(this).height());
    });

    container.css('height', maxHeight + 'px');

    container.find('.slider__item').each(function() {
        var topMargin = (maxHeight - $(this).height()) / 2;

        $(this).css('margin-top', topMargin + 'px');
    });
};

// Code from:
// http://stackoverflow.com/a/4541963/3762084
var waitForFinalEvent = (function () {
  var timers = {};
  return function (callback, ms, uniqueId) {
    if (!uniqueId) {
      uniqueId = "Don't call this twice without a uniqueId";
    }
    if (timers[uniqueId]) {
      clearTimeout (timers[uniqueId]);
    }
    timers[uniqueId] = setTimeout(callback, ms);
  };
})();

$(window).on('load', resizeSlider);
$(window).resize(function() {
    waitForFinalEvent(resizeSlider, 250, "resize slider");
});
