
$("#sendButton").click(function () {
    swal({
        title: "Estas seguro?",
        text: "Se reproducira en el robot inmediatamente!",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                if ($("#inputTextSend").val() === ''){
                    swal ( "Ha habido un problema..." ,  "No has indicado ningun mensaje!" ,  "error" )
                } else {
                    ws.send('{"command":"action","action":"speak", "user":"gabriel","value":"' + $("#inputTextSend").val() + '"}')
                    swal("Enviado!", {
                        icon: "success",
                    });
                }
            } else {
                swal("Se ha cancelado la peticion");
            }
        });
});


$("#stopRobot").click(function () {
    swal({
        title: "Estas seguro?",
        text: "Una vez enviado el robot se parara inmediatamente!",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                if ($("#inputActionSend").val() === ''){
                    swal ( "Ha habido un problema..." ,  "Tienes que indicar el motivo de la acción remota!" ,  "error" )
                } else {
                    ws.send('{"command":"action","action":"stop", "user":"gabriel","value":"' + $("#inputActionSend").val() + '"}')
                    swal("Enviado!", {
                        icon: "success",
                    });
                }
            } else {
                swal("Se ha cancelado la peticion");
            }
        });
});

$("#pauseRobot").click(function () {
    swal({
        title: "Estas seguro?",
        text: "Una vez enviado el robot se pausara inmediatamente!",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                if ($("#inputActionSend").val() === ''){
                    swal ( "Ha habido un problema..." ,  "Tienes que indicar el motivo de la acción remota!" ,  "error" )
                } else {
                    ws.send('{"command":"action","action":"pause", "user":"gabriel","value":"' + $("#inputActionSend").val() + '"}')
                    swal("Enviado!", {
                        icon: "success",
                    });
                }
            } else {
                swal("Se ha cancelado la peticion");
            }
        });
});

$("#resumeRobot").click(function () {
    swal({
        title: "Estas seguro?",
        text: "El robot continuara con su programa",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                if ($("#inputActionSend").val() === ''){
                    swal ( "Ha habido un problema..." ,  "Tienes que indicar el motivo de la acción remota!" ,  "error" )
                } else {
                    ws.send('{"command":"action","action":"play", "user":"gabriel","value":"' + $("#inputActionSend").val() + '"}')
                    swal("Enviado!", {
                        icon: "success",
                    });
                }
            } else {
                swal("Se ha cancelado la peticion");
            }
        });
});

$("#montaje").click(function () {
    swal({
        title: "Estas seguro?",
        text: "El robot cargara el programa montaje automaticamente",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                ws.send('{"command":"action","action":"load", "user":"gabriel","value":"phoneAssemblyBucle"}')
                swal("Enviado!", {
                    icon: "success",
                });
            } else {
                swal("Se ha cancelado la peticion");
            }
        });
});

$("#empaquetaje").click(function () {
    swal({
        title: "Estas seguro?",
        text: "El robot cargara el programa empaquetaje automaticamente",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                ws.send('{"command":"action","action":"load", "user":"gabriel","value":"phoneBoxing"}')
                swal("Enviado!", {
                    icon: "success",
                });
            } else {
                swal("Se ha cancelado la peticion");
            }
        });
});

var charts = []
var joint = 0
var data = {}

function updateLoadingStatus(show, data) {
    for (let i = 0; i < 6; i++) {
        if (show) {
            if (data) {
                $('#loadingWheel' + i).show()
                $('#nodata' + i).hide()
                $('#loadinggraphs' + i).show()
            } else {
                $('#loadingWheel' + i).hide()
                $('#nodata' + i).show()
                $('#loadinggraphs' + i).hide()
            }
            $('#infoTabs' + i).hide()
            $('#boxTabs' + i).hide()
        } else {
            $('#infoTabs' + i).show()
            $('#boxTabs' + i).show()
            $('#loadingWheel' + i).hide()
            $('#nodata' + i).hide()
            $('#loadinggraphs' + i).hide()
        }
    }
}

updateLoadingStatus(true, true)

for (let i = 0; i < 6; i++) {
    var ctx = document.getElementById('chartContainer' + joint);
    data = {
        labels: [],
        datasets: [{
            label: 'Temperatura',
            backgroundColor: "rgba(247,91,54,0.7)",
            strokeColor: "rgba(255,64,38,0.9)",
            data: []
        }]
    };
    charts.push(new Chart(ctx, {
        type: 'line',
        label: 'DefaultLabel',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                xAxes: [{
                    display: true,
                    labelString: 'probability'
                }],
                yAxes: [{
                    display: true,
                    labelString: 'probability'
                }]
            }
        }
    }));
    $('#chartContainer' + joint).hide()
    joint++;
    var ctx = document.getElementById('chartContainer' + joint);
    data = {
        labels: [],
        datasets: [{
            label: 'Corriente',
            backgroundColor: "rgba(0,181,194,0.65)",
            strokeColor: "rgba(0,120,129,0.9)",
            data: []
        }]
    };
    charts.push(new Chart(ctx, {
        type: 'line',
        label: 'DefaultLabel',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                xAxes: [{
                    display: true,
                    labelString: 'probability'
                }],
                yAxes: [{
                    display: true,
                    labelString: 'probability'
                }]
            }
        }
    }));
    $('#chartContainer' + joint).hide()
    joint++;
    var ctx = document.getElementById('chartContainer' + joint);
    data = {
        labels: [],
        datasets: [{
            label: 'Voltage',
            backgroundColor: "rgba(0,142,250,0.65)",
            strokeColor: "rgba(0,142,250,0.9)",
            data: []
        }]
    };
    charts.push(new Chart(ctx, {
        type: 'line',
        label: 'DefaultLabel',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                xAxes: [{
                    display: true,
                    labelString: 'probability'
                }],
                yAxes: [{
                    display: true,
                    labelString: 'probability'
                }]
            }
        }
    }));
    $('#chartContainer' + joint).hide()
    joint++;
}

var day = new Date().getDate()
var month = new Date().getMonth() + 1
var hour = new Date().getHours()
var path = 'events/' + (month < 10 ? '0' + month : month) + '/' + (day < 10 ? '0' + day : day) + '/' + (hour < 10 ? '0' + hour : hour)

var all_data_charts = []

firebase.database().ref('events/' + (month < 10 ? '0' + month : month)).once('value').then(function (snapshot) {
    all_data_charts = snapshot.val()
});

var firstTime = true
var minute_data = []
var hours_data = []
var days_data = []
var status = 0

$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    var target = $(e.target).attr("href")
    var id = target[target.length - 1]
    var hour = (new Date().getHours()) + '';
    var day = new Date().getDate();
    day = day < 10 ? '0' + day : '' + day;
    if (target.includes('minutes')) {
        tempList = all_data_charts[day][hour]
        tempListValues = []
        Object.keys(tempList).forEach(function (key) {
            val = {}
            val.key = Number(key)
            val.value = tempList[key]
            tempListValues.push(val)
        });
        updateChartsMinutes(id, tempListValues)
    } else if (target.includes('hours')) {
        status = 1
        tempList = all_data_charts[day]
        var chart = 0
        switch ($("ul#selectedTabsTCV li.tab-current-2")[id].innerText) {
            case "TEMPERATURA":
                chart = 0
                break;
            case "CORRIENTE":
                chart = 1
                break;
            case "VOLTAJE":
                chart = 2
                break;
        }
        var chart_id = Number(id) * 3 + chart

        charts[chart_id].data.labels = []
        charts[chart_id].data.datasets.data = []

        Object.keys(tempList).forEach(function (key) {
            hours_val = tempList[key]
            var mean = 0;
            var number = 0;
            Object.keys(hours_val).forEach(function (key) {
                switch (chart) {
                    case 0:
                        mean += JSON.parse(hours_val[key].temp)[chart]
                        break;
                    case 1:
                        mean += JSON.parse(hours_val[key].amp)[chart]
                        break;
                    case 2:
                        mean += JSON.parse(hours_val[key].voltage)[chart]
                        break;
                }
                number++
            });
            mean = mean / number;
            charts[chart_id].data.labels.push(key);
            charts[chart_id].data.datasets.forEach((dataset) => {
                dataset.data.push(mean);
            });
        });
        charts[chart_id].update();
    } else if (target.includes('days')) {

    }
});

function updateChartsMinutes(chart, tempListValues) {
    var start = 0
    if (chart < 0) {
        start = tempListValues.length - 1
    } else {
        charts[chart].data.labels = []
        charts[chart].data.datasets.data = []
        charts[chart].update();
    }
    if (firstTime) {
        start = 0
        firstTime = false
    }
    tempListValues.sort(function (a, b) {
        return Number(a.key) - Number(b.key)
    })
    updateLoadingStatus(false, false);
    var hour = new Date().getHours()
    var max = chart < 0 ? 6 : chart + 1;
    var min = chart < 0 ? 0 : chart;
    for (let j = start; j < tempListValues.length; j++) {
        var joint = 0
        for (let i = min; i < max; i++) {
            var minute = tempListValues[j].key < 10 ? '0' + tempListValues[j].key : tempListValues[j].key;
            charts[joint].data.labels.push(hour + ':' + minute);
            charts[joint].data.datasets.forEach((dataset) => {
                dataset.data.push(JSON.parse(tempListValues[j].value.temp)[i]);
            });
            charts[joint].update();
            $('#chartContainer' + joint).show()
            joint++;
            charts[joint].data.labels.push(hour + ':' + minute);
            charts[joint].data.datasets.forEach((dataset) => {
                dataset.data.push(JSON.parse(tempListValues[j].value.amp)[i]);
            });
            charts[joint].update();
            $('#chartContainer' + joint).show()
            joint++;
            charts[joint].data.labels.push(hour + ':' + minute);
            charts[joint].data.datasets.forEach((dataset) => {
                dataset.data.push(JSON.parse(tempListValues[j].value.voltage)[i]);
            });
            charts[joint].update();
            $('#chartContainer' + joint).show()
            joint++;
        }
    }
}

var dataCharts = firebase.database().ref(path);
dataCharts.on('value', function (snapshot) {
    values = snapshot.val()
    if (values == null) {
        updateLoadingStatus(true, false);
    } else {
        if (status == 0) {
            tempListValues = []
            Object.keys(values).forEach(function (key) {
                val = {}
                val.key = Number(key)
                val.value = values[key]
                tempListValues.push(val)
            });
            updateChartsMinutes(-1, tempListValues)
        }
    }
});

$(document).ready(function () {
    var sparklineLogin = function () {
        $("#sparkline1dash").sparkline([0, 23, 43, 35, 44, 45, 56, 37, 40, 45, 56, 7, 10], {
            type: 'line',
            width: '100%',
            height: '70',
            lineColor: '#fff',
            fillColor: 'transparent',
            spotColor: '#fff'
        });
        $('#sparkline2dash').sparkline([10, 12, 9, 6, 10, 9, 11, 9, 10, 12, 9, 11, 9, 10, 12], {
            type: 'bar',
            height: '70',
            barWidth: '5',
            resize: true,
            barSpacing: '10',
            barColor: '#fff'
        });
        $("#sparkline3dash").sparkline([130, 123, 120, 130, 140, 210, 152, 143, 128, 122, 123, 135, 128], {
            type: 'line',
            width: '100%',
            height: '70',
            lineColor: '#fff',
            fillColor: 'transparent',
            spotColor: '#fff',
            minSpotColor: undefined,
            maxSpotColor: undefined,
            highlightSpotColor: undefined,
            highlightLineColor: undefined
        });
        $('#sparkline4dash').sparkline([10, 12, 9, 6, 10, 9, 11, 9, 10, 12, 9, 11, 9, 10, 12], {
            type: 'bar',
            height: '70',
            barWidth: '5',
            resize: true,
            barSpacing: '10',
            barColor: '#fff'
        });

    }
    var sparkResize;

    $(window).resize(function (e) {
        clearTimeout(sparkResize);
        sparkResize = setTimeout(sparklineLogin, 100);
    });
    sparklineLogin();
});

setInterval(function updatePanelTemp() {
    ws.send('{"command":"joint_temperatures_json"}')
    for (let i = 0; i < 6; i++) {
        $("#temperature" + i).text(temperatures[i])
    }
}, 1000);

setInterval(function updatePanelCurrent() {
    ws.send('{"command":"actual_current_json"}')
    for (let i = 0; i < 6; i++) {
        var string = $("#current" + i).text((Math.abs(currents[i])).toString().slice(0, 6))
    }
}, 1000);

setInterval(function updatePanelVoltage() {
    ws.send('{"command":"actual_joint_voltage_json"}')
    for (let i = 0; i < 6; i++) {
        var string = $("#voltage" + i).text(voltages[i].toString().slice(0, 6))
    }
}, 1000);