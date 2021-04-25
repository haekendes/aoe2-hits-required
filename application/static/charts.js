var scatterChart,
    lineChart, 
    histogram,
    options,
    histOptions,
    chartsInitialized = false,
    chartIcons = [],
    observer; // global observer var to reduce draw calls upon multiple column select changes

  google.charts.load('current', {packages: ['corechart']});
  google.charts.setOnLoadCallback(init);

  function init() {
    options = {
      'height': 500,
      colors: ['#fadcd1', '#f6c7b6', '#f3b49f','#ec8f6e','#e6693e', '#e05424', '#e0440e', 'c53300'],
      vAxis: {
        title: 'Hits required',
        titleTextStyle: {italic: false, bold: true}
      },
      hAxis: {
        title: 'Defense Upgrades',
        titleTextStyle: {italic: false, bold: true}
      },
      explorer: {
        zoomDelta: 1.3,
      },
      selectionMode: 'multiple',
      animation: {
        startup: true,
        duration: 750,
        easing: 'inAndOut',
      },
    };

    // Instantiate and draw the chart.
    scatterChart = new google.visualization.ScatterChart(document.getElementById('chart1'));

    lineChart = new google.visualization.LineChart(document.getElementById('chart2'));

    histOptions = {};
    Object.assign(histOptions, options);    
    //change options for histogram
    histOptions['colors']= ['#ec8f6e',];
    histOptions['vAxis'] = {
      title: 'Amount of Matchups',
      titleTextStyle: {italic: false, bold: true}
    }
    histOptions['hAxis'] = {
      title: 'Hits required',
      titleTextStyle: {italic: false, bold: true}
    }
    
    histogram = new google.visualization.Histogram(document.getElementById('chart3'));
  }


  function drawCharts(data) {
    showChartInfoIcon();
    let checkboxes = document.querySelectorAll("input[type=checkbox]");
    let columns = 
              Array.from(checkboxes) // Convert checkboxes to an array to use filter and map.
              .filter(i => i.checked) // Use Array.filter to remove unchecked checkboxes.
              .map(i => i.value) // Use Array.map to extract only the checkbox values from the array of objects.      

    if (columns.length > 0) {
      let redrawTable = getChartDataTable(columns, data);
      let charts = [].slice.call(document.getElementsByClassName("chart"));

      if(observer) {
        charts.forEach(function(chart) {
          observer.unobserve(chart);
        })
      }
      observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {

          if (entry.isIntersecting) {

            if(entry.target.id === 'chart1') {
              drawScatterChart(redrawTable);
              observer.unobserve(entry.target);
            }
            else if (entry.target.id === 'chart2') {
              drawLineChart(redrawTable);
              observer.unobserve(entry.target);
            } 
            else if (entry.target.id === 'chart3') {
              drawHistogram(getHistDataTable(columns, data));
              observer.unobserve(entry.target);
            }
          }
        });
      }, {threshold: 0.7});

      charts.forEach(function(chart) {
        observer.observe(chart);
      })
  }
}

  function showChartInfoIcon() {
    let element = document.getElementById('chart-info');
    element.innerHTML = '<details><summary><i class="bi bi-info-circle"></i></summary><ul> <li>Try to hover over / click on the attack upgrades in the chart&#39;s legend. You can select multiple.</li> <li>You can pan & zoom inside the chart. Right click to reset the view.</li> <li>Each chart can be saved as png.</li> </ul></details>'
    element.title = "Information";
    element.style.display = 'table';
    element.classList.add("chart-info", "animate__animated", "animate__backInRight");
    chartIcons.push(element);
  }

  function addPngDownloadToChart(chart, id, fileName) {
    google.visualization.events.addListener(chart, 'ready', function () {
      let element = document.getElementById(id);
      element.innerHTML = '<a download='+ fileName +' href="'+ chart.getImageURI() + '" style="margin-right: 32px;"><i class="bi bi-card-image"></i><i class="bi bi-download"></i></a>';
      element.title = "Save chart as png";
      element.style.display = 'revert';
      element.classList.add("png-download", "animate__animated", "animate__backInRight");
      chartIcons.push(element);
    });
  }

  function getChartDataTable(columns, data) {
    let dataTable = new google.visualization.DataTable();
    dataTable.addColumn('string', 'Element');
    for (let e of columns) {
      dataTable.addColumn("number", e);
    }
    for (let e of data) {
      let row = [e.empty];
      for (const [key, value] of Object.entries(e)) {
        if (columns.includes(key)) {
          row.push(value);
        }
      }
      dataTable.addRow(row);
    }

    return dataTable;
  }

  function getHistDataTable(columns, data) {
    let dataTableHist = new google.visualization.DataTable();
    dataTableHist.addColumn('string', 'Element');
    dataTableHist.addColumn("number", "Single Matchup");
    
    for (let e of data) {
      for (const [key, value] of Object.entries(e)) {
        if (columns.includes(key)) {
          let row = [e.empty + " | " + key];
          row.push(value);
          dataTableHist.addRow(row);
        }
      }
    }

    return dataTableHist;
  }

function drawScatterChart(dataTable) {
    addPngDownloadToChart(scatterChart, "chart1-png-download", $('#select-catcher').select2('data')[0].text.replaceAll(' ', '_') +"-"+ $('#select-pitcher').select2('data')[0].text.replaceAll(' ', '_') +"-scatter-chart.png");
    scatterChart.draw(dataTable, options);
}

function drawLineChart(dataTable) {
    addPngDownloadToChart(lineChart, "chart2-png-download", $('#select-catcher').select2('data')[0].text.replaceAll(' ', '_') +"-"+$('#select-pitcher').select2('data')[0].text.replaceAll(' ', '_') +"-line-chart.png");
    lineChart.draw(dataTable, options);
}

function drawHistogram(dataTable) {
    addPngDownloadToChart(histogram, "histogram-png-download", $('#select-catcher').select2('data')[0].text.replaceAll(' ', '_') +"-"+$('#select-pitcher').select2('data')[0].text.replaceAll(' ', '_') +"-histogram.png");
    histogram.draw(dataTable, histOptions);
}