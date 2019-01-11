
console.log('data_hoops is: ', data_hoops);


// PULL IN DATA FROM JSON OBJECT. 
// Assign the data from var data_hoops in index.html; 'data_hoops' is json sent from flask 
// data file is imported at the bottom of index.html
var gamesData = data_hoops;

// Console.log whole data set from data.js to confirm it's been read correctly
console.log(gamesData);
// iterate through json array of game objects
gamesData.forEach(function(game) {
    console.log(game);
});

// select container for today's games
// delete existing rows in container
var gameContainer = d3.select("div#today_games");
d3.selectAll("div#today_games > *").remove();

// loop through game objects in data and populate DOM elements per game
for (var i =0; i < gamesData.length; i++) {

    // // wrap the below game builder inside the loop
    // // ============================================================
    // // // create new Div rows for each game object

    // creates new game row, 
    gamei = gameContainer
        .append('div')
        .attr('id', 'game' + i)
        .classed('row no-gutters', true);

    // divider between game div rows
    gameContainer.append('hr');

    // add first child div column with game time and location
    gamei.append('div')
        .attr('id', 'timeLoc' + i)
        .classed('col-sm-2 vert_align', true)
        // add heading tag for game time
        .append('h6')
        .attr('id', 'time' + i)
        .classed('text-center', true)
        .text("INSERT GAME TIME HERE");

    // update the time text
    d3.select('h6#time' + i).text(gamesData[i].time);

    // adding the second line to the game details div for the game location is not working.
    d3.select("div#timeLoc" + i)
        .append('h6')    
        .attr('id', 'loc' + i)
        .classed('text-center', true)
        .text("INSERT GAME LOCATION HERE");

    // update the game location text
    d3.select('h6#loc' + i).text(gamesData[i].location);

    // create road team div.col
    gamei.append('div')
        .attr('id', 'roadTeam' + i)
        .classed('col-sm', true)
        .append('figure')
        .attr('id','roadFig' + i)
        .classed('figure center', true)
        .append('img')
        .attr('id', 'roadLogo' + i)
        .classed('center team-logo', true);

    d3.select('figure#roadFig' + i).append('figcaption')
        .classed('figure-caption text-center', true)
        .text(gamesData[i].road_team);

    // update the road team logo image
    d3.select('img#roadLogo' + i).attr('src', gamesData[i].road_team_logo);


    // "-- AT --" divider div.col
    gamei.append('div')
        .classed('col-sm-2 vert_align', true)
        .append('p')
        .classed('text-center', true)
        .text('-- AT --');


    // create home team div.col
    gamei.append('div')
        .attr('id', 'homeTeam' + i)
        .classed('col-sm', true)
        .append('figure')
        .attr('id','homeFig' + i)
        .classed('figure center', true)
        .append('img')
        .attr('id', 'homeLogo' + i)
        .classed('center team-logo', true);

    d3.select('figure#homeFig' + i).append('figcaption')
        .classed('figure-caption text-center', true)
        .text(gamesData[i].home_team);

    // update the home team logo image
    d3.select('img#homeLogo' + i).attr('src', gamesData[i].home_team_logo);


    // conditional statment to update team logos with border to indicate win prediction
    // does nothing if value != 'Win'|'Loss'
    if (gamesData[i].road_win_prediction === "Win") {
        d3.select('figure#roadFig' + i).attr('class','figure center rounded border border-success');
    }
    else if (gamesData[i].road_win_prediction === "Loss") {
        d3.select('figure#homeFig' + i).attr('class','figure center rounded border border-success');
    }
    else{};
    // ==================================================================================
};

// select H4 header text for "Today's Date" by id #today_date
// update existing text with the date from one of the game objects
var headerDate = d3.select("#today_date");
// This line will be the default text if no game objects availble
headerDate.text("no games available");
// This override the above with the date from the first game object
headerDate.text(gamesData[0].date);