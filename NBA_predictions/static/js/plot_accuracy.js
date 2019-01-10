
// list passed from flask
console.log('value of predict_results_list is: ', predict_results_list);

// build Pie chart for Model Accuracy
var accuracy_trace = {
  labels: ["Correct", "Incorrect"],
  values: predict_results_list,
  type: 'pie'
};

var accuracy_data = [accuracy_trace];

var accuracy_layout = {
  title: 'NBA 2019 Games Model Prediction Accuracy',
};

// Plot chart
Plotly.newPlot("nba-pie", accuracy_data, accuracy_layout ,{responsive: true});

