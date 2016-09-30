function activateNavLink(id) {
    $(id).addClass('active');
}

$(document).ready(function() {
    $('.navbar__toggle').click(function(e) {
        e.preventDefault();

        var target = $($(this).data('target'));

        if (target.is(':hidden')) {
            target.show();
        } else {
            target.removeAttr('style');
        }
    });
});
