var station_number = 1;
var type = 'daily';

function showStationMarkers() {
	var map = new google.maps.Map(document.getElementById('map'), {
       zoom: 13,
       center: new google.maps.LatLng(53.3438, -6.2546),
       mapTypeId: google.maps.MapTypeId.ROADMAP
   	});

   // Info window from Google Map API https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple

	var infoWindow = new google.maps.InfoWindow();
	let stations;
	$.getJSON("/stations", function(data) {
		stations = data.stations;
		console.log('stations', stations);
		getDropDown(stations);
		_.forEach(stations, function(station) {
			console.log(station.name, station.number);
			var marker = new google.maps.Marker({
				position : {
					lat : station.position_latitude,
					lng : station.position_longitude
				},
				map : map,
				title : station.station_name,
				station_number : station.station_number
			});
			contentString = '<div id="content"><h1>' + station.station_name + '</h1></div>'
			+ '<div id="station_availability"></div>';
			google.maps.event.addListener(marker, 'click', function() {
				// what is the �this� variable when drawInfoWindowChart is called?
				drawInfoWindowChart(this);
			});
		})
	})
	.fail(function() {
		console.log( "error" );
	});
}

//dropdown for stations

function getDropDown(stations) {
	let ele = document.getElementById('select');

    for (let i = 0; i < stations.length; i++) {
        // populate select element with json data
        ele.innerHTML = ele.innerHTML +
            '<option value="' + stations[i].station_number+ '">' + stations[i].station_address + '</option>';

    }
}

function drawChart(data) {
    //var array = JSON.parse(data_array);
    let data_array_bikes;
    let data_array_stands;

    let allRows = [];

    for (d of data.stations) {
        allRows.push([d.date_formatted, d.avg_bikes, d.avg_stands]);
    }

    var data_daily = new google.visualization.DataTable(data_array_bikes);

    data_daily.addColumn('string', 'Date');
    data_daily.addColumn('number', 'Bikes');
    data_daily.addColumn('number', 'Stands');

    data_daily.addRows(allRows);


    //Set chart options
    var options = {'title': 'Daily Averages:', 'width': 700, 'height': 550};

    //instantiate and draw our chart, passing in some options
    var chart = new google.charts.Bar(document.getElementById('daily_div'));
    chart.draw(data_daily, options);

    $('#dTime').show();
}

function updateType(ele) {
	type = ele.options[ele.selectedIndex].value;
	updateChart(station_number, type);
}

function updateChart() {
	$.getJSON("/charts_daily?station_number=" + station_number + "&type=" + type, function(data) {
		google.charts.setOnLoadCallback(drawChart(data));
	});
}

function show(ele) {
	station_number = ele.options[ele.selectedIndex].value;
	updateChart();

}


function init() {
	showStationMarkers();
}

$(document).ready(function() {
	$('#dTime').hide();
});

window.onload = init();


//pageloader
$(window).load(function() {
		// Animate loader off screen
		$(".se-pre-con").fadeOut("slow");
	});