setInterval(function updateCiclos() {
    var string = $("#updateCiclos").text()
    var x = Number(string)
    x = x + 1;
    $("#updateCiclos").text(x)
}, 78000);

setInterval(function updateTiempoCiclo() {
    var string = $("#updateTiempoCiclo").text()
    var x = Number(string)
    var random = Math.random() * 10;
    if (random > 5) {
        x = x + 1;
    } else {
        x = x - 1;
    }
    $("#updateTiempoCiclo").text(x)
}, 8000);

setInterval(function updateMontajes() {
    var x = Number($("#updateMontajes").text())
    x = x + 1;
    $("#updateMontajes").text(x)
}, 12000);

setInterval(function updateMontaje() {
    var string = $("#updateMontaje").text()
    var x = Number(string)
    var random = Math.random() * 10;
    if (random > 3) {
        x = x + 1;
    } else {
        x = x - 1;
    }
    $("#updateMontaje").text(x)
}, 7000);

window.chartColors = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};

var ctx6 = document.getElementById("problemsPie");
var myDoughnutChart = new Chart(ctx6, {
    type: 'polarArea',
    data: {
        labels: ['Ensamblaje', 'Robot', 'Humano', 'Orden'],
        datasets: [{
            data: [10, 20, 30, 34],
            backgroundColor: [
                'rgb(0, 194, 146)',
                'rgb(247, 91, 54)',
                'rgb(97, 100, 193)',
                'rgb(153, 214, 131)'
            ]
        }]
    },
    options: {
        legend: {
            display: false
        }
    }
});

var ctx7 = document.getElementById("problemsPie2");
var myDoughnutChart = new Chart(ctx7, {
    type: 'polarArea',
    data: {
        labels: ['Ensamblaje', 'Robot', 'Humano', 'Orden'],
        datasets: [{
            data: [23, 10, 34, 22],
            backgroundColor: [
                'rgb(0, 194, 146)',
                'rgb(247, 91, 54)',
                'rgb(97, 100, 193)',
                'rgb(153, 214, 131)'
            ]
        }]
    },
    options: {
        legend: {
            display: false
        }
    }
});

var barChartData = {
    labels: ['Diciembre', 'Enero', 'Febrero', 'Marzo', 'Abril'],
    datasets: [{
        label: 'K42',
        backgroundColor: 'rgb(255, 159, 64)',
        data:
            [23, 10, 34, 22, 45]
    }, {
        label: 'K72',
        backgroundColor: 'rgb(75, 192, 192)',
        data:
            [56, 10, 34, 34, 45]
    }
    ]

};

var ctx8 = document.getElementById("problemsPie3");
var myDoughnutChart3 = new Chart(ctx8, {
    type: 'bar',
    data: barChartData,
    options: {
        tooltips: {
            mode: 'index',
            intersect: false
        },
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
                stacked: true,
            }],
            yAxes: [{
                stacked: true
            }]
        }
    }
});