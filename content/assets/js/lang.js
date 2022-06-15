$(document).ready(function () {

    // Show dropdown
    $('.selected').click(function () {
        $('.custom-sel').addClass('show-sel');
        $('.custom-sel option').removeClass('hidden');
    });

    // Hide dropdown when not focused
    $('.custom-sel').focusout(function () {
        $('.custom-sel').removeClass('show-sel');
        $('.custom-sel option:not(:first)').addClass('hidden');
    }).blur(function () {
        $('.custom-sel').removeClass('show-sel');
        $('.custom-sel option:not(:first)').addClass('hidden');
    });

});