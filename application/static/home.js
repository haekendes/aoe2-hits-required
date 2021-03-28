var fetchedData,
    columnNames,
    tableData,
    selectData,
    tableElement = document.getElementById("myGrid")
    il = 0;

fetchData();

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
    var data = e.params.data;
    console.log("Catcher: Selected " + data['text']);
    //console.log(data);
    //console.log(columnNames[data['id']]);
    //console.log(Object.values(fetchedData['table'][data['id']])[0]);
    tableData = [];
    innerTableData(Object.values(fetchedData['table'][data['id']])[0]);
    initializeTable(columnNames, tableData);
  });
  $('.select-catcher').on('select2:unselect', function (e) {
    console.log("Catcher: unselected");
    setTableData()
    initializeTable(columnNames, tableData);
  });
  $('.select-pitcher').on('select2:select', function (e) {
    var data = e.params.data;
    console.log("Pitcher: Selected " + data['text']);
    
  });
  $('.select-pitcher').on('select2:unselect', function (e) {
    console.log("Pitcher: unselected");
  });
});
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

function innerTableData(objDict) {
  for(e in objDict) {
    values = {}
    for (i of objDict[e]) {
      for (j of Object.entries(i)) {
        values[j[0]] = j[1];
      }
    }
    values.empty = e;
    tableData.push(values);
  }
}

function setTableData() {
  tableData = []
  for (e in fetchedData['table']) {
    innerTableData(Object.values(fetchedData['table'][e])[0]);
    tableData.push("");
  }
  
}

function setColumnData() {
  columnNames = []
  objList = Object.values(Object.values(Object.values(fetchedData['table'])[0])[0])[0];
  for (e of objList) {
    columnNames = columnNames.concat(Object.keys(e));
  }
}

function initializeTable(colNames, data) {
    var grid;
    var columns = [{id: "empty", name: "", field: "empty", minWidth: 150}]
    for (e of colNames) {
      columns.push({id: e, name: e, field: e, minWidth: 150});
    };
    
  
    var options = {
      editable: false,
      enableAddRow: false,
      enableCellNavigation: true,
      enableColumnReorder: false,
      frozenColumn: 0,
    };
  
    grid = new Slick.Grid(tableElement, data, columns, options);
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
            fetchedData = data;

            setColumnData();
            //console.log(columnNames);
            setTableData();
            console.log(fetchedData['table']);
            console.log(tableData)
            initializeTable(columnNames, tableData);

            setSelectData(columnNames);
            initSelectors();
          });
        }
      )
      .catch(function(err) {
        console.log('Fetch Error :-S', err);
      });
}