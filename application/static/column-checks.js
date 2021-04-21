var checkDiv = document.getElementById('check-div');

//show & hide functions in charts.js

function initCheckBoxes(columns) {
    checkDiv.innerHTML = '';
    for (e of columns) {
        new_div = document.createElement("div");
        new_div.classList.add("animate__animated", "animate__fadeIn", "mb-auto");
        new_div.innerHTML = '<div class="mx-2 custom-control custom-checkbox">'
        +'<input class="custom-control-input" type="checkbox" id="'+e+'Checkbox" value="'+ e +'" checked>'
        +'<label class="custom-control-label" for="'+e+'Checkbox">'+ e +'</label>'
        +'</div>'
        checkDiv.appendChild(new_div);
    }

    let checkboxes = document.querySelectorAll("input[type=checkbox]");
    let checkedColumns = [];

    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
        checkedColumns = 
            Array.from(checkboxes) // Convert checkboxes to an array to use filter and map.
            .filter(i => i.checked) // Use Array.filter to remove unchecked checkboxes.
            .map(i => i.value) // Use Array.map to extract only the checkbox values from the array of objects.

            if ($('div.custom-checkbox :checkbox:checked').length > 0) {
                redrawCharts(checkedColumns, tableData);
            }
        });
  });
}