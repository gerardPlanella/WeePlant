var ws = new WebSocket("ws://192.168.1.40:30101/");

var temperatures = [];
var voltages = [];
var currents = [];
var oldCurrent = [];

ws.onopen = function () {
    console.log("opened")
};

ws.onmessage = function (event) {
    try {
        received = JSON.parse(event.data)
        value = JSON.parse(received.value)
        if (value === "" || value.length !== 6) {
            return;
        }
        switch (received.command) {
            case 'joint_temperatures_json':
                temperatures = value
                break;
            case 'actual_joint_voltage_json':
                voltages = value
                break;
            case 'actual_current_json':
                currents = value
                break;
            default:
                console.error('Received unknown data: ' + event.data)
                break;
        }
    } catch(e) {
        console.error(e); // error in the above string (in this case, yes)!
    }
};

ws.onclose = function () {
    console.log("Closed!");
};

ws.onerror = function (err) {
    console.log(err)
};

var dataCharts = firebase.database().ref('/status');
dataCharts.on('value', function (snapshot) {
    var received = snapshot.val()
    if (received !== null) {
        if (received.on == 1) {
            $('#textStatusRobot').text('Encendido')
            $('#statusRobot').removeClass()
            $('#statusRobot').addClass('white-box-shadow text-center bg-success')
            $('#modalStatus').text('ON');
            $('#modalStatus').addClass('label label-success');
        } else if (received.on == 0) {
            $('#textStatusRobot').text('Apagado')
            $('#statusRobot').removeClass()
            $('#statusRobot').addClass('white-box-shadow text-center bg-danger')
            $('#modalStatus').text('OFF');
            $('#modalStatus').addClass('label label-danger')
        }
    }
});