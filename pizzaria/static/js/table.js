function getTableRowData(rowId) {
  var table = document.getElementById("myTable");
  var row = table.rows[rowId];
  var data = {
    name: row.cells[0].innerHTML,
    price: row.cells[1].innerHTML,
    size: row.cells[2].innerHTML,
    toppings: row.cells[3].innerHTML
  };

  // Send data to Flask route via AJAX
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/process_data", true);
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
      console.log("Response from server: ", xhr.responseText);
    }
  };
  xhr.send(JSON.stringify(data));
}





