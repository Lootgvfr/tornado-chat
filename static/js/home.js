/**
 * Created by D-N on 17/02/2017.
 */

var form = $('#messageForm');
var error = $('#error-text');

form.on('submit', function(event){
    event.preventDefault();
    error.html('');
    $.ajax({
        url: form.attr('data-link'),
        type: 'POST',
        dataType: 'json',
        data: form.serialize(),
        success: function (data) {
            if (data.type == 'error') {
                error.html(data.message);
            }
            else if (data.type == 'success') {
                $('#msg-text').val('');
            }
        }
    });
});

$("#msg-text").keypress(function (event) {
    if (event.keyCode == 13 && !event.shiftKey) {
        form.trigger('submit');
        event.preventDefault();
    }
});