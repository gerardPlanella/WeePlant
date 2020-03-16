var direction = 1;
var opacity = 0.0;

var heartbeat = function() {

    if (direction) {
        opacity = opacity + 0.1;
    }

    if (!direction) {
        opacity = opacity - 0.1;
    }

    if (opacity >= 1.0 || opacity < 0.0) {
        direction = !direction;
    }

    for (let i = 1; i < 7; i++) {
        $("#robot" + i).css('opacity', opacity);
    }
}

var heartbeatInterval;
var chartInterval;

$(document).ready(function(){
    setTimeout(f, 2000);
});

function f() {
    clearInterval(heartbeatInterval);
    heartbeatInterval = setInterval(heartbeat, 100);
}