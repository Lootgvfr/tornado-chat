/**
 * Created by D-N on 17/02/2017.
 */

var form = $('#messageForm');
var error = $('#error-text');
var chat_container = $('#chat-container');
var panel = $('#panel-content');
var socket = new WebSocket(form.attr('data-socket-url'));

socket.onmessage = function (event) {
    var result = JSON.parse(event.data);
    if (result.type == 'response'){
        $('#msg-text').val('');
    }
    else if (result.type == 'new_message'){
        panel.prepend(result.content);
        chat_container.scrollTop(0);
    }
    else if (result.type == 'open'){
        panel.prepend(result.content);
    }
    else if (result.type == 'error'){
        error.html(result.message);
    }
};

socket.onerror = function (error) {
    alert('topkek failed: ' + error.message);
};

form.on('submit', function(event){
    event.preventDefault();
    error.html('');
    var msg = $('#msg-text').val();
    //if (msg) socket.send(msg);
    socket.send(msg);
});

$("#msg-text").keypress(function (event) {
    if (event.keyCode == 13 && !event.shiftKey) {
        form.trigger('submit');
        event.preventDefault();
    }
});