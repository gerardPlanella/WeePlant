$( document ).ready(function() {

    var ctx6 = document.getElementById("chart6").getContext("2d");
    var data6 = {
        labels: ["Malfuncionamiento del robot", "Línea de ensamblaje no sincronizada", "Error Humano", "Orden Ensamblaje", "Otros", "Partes faltantes"],
        datasets: [
            {
                label: "My First dataset",
                fillColor: "rgba(19,218,254,0.8)",
                strokeColor: "rgba(19,218,254,1)",
                pointColor: "rgba(19,218,254,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(19,218,254,1)",
                data: [65, 59, 90, 81, 56, 45]
            },
            {
                label: "My Second dataset",
                fillColor: "rgba(97,100,193,0.8)",
                strokeColor: "rgba(97,100,193,1)",
                pointColor: "rgba(97,100,193,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(97,100,193,1)",
                data: [28, 48, 40, 19, 34, 83]
            }
        ]
    };

    var myRadarChart = new Chart(ctx6).Radar(data6, {
        scaleShowLine : true,
        angleShowLineOut : true,
        scaleShowLabels : false,
        scaleBeginAtZero : true,
        angleLineColor : "rgba(0,0,0,.1)",
        angleLineWidth : 1,
        pointLabelFontFamily : "'Arial'",
        pointLabelFontStyle : "normal",
        pointLabelFontSize : 10,
        pointLabelFontColor : "#666",
        pointDot : true,
        pointDotRadius : 3,
        tooltipCornerRadius: 2,
        pointDotStrokeWidth : 1,
        pointHitDetectionRadius : 20,
        datasetStroke : true,
        datasetStrokeWidth : 2,
        datasetFill : true,
        legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>",
        responsive: true
    });

});