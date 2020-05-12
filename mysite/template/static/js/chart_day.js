    google.charts.load('current', {packages: ['corechart', 'bar']});
    google.charts.setOnLoadCallback(drawColColors);

function drawColColors() {
      var data = new google.visualization.DataTable();
      data.addColumn('timeofday', 'Time of Day');
      data.addColumn('number', 'Mean');
      var dataValues = {{ listData|safe }}
      console.log(dataValues);
      data.addRows(dataValues);

      var options = {
        colors: ['red', 'green', 'blue'],
        hAxis: {
          title: 'Time of Day',
          format: 'h:mm a',
          viewWindow: {
            min: [-1, 30, 0],
            max: [23, 30, 0]
          }
        },
        vAxis: {
          title: 'Temperature °C'
        }
      };

      var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
      chart.draw(data, options);
    }