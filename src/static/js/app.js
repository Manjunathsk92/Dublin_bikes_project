var map;
function initMap() {
map = new google.maps.Map(document.getElementById('map'), {
center: {lat: -34.397, lng: 150.644},
zoom: 8
});
}

/*function showStationMarkers()
{


    // Info window from Google Map API https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple

 var infoWindow = new google.maps.InfoWindow();
var jqxhr = $.getJSON("/stations", function(data) {
 var stations = data.stations;
 console.log('stations', stations);
 _.forEach(stations, function(station) 
	 {
	  console.log(station.name, station.number);
 var marker = new google.maps.Marker({
 position : {
 lat : station.position_lat,
 lng : station.position_lng
 },
 map : map,
 title : station.name,
 station_number : station.number
 });
 contentString = '<div id="content"><h1>' + station.name + '</h1></div>'
 + '<div id="station_availability"></div>';
 google.maps.event.addListener(marker, 'click', function() {
 // what is the “this” variable when drawInfoWindowChart is called?
 drawInfoWindowChart(this);
 });
 })
 })
 .fail(function() {
 console.log( "error" );
 })
}*/

showStationMarkers();
