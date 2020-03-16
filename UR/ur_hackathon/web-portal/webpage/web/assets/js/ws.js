var ws = new WebSocket("ws://192.168.1.40:30100/");

var $table = $('#table')

ws.onopen = function () {
    alert("Opened!");
};

ws.onmessage = function (evt) {
    var data = JSON.parse(evt.data);
    var layer = data.node;

};

ws.onclose = function () {
    alert("Closed!");
};

ws.onerror = function (err) {
    console.log(err)
    alert("Error: " + err);
};