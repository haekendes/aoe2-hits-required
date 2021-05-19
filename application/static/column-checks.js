var checkDiv = document.getElementById('check-form');

//show & hide functions in charts.js

function initCheckBoxes(columns) {
    let columnCheckStatus = localStorage.getItem('columnCheckStatus');
    if (columnCheckStatus === null) {
        localStorage.setItem('columnCheckStatus', JSON.stringify([1,1,1,1,1,1,1,1,1]));
    }

    checkDiv.innerHTML = '';
    columns.forEach(function(e, i) {
        let checked = '';
        if(JSON.parse(localStorage.getItem('columnCheckStatus'))[i]) {
            checked = 'checked';
        }

        new_div = document.createElement("div");
        new_div.classList.add("animate__animated", "animate__fadeIn", "mb-auto");
        new_div.innerHTML = '<div class="mx-2 custom-control custom-checkbox">'
        +'<input class="custom-control-input" type="checkbox" id="'+e+'Checkbox" value="'+ e +'" '+checked+'>'
        +'<label class="custom-control-label" for="'+e+'Checkbox">'+ e +'</label>'
        +'</div>';
        checkDiv.appendChild(new_div);
    });

    let checkboxes = document.querySelectorAll("input[type=checkbox]");

    checkboxes.forEach(function(checkbox, i) {
        checkbox.addEventListener('change', function() {
            tempList = JSON.parse(localStorage.getItem('columnCheckStatus'));
            if (this.checked) {
                tempList[i] = 1;
            } else {
                tempList[i] = 0;
            }
            localStorage.setItem('columnCheckStatus', JSON.stringify(tempList));
            drawCharts(tableData);
        });
  });
}