var completeData = JSON.parse(localStorage.getItem('fetchedData')),
  columnNames,
  tableData,
  grid,
  chartIcons = [];

//if (completeData === null || version != localStorage.getItem('version')) {
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