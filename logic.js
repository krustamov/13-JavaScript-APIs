// Store our API endpoint as queryUrl
var queryUrl = "http://127.0.0.1:5000/names";

Plotly.d3.json("/names")
.get(function(data) {
   console.log(data);
})