function showStationMarkers() {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: new google.maps.LatLng(53.3438, -6.2546),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    // Info window from Google Map API https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple

    var infoWindow = new google.maps.InfoWindow();
    var jqxhr = $.getJSON("http://ec2-34-208-241-74.us-west-2.compute.amazonaws.com/stations", null, function(data) {
            var stations = data.stations;
            _.forEach(stations, function(station) {
                var marker = new google.maps.Marker({
                    position: {
                        lat: station.station_loc_lat,
                        lng: station.station_loc_long
                    },
                    map: map,
                    title: station.station_name,
                    station_number: station.station_number
                });
				marker.metadata = {type: "point", id: station.station_number};
                google.maps.event.addListener(marker, 'click', (function(marker, stations) {
                    return function() {
                        if (station.banking_available == 0) {
                            station.banking_available = "No";
                        } else {
                            station.banking_available = "Yes";

                        }

						var station_number = station.station_number;
                    	var content = "Station name: " + station.station_name + "<br>" + "Station number: " + station.station_number + "<br>" + "Address: " + station.station_address + "<br>" + "Banking: " + station.banking_available + "<br>";
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