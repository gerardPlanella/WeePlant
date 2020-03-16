// Dashboard 1 Morris-chart

Morris.Donut({
    element: 'morris-donut-chart',
    data: [{
        label: "Robot",
        value: 65,
    }, {
        label: "Ensamblaje",
        value: 59,
    }, {
        label: "Humano",
        value: 90,
    }, {
        label: "Orden",
        value: 56,
    }, {
        label: "Otros",
        value: 43,
    }],
    resize: true,
    colors:['#f75b36', '#00c292', '#6164c1','#99d683', '#13dafe']
});

Morris.Donut({
    element: 'morris-donut-chart1',
    data: [{
        label: "Robot",
        value: 43,
    }, {
        label: "Ensamblaje",
        value: 56,
    }, {
        label: "Humano",
        value: 59,
    }, {
        label: "Orden",
        value: 90,
    }, {
        label: "Otros",
        value: 43,
    }],
    resize: true,
    colors:['#f75b36', '#00c292', '#6164c1','#99d683', '#13dafe']
});


Morris.Area({
    element: 'morris-area-chart2',
    data: [{
        period: '2010',
        SiteA: 0,
        SiteB: 0,

    }, {
        period: '2011',
        SiteA: 130,
        SiteB: 100,

    }, {
        period: '2012',
        SiteA: 80,
        SiteB: 60,

    }, {
        period: '2013',
        SiteA: 70,
        SiteB: 200,

    }, {
        period: '2014',
        SiteA: 180,
        SiteB: 150,

    }, {
        period: '2015',
        SiteA: 105,
        SiteB: 90,

    },
        {
            period: '2016',
            SiteA: 250,
            SiteB: 150,

        }],
    xkey: 'period',
    ykeys: ['SiteA', 'SiteB'],
    labels: ['Site A', 'Site B'],
    pointSize: 0,
    fillOpacity: 0.4,
    pointStrokeColors:['#fdc006', '#00bfc7'],
    behaveLikeLine: true,
    gridLineColor: '#e0e0e0',
    lineWidth: 0,
    smooth: false,
    hideHover: 'auto',
    lineColors: ['#fdc006', '#00bfc7'],
    resize: true

});

/*
Morris.Area({
        element: 'morris-area-chart2',
        data: [{
            period: '2010',
            SiteA: 0,
            SiteB: 0,
            
        }, {
            period: '2011',
            SiteA: 130,
            SiteB: 100,
            
        }, {
            period: '2012',
            SiteA: 80,
            SiteB: 60,
            
        }, {
            period: '2013',
            SiteA: 70,
            SiteB: 200,
            
        }, {
            period: '2014',
            SiteA: 180,
            SiteB: 150,
            
        }, {
            period: '2015',
            SiteA: 105,
            SiteB: 90,
            
        },
         {
            period: '2016',
            SiteA: 250,
            SiteB: 150,
           
        }],
        xkey: 'period',
        ykeys: ['SiteA', 'SiteB'],
        labels: ['Sales A', 'Sales B'],
        pointSize: 0,
        gridTextColor:'#2b2b2b',
        fillOpacity: 0,
        pointStrokeColors:['#b4becb', '#008efa'],
        behaveLikeLine: true,
        gridLineColor: 'rgba(0, 0, 0, 0.05)',
        lineWidth: 2,
        smooth: true,
        hideHover: 'auto',
        lineColors: ['#b4becb', '#008efa'],
        resize: true
        
    });

*/
 $('.vcarousel').carousel({
            interval: 3000
         })
$(".counter").counterUp({
        delay: 100,
        time: 1200
    });

$(document).ready(function() {
    
   var sparklineLogin = function() { 
        $('#sales1').sparkline([20, 40, 30], {
            type: 'pie',
            height: '120',
            resize: true,
            sliceColors: ['#00b5c2', '#183f7c', '#f6f6f6']
        });
        $('#sparkline2dash').sparkline([6, 10, 9, 11, 9, 10, 12], {
            type: 'bar',
            height: '154',
            barWidth: '4',
            resize: true,
            barSpacing: '10',
            barColor: '#25a6f7'
        });
       
        $('#sparkline2dash2').sparkline([6, 10, 9, 11, 9, 10, 12], {
            type: 'bar',
            height: '154',
            barWidth: '4',
            resize: true,
            barSpacing: '10',
            barColor: '#f75b36'
        });
       $('#sales12').sparkline([6, 10, 9, 11, 9, 10, 12], {
            type: 'bar',
            height: '154',
            barWidth: '4',
            resize: true,
            barSpacing: '10',
            barColor: '#2b2b2b'
        });
        
   }
    var sparkResize;
 
        $(window).resize(function(e) {
            clearTimeout(sparkResize);
            sparkResize = setTimeout(sparklineLogin, 500);
        });
        sparklineLogin();

});