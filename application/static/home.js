var fetchedData,
    columnNames,
    tableData,
    selectData,
    tableElement = document.getElementById("myGrid");

fetchData();

function initSite() {
  setColumnData();
  setTableData();
  initializeTable(columnNames, tableData);

  setSelectData(columnNames);
  initSelectors();
}

function initSelectors() {
$(document).ready(function() {
  $('.select-catcher').select2({
    placeholder: 'Choose a unit getting hit',
    allowClear: true,
    data: selectData
  });
  $('.select-pitcher').select2({
    placeholder: 'Choose a hitting unit',
    allowClear: true,
    data: selectData
  });
  $('.select-catcher').on('select2:select', function (e) {
    select1 = e.params.data;
    tableData = [];
    innerTableData(Object.values(fetchedData['table'][select1['id']])[0]);
    initializeTable(columnNames, tableData);
  });
  $('.select-catcher').on('select2:unselect', function (e) {
    console.log("Catcher: unselected");
    setTableData()
    initializeTable(columnNames, tableData);
  });
  $('.select-pitcher').on('select2:select', function (e) {
    select2 = e.params.data;
    console.log("Pitcher: Selected " + select2['text']);
    setSingleColumnData(select2);
    initializeTable(columnNames, tableData);
  });
  $('.select-pitcher').on('select2:unselect', function (e) {
    console.log("Pitcher: unselected");
    setColumnData()
    initializeTable(columnNames, tableData);
  });
});
}

function innerTableData(objDict) { //receives dict of unit rows
  for (bla of objDict) {
    for(e in bla) {
      values = {}
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
  for (e in fetchedData['table']) {
    innerTableData(Object.values(fetchedData['table'][e])[0]);
    tableData.push("");
  }
  
}

function setSingleColumnData(data) {
  obj = Object.values(Object.values(Object.values(fetchedData['table'])[0])[0][0])[0][data['id']];
  columnNames = (Object.keys(obj));
}

function setColumnData() {
  columnNames = []
  objList = Object.values(Object.values(Object.values(Object.values(fetchedData['table'])[0])[0])[0])[0];
  for (e of objList) {
    columnNames = columnNames.concat(Object.keys(e));
  }
}

function setSelectData(data) {
  selectData = []
  index = 0;
  for (e in fetchedData['table']) {
    selectData.push({
      id: index,
      text: Object.keys(fetchedData['table'][e])[0]
    });
    index++;
  }
}

function initializeTable(colNames, data) {
    var grid;
    var columns = [{id: "empty", name: "", field: "empty", minWidth: 200}]
    for (e of colNames) {
      columns.push({id: e, name: e, field: e, minWidth: 175});
    };
    
  
    var options = {
      enableCellNavigation: true,
      enableColumnReorder: false,
      frozenColumn: 0,
    };
  
    grid = new Slick.Grid(tableElement, data, columns, options);
    //grid.getColumns()[0].width = 250
    //console.log(grid.getColumns()[0])
    //grid.invalidate();
  }

function combineData(data) {
  for (e in data['table']) {
    innerTable = Object.values(data['table'][e])[0];
    for (bla of innerTable) {
      for(e in bla) {
        var index = 0;
        bla[e].forEach(function(value, i) {
          var temp_obj = {}
          for(number of value) {
            temp_obj[data['columns'][index]] = number;
            index += 1;
          }
          bla[e][i] = temp_obj;
        })
      }
    }
  }

  return data;
}

function fetchData() {
    return fetch('/get_table', {
        method: 'GET',
    }).then(
        function(response) {
          if (response.status !== 200) {
            console.log('Looks like there was a problem. Status Code: ' +
              response.status);
            return;
          }
    
          // Examine the text in the response
          response.json().then(function(data) {
            fetchedData = combineData(data);
            initSite();
          });
        }
      )
      .catch(function(err) {
        console.log('Fetch Error :-S', err);
      });
}