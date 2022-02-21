var scatterChart,
    lineChart, 
    histogram,
    options,
    histOptions,
    chartIcons = [],
    observer, // global observer var to reduce draw calls upon multiple column select changes
    chart_colors = ['#fadcd1', '#f6c7b6', '#f3b49f','#ec8f6e','#e6693e', '#e05424', '#e0440e', '#c53300', '#942600'];

  google.charts.load('current', {packages: ['corechart']});
  google.charts.setOnLoadCallback(init);

  function init() {
    options = {
      'height': 500,
      colors: chart_colors,
      vAxis: {
        title: 'Hits required',
        titleTextStyle: {italic: false, bold: true},
        minValue: 0,
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
        duration: 330,
        easing: 'inAndOut',
      },
      allowAsync: 'true',
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
    };
    histOptions['hAxis'] = {
      title: 'Hits required',
      titleTextStyle: {italic: false, bold: true}
    };
    
    histogram = new google.visualization.Histogram(document.getElementById('chart3'));
  }


  function drawCharts(data) {
    if(!chartIcons.length) {
      showChartInfoIcon();
      addPngDownloadToChart(scatterChart, "chart1-png-download");
      addPngDownloadToChart(lineChart, "chart2-png-download");
      addPngDownloadToChart(histogram, "histogram-png-download");
    }

    let checkboxes = document.querySelectorAll("input[type=checkbox]");
    let columns = 
              Array.from(checkboxes) // Convert checkboxes to an array to use filter and map.
              .filter(i => i.checked) // Use Array.filter to remove unchecked checkboxes.
              .map(i => i.value); // Use Array.map to extract only the checkbox values from the array of objects.      

    if (columns.length) {
      let redrawTable = getChartDataTable(columns, data);
      let charts = [].slice.call(document.getElementsByClassName("chart"));

      options['colors'] = setOptionColors(columns.length);

      if(observer) {
        charts.forEach(function(chart) {
          observer.unobserve(chart); // remove old observers who haven't been triggered and are now obsolete
        })
      }
      observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {

          if (entry.isIntersecting) {
            if(entry.target.id === 'chart1') {
              scatterChart.draw(redrawTable, options);
              observer.unobserve(entry.target);
            }
            else if (entry.target.id === 'chart2') {
              lineChart.draw(redrawTable, options);
              observer.unobserve(entry.target);
            } 
            else if (entry.target.id === 'chart3') {
              histogram.draw(getHistDataTable(columns, data), histOptions);
              observer.unobserve(entry.target);
            }
          }
        });
      }, 
      {threshold: 0.5});

      charts.forEach(function(chart) {
        observer.observe(chart);
      })
  }
}

function setOptionColors(columns_length) {
  switch(columns_length) {
    case 0:
      return;
    case 1:
      return [chart_colors[3]];
    case 2:
      return [chart_colors[2], chart_colors[6]];
    case 3: 
      return [chart_colors[1], chart_colors[3], chart_colors[7]];
    case 4: 
      return chart_colors.filter((x, i) => i % 2);
    case 5:
      return chart_colors.slice(1,6);
    case 6:
      return chart_colors.slice(1,7);
    case 7:
      return chart_colors.slice(1);
    case 8:
      return chart_colors;
    case 9:
      return chart_colors;
  }
}

function showChartInfoIcon() {
  let element = document.getElementById('chart-info');
  element.innerHTML = '<details><summary><i class="bi bi-info-circle"></i></summary><ul> <li>After loading the site, try pressing tab+enter+enter, then again tab+enter+enter and see what happens. <br>You can use this to quickly select units with keyboard only.</li><li>Try to hover over / click on the attack upgrades in the chart&#39;s legend. You can select multiple.</li> <li>You can pan & zoom inside the chart. Right click to reset the view.</li> <li>Each chart can be saved as png.</li><li>Your checkbox choice is saved depending on the checkbox position, not on attack upgrade.<br>It also stays saved if you leave the session.</li><li>Charts are updated only if scrolled into view.</li> </ul></details>';
  element.title = "Information";
  element.style.display = 'table';
  element.classList.add("chart-info", "animate__animated", "animate__backInRight");
  chartIcons.push(element);
}

function addPngDownloadToChart(chart, id) {
  let element = document.getElementById(id);

  element.addEventListener("click", function() {
    var link = document.createElement("a");
    link.download = $('#select-catcher').select2('data')[0].text.replaceAll(' ', '_') +"-"+ $('#select-pitcher').select2('data')[0].text.replaceAll(' ', '_') +"-scatter-chart.png";
    link.href = chart.getImageURI();
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    delete link;
  }); 

  element.innerHTML = '<a style="margin-right: 32px;"><i class="bi bi-card-image"></i><i class="bi bi-download"></i></a>';
  element.title = "Save chart as png";
  element.style.display = 'revert';
  element.classList.add("png-download", "animate__animated", "animate__backInRight");
  chartIcons.push(element);
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
