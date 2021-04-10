var completeData = JSON.parse(localStorage.getItem('fetchedData')),
  columnNames,
  tableData;

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

function innerTableData(objDict) { //receives dict of unit rows
  for (bla of objDict) {
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
  for (e in completeData['table']) {
    innerTableData(Object.values(completeData['table'][e])[0]);
    tableData.push("");
  }
  
}

function getSingleColumnData(data) {
  return Object.keys(Object.values(Object.values(Object.values(completeData['table'])[0])[0][0])[0][data['id']]);
}

function setColumnNames() {
  columnNames = []
  const objList = Object.values(Object.values(Object.values(Object.values(completeData['table'])[0])[0])[0])[0];
  for (e of objList) {
    columnNames = columnNames.concat(Object.keys(e));
  }
}

function initTable(colNames, data) {
  const columns = [{id: "empty", name: "", field: "empty", width: 200}]
  for (e of colNames) {
    columns.push({id: e, name: e, field: e, width: 175});
  };
  

  const options = {
    enableCellNavigation: true,
    enableColumnReorder: false,
    frozenColumn: 0,
  };

  const grid = new Slick.Grid(document.getElementById("myGrid"), data, columns, options);
  // TODO autosize column
  /*
  grid.getColumns()[0].width = 250
  console.log(grid.getColumns()[0])
  grid.invalidate();
  */
}

function setSelectData(data) {
  const selectData = [];
  let index = 0;
  for (e in completeData['table']) {
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

    initSelector(selectData, '.select-catcher', 'Choose a unit getting hit', 
    function (e) {
      tableData = [];
      innerTableData(Object.values(completeData['table'][e.params.data['id']])[0]);
      initTable(columnNames, tableData);
    },
    function (e) {
      setTableData()
      initTable(columnNames, tableData);
    });

    initSelector(selectData, '.select-pitcher', 'Choose a hitting unit', 
    function (e) {
      initTable(getSingleColumnData(e.params.data), tableData);
    },
    function (e) {
      initTable(columnNames, tableData);
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
  for (e in data['table']) {
    for (bla of Object.values(data['table'][e])[0]) {
      for(k in bla) {
        var index = 0;
        bla[k].forEach(function(value, i) {
          var temp_obj = {}
          for(number of value) {
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