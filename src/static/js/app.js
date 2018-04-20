var station_number = 1;
var type = 'daily';
var selected_date;
var selected_time;
var date_time;
var hire_or_return;

//Function to display station markers
function showStationMarkers()
{

getWeatherInfo();
var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: new google.maps.LatLng(53.3438, -6.2546),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    // Info window from Google Map API https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple

 var infoWindow = new google.maps.InfoWindow();
var jqxhr = $.getJSON("/stations", function(data) {
    $(".se-pre-con").hide();
var stations = data.stations;
getDropDown(stations);

 //console.log('stations', stations);
 _.forEach(stations, function(station) 
	 {
	  //console.log(station.available_bikes, station.bike_stands);
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
                    	var content = "<b>Station name: " + station.station_name + "<br>" + "Station number: " + station.station_number + "<br>" + "Address: " + station.station_address + "<br>" + "Banking:" +station.banking +"</b><br>";
                        var button = "<button onclick='showDiv(); getOccupancy(" + station_number + ")'><b>More details!</b></button>";
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

//function to get current weather information
function getWeatherInfo(){
   
    var jqxhr =$.getJSON('http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=a333fd4b6cc086808ce5e483c98b85f6',function(data){
   
    var icon = data.weather[0].icon;
    var iconUrl = ("<img src='http://openweathermap.org/img/w/" + icon + ".png'>");
    var weatherdata= "<br><b><u>Weather Details:</u></b> <br><br>Current Weather:" + data.weather[0].description+ "<br> Current Temperature: " + parseInt(data.main.temp - 273) + " &#8451;" +"<br> Wind Speed: " + parseFloat(data.wind.speed * 3.6).toFixed(2) + " km/hr" + "<br>" +iconUrl + "<br>";//alert(weatherdata);
        document.getElementById("weather_info").innerHTML = weatherdata;
});
}

//Function to choose appropriate color for markers
function defineMarker(bikes, stands) {
    //function which defines the color of the marker, depending on the occupancy of the station
	console.log(bikes,stands);
       
            //sliderChecked shows the user the number of available bikes at each station
            if ((bikes/stands)<=0.33) {
                return '../static/images/red1.png'            }
        else if (bikes/stands<=0.66) {
                return '../static/images/yellow1.png'
            } else {
                return '../static/images/green1.png'
            }
      
         
        
    }


function showDiv(){
    $(".se-pre-con").show();
    div = document.getElementById("display");
    div.style.display = "inline-block";
}

//get current occupancy
function getOccupancy(station_number) {
    document.getElementById("availability").style.display = "inline-block";
    var jqxhr = $.getJSON("/station_details?station_number=" + station_number, function(data){
        $(".se-pre-con").hide();
        var station_details = data.stations;
        _.forEach(station_details, function(station){
            var content = "<b><u>Station:</u></b> <br><br>Station Number:" + station.station_number+ "<br> Address: " + station.station_address + "<br><br>" + "<b><u>Currently there are: </u></b><br><br> Bikes available: " + station.available_bikes +"<br>" + "Bike stands available: " + station.available_bike_stands + "<br>";
            document.getElementById("availability").innerHTML = content;
        })
    });}


//dropdown for stations

function getDropDown(stations) {
	var ele = document.getElementById('select');
    
    for (var i = 0; i < stations.length; i++) {
        
        // populate select element with json data
        ele.innerHTML = ele.innerHTML +
            '<option value="' + stations[i].station_number+ '">' + stations[i].station_address + '</option>';

    }
    var ele_date = document.getElementById('select_date');
var corrected_date;
    for (var i = 0; i < 5; i++) {
        var currentDate = new Date(new Date().getTime() + 24*i * 60 * 60 * 1000);
        
        var new_date = String(currentDate.getDate());
        if (new_date.length == 1) {
            new_date= "0" + new_date;
        }
        var new_month =  String(currentDate.getMonth());
        if (new_month.length == 1) {
            new_month="0" + new_month;
        }
        corrected_date=currentDate.getFullYear()  + "-" + new_month + "-" + new_date;
        ele_date.innerHTML = ele_date.innerHTML +
            '<option value="' + corrected_date+  '">' + corrected_date + '</option>';

    }
    var ele_time=document.getElementById('select_time');
    for (var i=0; i<24; i++){
        hour_value= String(i);
        if (hour_value.length == 1){
            hour_value="0" + hour_value;
        }
        ele_time.innerHTML = ele_time.innerHTML +
            '<option value="' + hour_value +  '">' + hour_value + '</option>';
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

    data_daily.addColumn('string', 'Date/time');
    data_daily.addColumn('number', 'Bikes');
    data_daily.addColumn('number', 'Stands');

    data_daily.addRows(allRows);


    //Set chart options
    var options = {'title': 'Daily Averages:', 'width': 450, 'height': 290};

    //instantiate and draw our chart, passing in some options
    var chart =  new google.charts.Bar(document.getElementById('daily_div'));
    chart.draw(data_daily, options);

    $('#dTime').show();
}


function updateType(ele) {
	type = ele.options[ele.selectedIndex].value;
	updateChart(station_number, type);
}

//display the charts
function updateChart() {
    
	$.getJSON("/charts_daily?station_number=" + station_number + "&type=" + type, function(data) {
        $(".se-pre-con").hide();
		google.charts.setOnLoadCallback(drawChart(data));
	});
    
    
}

//get the prediction of bikes/stands
function getPrediction(){
    $.get("/predicted_value?station_number=" + station_number + "&date_time=" + date_time + "&hire_or_return=" + hire_or_return, function(data){
        
        if (parseInt(data) < 0){
            data = String(0);
        }
        if (hire_or_return=="hire"){
            document.getElementById("predicted_bikes").innerHTML="<p> Number of bikes available at given time and date at above station is " + data + "</p>";
        }
        else {
            document.getElementById("predicted_bikes").innerHTML="<p> Number of bike stands available at given time and date at above station is " + data + "</p>";
        }
        
    })
    updateChart();
}

//function called upon clicking submit button to validate data and get the requested details
function show() {
    $(".se-pre-con").show();
    station_number=document.getElementById("select").value;
    
    selected_date=document.getElementById("select_date").value;
    selected_time=document.getElementById("select_time").value;
    var current_date = new Date(new Date().getTime());
   
    
    hire_or_return=document.getElementById("hire_or_return").value;
    date_time = String(selected_date) + ' ' + String(selected_time);
   
    if (selected_date == '' || selected_time == '' || hire_or_return=='' || station_number==''){
        alert("Please enter all the details and click submit");
        $(".se-pre-con").hide();
    }
    else if (selected_date.substring(8,) == current_date.getDate()){
        
        if (parseInt(selected_time) <= parseInt(current_date.getHours())){
            alert("Please select valid time. ");
            $(".se-pre-con").hide();
        }
        else {
            document.getElementById("predicted_bikes").innerHTML="Please wait while we fetch the required details";
        getPrediction();
        }
    }
    else
 {
         document.getElementById("predicted_bikes").style.display="inline-block";
        document.getElementById("predicted_bikes").innerHTML="Please wait while we fetch the required details";
        getPrediction();
        
         }
	

}

//function to load page loader
function init() {
    $(".se-pre-con").show();
	showStationMarkers();
}

//function to hide page loader
$(document).ready(function() {
	$('#dTime').hide();
});

window.onload = init();
