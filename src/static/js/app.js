

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
	  console.log(station.available_bikes, station.bike_stands);
 var marker = new google.maps.Marker({
 position : {
 lat : station.position_latitude,
 lng : station.position_longitude
 },
 map : map,
 icon: defineMarker(station.available_bikes,station.bike_stands),
 title : station.station_name+" Station Number :"+ station.station_number
 });
marker.metadata = {type: "point", id: station.station_number};
                google.maps.event.addListener(marker, 'click', (function(marker, stations) {
                    return function() {
                        if (parseInt(station.banking) == 0) {
                            station.banking = "No";
                        } else {
                            station.banking = "Yes";
                        }
						var station_number = station.station_number;
                    	var content = "Station name: " + station.station_name + "<br>" + "Station number: " + station.station_number + "<br>" + "Address: " + station.station_address + "<br>" + "Banking" +station.banking +"<br>";
                        var button = "<button onclick='showDiv(); getOccupancy(" + station_number + ")'>Click here for more detailed information!</button>";
                        infoWindow.setContent(content + "<br> " + button);
                        infoWindow.open(map, marker);
                    }
                })(marker, stations));
            })
        })
        .fail(function() {
            console.log("error");
        })
}


showStationMarkers();

function defineMarker(bikes, stands) {
    //function which defines the color of the marker, depending on the occupancy of the station
	console.log(bikes,stands);
       
            //sliderChecked shows the user the number of available bikes at each station
            if ((bikes/stands)<=0.3) {
                return '../static/images/green1.png'            }
        else if (bikes/stands<=0.6) {
                return '../static/images/yellow1.png'
            } else {
                return '../static/images/red1.png'
            }
      
         
        
    }

function showDiv(){
    div = document.getElementById("display");
    div.style.display = "inline-block";
}


function getOccupancy(station_number) {
    document.getElementById("availability").style.display = "inline-block";
    var jqxhr = $.getJSON("/station_details?station_number=" + station_number, function(data){
        var station_details = data.stations;
        _.forEach(station_details, function(station){
            var content = "<b><u>Station:</u></b> <br><br> Address: " + station.station_address + "<br><br>" + "<b><u>Currently there are: </u></b><br><br> Bikes available: " + station.available_bikes +"<br>" + "Bike stands available: " + station.available_bike_stands + "<br>";
            document.getElementById("availability").innerHTML = content;
        })
    });}

