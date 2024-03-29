var fetchedData = JSON.parse(localStorage.getItem('fetchedData')),
  completeData;

if (fetchedData === null || version != localStorage.getItem('version')) {
    fetchData();
} else {
    initSite(fetchedData); //gotta do it with if else, as fetching is async. If fetch, then init only after fetch finished.
}

function initSite(data) {
    completeData = combineColumnsWithTable(data);
    setColumnNames();
    setTableData();
    initTable(columnNames, tableData);
    initSelectors();
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
        localStorage.setItem('fetchedData', JSON.stringify(data));
        localStorage.setItem('version', version);
        initSite(data);
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
            var temp_obj = {};
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