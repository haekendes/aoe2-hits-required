var completeData = JSON.parse(localStorage.getItem('fetchedData')),
  columnNames,
  tableData,
  grid,
  chartIcons = [];

//if (fetchedData === null || version != localStorage.getItem('version')) {
  fetchData();
/*}
else {
  initSite();
}
*/
function initSite() {
  setColumnNames();
  setTableData();
  initTable(columnNames, tableData);
  initSelectors();
}

function hideCharts() {
  for (let e of $('.chart')) {
    e.style.display = 'none';
  }
  for (let e of chartIcons) {
    e.style.display = 'none';
  }
}
function showCharts() {
  for (let e of $('.chart')) {
    e.style.display = 'revert';
  }
}

function showChartInfo() {
  let element = document.getElementById('chart-info');
  element.innerHTML = '<details><summary><i class="bi bi-info-circle"></i></summary><ul> <li>Try to hover over / click on the attack upgrades in the chart&#39;s legend. You can select multiple.</li> <li>You can pan & zoom inside the chart. Right click to reset the view.</li> <li>Each chart can be saved as png.</li> </ul></details>'
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

function charts(columns, data) {
  showChartInfo();

  google.charts.load('current', {packages: ['corechart']});
  google.charts.setOnLoadCallback(drawChart);
  showCharts();

  function drawChart() {
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

    let options = {
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
    let chart1 = new google.visualization.ScatterChart(document.getElementById('chart1'));
    addPngDownloadToChart(chart1, "chart1-png-download", $('#select-catcher').select2('data')[0].text.replaceAll(' ', '_') +"-"+ $('#select-pitcher').select2('data')[0].text.replaceAll(' ', '_') +"-scatter-chart.png");
    chart1.draw(dataTable, options);

    let chart2 = new google.visualization.LineChart(document.getElementById('chart2'));
    addPngDownloadToChart(chart2, "chart2-png-download", $('#select-catcher').select2('data')[0].text.replaceAll(' ', '_') +"-"+$('#select-pitcher').select2('data')[0].text.replaceAll(' ', '_') +"-line-chart.png");
    chart2.draw(dataTable, options);

    let dataTable3 = new google.visualization.DataTable();
    dataTable3.addColumn('string', 'Element');
    dataTable3.addColumn("number", "Single Matchup");
    
    for (let e of data) {
      for (const [key, value] of Object.entries(e)) {
        if (columns.includes(key)) {
          let row = [e.empty + " | " + key];
          row.push(value);
          dataTable3.addRow(row);
        }
      }
    }

    //change options for histogram
    options['colors']= ['#ec8f6e',];
    options['vAxis'] = {
      title: 'Amount of Matchups',
      titleTextStyle: {italic: false, bold: true}
    }
    options['hAxis'] = {
      title: 'Hits required',
      titleTextStyle: {italic: false, bold: true}
    }
    
    
    let chart3 = new google.visualization.Histogram(document.getElementById('chart3'));
    addPngDownloadToChart(chart3, "histogram-png-download", $('#select-catcher').select2('data')[0].text.replaceAll(' ', '_') +"-"+$('#select-pitcher').select2('data')[0].text.replaceAll(' ', '_') +"-histogram.png");
    chart3.draw(dataTable3, options);
  }
}

function getSingleColumnNames(data) {
  return Object.keys(Object.values(Object.values(Object.values(completeData['table'])[0])[0][0])[0][data['id']]);
}

function setColumnNames() {
  columnNames = []
  const objList = Object.values(Object.values(Object.values(Object.values(completeData['table'])[0])[0])[0])[0];
  for (e of objList) {
    columnNames = columnNames.concat(Object.keys(e));
  }
}

function setRowData(objList) { //receives list of unit rows
  for (bla of objList) {
    for(e in bla) {
      const values = {}
      for (i of bla[e]) {
        for (j of Object.entries(i)) {
          values[j[0]] = j[1]; //column_name: numerical_value
        }
      }
      values.empty = e;
      tableData.push(values);
    }
  }
}

function setTableData() {
  tableData = []
  for (let e in completeData['table']) {
    setRowData(Object.values(completeData['table'][e])[0]);
    tableData.push("");
  }
  
}

function initTable(colNames, data) {
  const columns = [{id: "empty", name: "", field: "empty", width: 200}]
  for (let e of colNames) {
    columns.push({id: e, name: e, field: e, width: 175});
  };
  
  const options = {
    enableCellNavigation: true,
    enableColumnReorder: false,
    frozenColumn: 0,
  };

  grid = new Slick.Grid($('#myGrid'), data, columns, options);
}

function setSelectData(data) {
  const selectData = [];
  let index = 0;
  for (let e in completeData['table']) {
    selectData.push({
      id: index,
      text: Object.keys(completeData['table'][e])[0]
    });
    index++;
  }
  return selectData;
}

function initSelectors() {
  const selectData = setSelectData(columnNames);

  $(document).ready(function() {

    initSelector(selectData, '#select-catcher', 'Choose a unit getting hit', 
    function (s) {
      tableData = [];
      setRowData(Object.values(completeData['table'][s.params.data['id']])[0]);

      $('#myGrid').height(tableData.length * 25 + 42).trigger('resize');

      grid.setData(tableData, true);
      grid.render();

      if($('#select-pitcher').select2('data')[0].text) {
        charts(columnNames, tableData);
      }
    },
    function (s) {
      setTableData();
      grid.setData(tableData, true);
      grid.render();

      $('#myGrid').height('62.75vh').trigger('resize');

      hideCharts();
    });

    initSelector(selectData, '#select-pitcher', 'Choose a hitting unit', 
    function (s) {
      columnNames = getSingleColumnNames(s.params.data);
      columnNames.sort();
      const columns = [{id: "empty", name: "", field: "empty", width: 200}]
      for (let e of columnNames) {
        columns.push({id: e, name: e, field: e, width: 175});
      };
      grid.setColumns(columns);
      
      if($('#select-catcher').select2('data')[0].text) {
        charts(columnNames, tableData);
      }
    },
    function (s) {
      setColumnNames();
      const columns = [{id: "empty", name: "", field: "empty", width: 200}]
      for (let e of columnNames) {
        columns.push({id: e, name: e, field: e, width: 175});
      };
      grid.setColumns(columns);

      hideCharts();
    });
  });
}

function initSelector(selectData, className, placeholderText, onSelect, onUnselect) {
  $(className).select2({
    placeholder: placeholderText,
    allowClear: true,
    data: selectData
  });
  $(className).on('select2:select', onSelect);
  $(className).on('select2:unselect', onUnselect);
}

async function fetchData() {
  try {
    const response = await fetch('/get_table', {
      method: 'GET',
    });
    if (response.status !== 200) {
      console.log('Looks like there was a problem. Status Code: ' +
        response.status);
      return;
    }
    response.json().then(function (data) {
      completeData = combineColumnsWithTable(data);
      localStorage.setItem('fetchedData', JSON.stringify(completeData));
      localStorage.setItem('version', version);
      initSite();
    });
  } catch (err) {
    console.log('Fetch Error :-S', err);
  }
}

function combineColumnsWithTable(data) {
  for (let e in data['table']) {
    for (let bla of Object.values(data['table'][e])[0]) {
      for(let k in bla) {
        var index = 0;
        bla[k].forEach(function(value, i) {
          var temp_obj = {}
          for(let number of value) {
            temp_obj[data['columns'][index]] = number;
            index++;
          }
          bla[k][i] = temp_obj;
        })
      }
    }
  }
  return data;
}