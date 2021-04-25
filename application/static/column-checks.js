var checkDiv = document.getElementById('check-form');

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

    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {

            drawCharts(tableData);
            
        });
  });
}