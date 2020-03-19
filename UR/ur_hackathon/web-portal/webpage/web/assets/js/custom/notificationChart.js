var month = new Date().getMonth() + 1
var mychart = new Chart(document.getElementById("notificationChart"), {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            data: [],
            label: "Informativo",
            borderColor: "rgb(0,142,250)",
            fill: false
        }, {
            data: [],
            label: "Exito",
            borderColor: "rgb(0,142,50)",
            fill: false
        }, {
            data: [],
            label: "Advertencia",
            borderColor: "rgb(248,194,85)",
            fill: false
        }, {
            data: [],
            label: "Critico",
            borderColor: "rgb(247,91,54)",
            fill: false
        }
        ]
    }
});

var i = 0;
var already_added = []

function updateChart(events_data) {
    let data = 0
    for (let j = 0; j < events_data.length; j++) {
        var date = new Date(events_data[j][1].date)
        if (already_added.indexOf(events_data[j][0]) < 0){
            if (mychart.data.labels.indexOf(date.getDate() + ' de Abril\n'  + date.getHours() + ':00') < 0) {
                mychart.data.labels.push(date.getDate() + ' de Abril\n' + date.getHours() + ':00')
                mychart.data.datasets.forEach((dataset) => {
                    dataset.data.push(0);
                });
                data = mychart.data.labels.length - 1
            }
            switch (events_data[j][1].type) {
                case 1216:
                case 1536:
                    mychart.data.datasets[3].data[data]++
                    break;
                case 1028:
                    mychart.data.datasets[2].data[data]++
                    break;
                case 1:
                    mychart.data.datasets[1].data[data]++
                    break;
                default:
                    mychart.data.datasets[0].data[data]++
                    break;
            }
            already_added.push(events_data[j][0])
        }
    }
    mychart.update()

}


var dataCharts = firebase.database().ref('notifications/unread');
dataCharts.on('value', function (snapshot) {
    let general = snapshot.val()
    if (general !== null) {
        let events_data = Object.getOwnPropertyNames(general).map(function (e) {
            return [e, general[e]];
        });
        updateChart(events_data)
    }
});

firebase.database().ref('notifications/read').once('value').then(function (snapshot) {
    let general = snapshot.val()
    events_data = Object.getOwnPropertyNames(general).map(function (e) {
        return [e, general[e]];
    });
    events_data.sort(function (a, b) {
        return a[1].date - b[1].date;
    })
    updateChart(events_data)
});