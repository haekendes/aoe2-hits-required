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
      function (s) { // 1
        tableData = [];
        setRowData(Object.values(completeData['table'][s.params.data['id']])[0]);
  
        $('#myGrid').height(tableData.length * 25 + 42).trigger('resize');
  
        grid.setData(tableData, true);
        grid.render();
  
        if ($('#select-pitcher').select2('data')[0].text) { // must come before drawCharts()
          initCheckBoxes(columnNames);
        }
        
        if($('#select-pitcher').select2('data')[0].text) {
          drawCharts(tableData);
        }
      },
      function (s) { // 2
        setTableData();
        grid.setData(tableData, true);
        grid.render();
  
        $('#myGrid').height('62.75vh').trigger('resize');
      });
  
      initSelector(selectData, '#select-pitcher', 'Choose a hitting unit', 
      function (s) { // 3
        columnNames = getSingleColumnNames(s.params.data);
        const columns = [{id: "empty", name: "", field: "empty", width: 200}]
        for (let e of columnNames) {
          columns.push({id: e, name: e, field: e, width: 175});
        };
        grid.setColumns(columns);
        
        if ($('#select-catcher').select2('data')[0].text) {
          initCheckBoxes(columnNames);
        }
        
        if($('#select-catcher').select2('data')[0].text) {
          drawCharts(tableData);
        }
      },
      function (s) { // 4
        setColumnNames();
        const columns = [{id: "empty", name: "", field: "empty", width: 200}]
        for (let e of columnNames) {
          columns.push({id: e, name: e, field: e, width: 175});
        };
        grid.setColumns(columns);
      });
    });
  }
  
  function initSelector(selectData, id, placeholderText, onSelect, onUnselect) {
    $(id).select2({
      placeholder: placeholderText,
      allowClear: true,
      data: selectData
    });
    $(id).on('select2:select', onSelect);
    $(id).on('select2:unselect', onUnselect);
  }
  