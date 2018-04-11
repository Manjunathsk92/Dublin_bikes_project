
function showStationMarkers()
{
var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: new google.maps.LatLng(53.3438, -6.2546),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    // Info window from Google Map API https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple

 var infoWindow = new google.maps.InfoWindow();
var jqxhr = $.getJSON("/stations", function(data) {
 var stations = data.stations;
 console.log('stations', stations);
 _.forEach(stations, function(station) 
	 {
//	  console.log(station.name, station.number);
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
 // what is the “this” variable when drawInfoWindowChart is called?
 drawInfoWindowChart(this);
 });
 })
 })
 .fail(function() {
 console.log( "error" );
 })
}

showStationMarkers();
