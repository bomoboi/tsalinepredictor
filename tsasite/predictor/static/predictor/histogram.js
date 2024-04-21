const times = JSON.parse(document.getElementById('times').textContent);
const avgs = JSON.parse(document.getElementById('avgs').textContent);

$(function () {

  $('#container').highcharts({
        chart: {
            type: 'column',
            backgroundColor: '#fff'
        },
        title: {
            text: '',
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
            categories: times
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
           valueSuffix: ' pax/hr'
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
            data: avgs
        }]
    });
});
