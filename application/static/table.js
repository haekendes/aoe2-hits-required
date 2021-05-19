var columnNames,
  tableData,
  tableGrid;

function setColumnNames() {
  columnNames = [];
  const objList = Object.values(Object.values(Object.values(Object.values(completeData['table'])[0])[0])[0])[0];
  for (e of objList) {
    columnNames = columnNames.concat(Object.keys(e));
  }
}

function setRowData(objList) { //receives list of unit rows
  for (bla of objList) {
    for(e in bla) {
      const values = {};
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
  tableData = [];
  for (let e in completeData['table']) {
    setRowData(Object.values(completeData['table'][e])[0]);
    tableData.push("");
  }
  
}

function initTable(colNames, data) {
  const columns = [{id: "empty", name: "", field: "empty", width: 200}];
  for (let e of colNames) {
    columns.push({id: e, name: e, field: e, width: 175});
  }
  
  const options = {
    enableCellNavigation: true,
    enableColumnReorder: false,
    frozenColumn: 0,
  };

  tableGrid = new Slick.Grid($('#myGrid'), data, columns, options);
}
