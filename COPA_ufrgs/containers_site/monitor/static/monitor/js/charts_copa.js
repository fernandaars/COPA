
var chart1 = Highcharts.chart('chart1', {

    chart:{
        width: 300,
        height: 250,
        type: 'line',
        
        // events: {
         //    load: requestlinksData
        // }
    },

    credits: {
        enabled: false
    },


    title: {
        text: ''
    },

    subtitle: {
        text: ''
    },

    yAxis: {
        gridLineWidth: 1,
        title: {
            text: 'Milisseconds'
        }
    },
    
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

     xAxis: {
            type: 'datetime',

            

            title: {
                text: 'Time'
            }
      },

    plotOptions: {
        series: {
            label: {
                connectorAllowed: false
            },
            pointStart: 0,
        }

    },

    series: [{
        name: 'Uplink',
        data: []
    }, {
        name: 'Downlink',
        data: []
    }],


    responsive: {
        rules: [{
            condition: {
                maxWidth: 300
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }

});



var chart2 = Highcharts.chart('chart2', {

    chart:{
        width: 300,
        height: 250,
        type: 'line',
        
        //events: {
        //    load: requestlinksData
        //}
    },

    credits: {
        enabled: false
    },


    title: {
        text: ''
    },

    subtitle: {
        text: ''
    },

    yAxis: {
        gridLineWidth: 1,
        title: {
            text: 'Milisseconds'
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

     xAxis: {
            type: 'datetime',
            title: {
                text: 'Time'
            }
      },

    plotOptions: {
        series: {
            label: {
                connectorAllowed: false
            },
            pointStart: 0
        }
    },

    series: [{
        name: 'Uplink',
        data: []
    }, {
        name: 'Downlink',
        data: []
    }],

    responsive: {
        rules: [{
            condition: {
                maxWidth: 300
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }

});


// Make monochrome colors
var pieColors = (function () {
    var colors = [],
        base = Highcharts.getOptions().colors[0],
        i;

    for (i = 0; i < 10; i += 1) {
        // Start out with a darkened base color (negative brighten), and end
        // up with a much brighter color
        colors.push(Highcharts.Color(base).brighten((i - 3) / 7).get());
    }
    return colors;
}());

// Build the chart
var chart3 = Highcharts.chart('chart3', {
    chart: {
        width: 250,
        height: 200,
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie',

        //events: {
        //    load: requestlinksData
        //}
    },


    credits: {
        enabled: false
    },

    title: {
        text: ''
    },
    
    tooltip: {
        pointFormat: '<b>{point.percentage:.1f}%</b>'
    },

    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            colors: pieColors,
            dataLabels: {
                enabled: false,
                distance: -50,
                filter: {
                    property: 'percentage',
                    operator: '>',
                    value: 4
                }
            }
        }
    },

    series: [{
        name: "Wireless",
        data: [
            {
                name: 'TX',
                y: 0,
            }, 
            {
                name: 'TX failed',
                y: 0,
            }, 
            {
                name: 'RX',
                y: 0,
            }
        ]
    }]

});



var gaugeOptions = {

    chart: {
        spacingTop: -1500,
        width: 280,
        height: 200,
        type: 'solidgauge',
        marginTop: 0,
        spacingTop: 0,

        //events: {
        //    load: requestlinksData
        //}
    },

    title: null,

    pane: {
        center: ['50%', '85%'],
        size: '160px',
        startAngle: -90,
        endAngle: 90,
        background: {
            backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
            innerRadius: '60%',
            outerRadius: '100%',
            shape: 'arc'
        }
    },

    tooltip: {
        enabled: false
    },

    // the value axis
    yAxis: {
        stops: [
            [0.1, '#77a4d1'], // green
            [0.5, '#346da4'], // yellow
            [0.9, '#0f487f'] // red
        ],
        lineWidth: 0,
        minorTickInterval: null,
        tickAmount: 2,
        title: {
            y: -70
        },
        labels: {
            y: 16
        }
    },

    plotOptions: {
        solidgauge: {
            dataLabels: {
                y: 5,
                borderWidth: 0,
                useHTML: true
            }
        }
    }
};


// The speed gauge
var chartSpeed = Highcharts.chart('container-speed', Highcharts.merge(gaugeOptions, {
    yAxis: {
        min: -60,
        max: 10,
        title: {
            text: 'RSSI'
        }
    },

    credits: {
        enabled: false
    },

    series: [{
        name: 'Speed',
        data: [0],
        dataLabels: {
            format: '<div style="text-align:center"><span style="font-size:19px;color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
                   '<span style="font-size:12px;color:silver">dB</span></div>'
        },
        tooltip: {
            valueSuffix: ' '
        }
    }]

}));
