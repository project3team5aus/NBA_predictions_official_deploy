console.log('data_year_hoops is: ', data_year_hoops);

var year_tableData = data_year_hoops;
console.log('year_tableData is: ', year_tableData);


// create function called makeTable that will make a table using HTML elements
// argument passed in is the array of data
function make_yearTable(year_tableData) {

console.log(year_tableData);

// create variable called year_table_html that will be used to make the 
// year games table using json from flask

// start with making table border
var year_table_html = "<table border='1|1'>";

// use for loop with tableData to bring in elements for campus_name, address, and zipcode
for (var i = 0; i < year_tableData.length; i++) {
    var y_campus_link = '/year_predictions'
    console.log('y_campus_link is: ', y_campus_link);
    year_table_html+="<tr>";
    // add table data object and align in center for date
    year_table_html+="<td align='center'>"+year_tableData[i].date+"</td>";
    // add table data object and align in center for road team
    year_table_html+="<td align='center'>"+"<div class='col-sm'>"+"<figure class='figure center rounded border-success'>"+"<img class='center team-logo' src="+year_tableData[i].road_team_logo+">"+"<figcaption class='figure-caption text-center'>"+year_tableData[i].road_team+"</figcaption>"+"</figure>"+"</div>"+"</td>";
    //table_html+="<td align='center'>"+"<a href="+campus_link+" target='_blank'>"+tableData[i].date+"</a>"+"</td>";
    year_table_html+="<td align='center'>"+'AT'+"</td>";
    // add table data object and align in center for home team
    year_table_html+="<td align='center'>"+"<div class='col-sm'>"+"<figure class='figure center rounded border-success'>"+"<img class='center team-logo' src="+year_tableData[i].home_team_logo+">"+"<figcaption class='figure-caption text-center'>"+year_tableData[i].home_team+"</figcaption>"+"</figure>"+"</div>"+"</td>";
    // add table data object and align in center for road win prediction
    year_table_html+="<td align='center'>"+year_tableData[i].road_win_prediction+"</td>";
    // end of row
    year_table_html+="</tr>";

}
// end of table creation
year_table_html+="</table>";
// create a full html variable to add column headers (School Name, Address, Zipcode) to the table_html we just created
year_full_html = "<thead><tr><td align='center'><strong>Date</strong></td><td align='center'><strong>Road Team</strong></td><th></th><td align='center'><strong>Home Team</strong></td><td align='center'><strong>Road Team Prediction</strong></td></tr></thead>" + year_table_html;

// access by table id="games-table" from index.html file and populate with values from full_html variable
return document.getElementById("year-games-table").innerHTML = year_full_html;

}



// call function makeTable to render table on HTML page
make_yearTable(year_tableData);