$(function () { 

  $('#container').highcharts({
        chart: {
            type: 'column',
            backgroundColor: '#fff'
        },
        title: {
            text: 'Wait Time Estimator',
            style: {  
              color: '#ff'
            }
        },
        xAxis: {
            tickWidth: 0,
            labels: {
              style: {
                  color: '#333',
                 }
              },
            categories: ['9 am', '10 am', '11 am', '12 pm', '1 pm']
        },
        yAxis: {
           gridLineWidth: .5,
		      gridLineDashStyle: 'dash',
		      gridLineColor: 'black',
           title: {
                text: '',
                style: {
                  color: '#333'
                 }
            },
            labels: {
              formatter: function() {
                        return ''+Highcharts.numberFormat(this.value, 0, '', ',');
                    },
              style: {
                  color: '#333',
                 }
              }
            },
        legend: {
            enabled: false,
        },
        credits: {
            enabled: false
        },
        tooltip: {
           valueSuffix: ' min'
        },
        plotOptions: {
		      column: {
			      borderRadius: 0,
             pointPadding: -0.12,
			      groupPadding: 0.1
            } 
		    },
        series: [{
            name: 'Wait Time',
            data: [14, 45, {y:5,color:'pink'}, 20, 21]
        }]
    });
});