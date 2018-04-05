    window.onload = dropdownSelect();
    function dropdownSelect() {
        // Reading the JSON data from Api
        var xmlReq = new XMLHttpRequest();
        
        xmlReq.onreadystatechange = function () 
        {
            if (xmlReq.readyState === XMLHttpRequest.DONE && xmlReq.status === 200) 
          {   
            //storing json data to a variable
            var stat = JSON.parse(xmlReq.responseText); 
            
            var ele = document.getElementById('select');
              
              for (var i = 0; i < stat.length; i++) 
            {
                // populate select element with json data 
                ele.innerHTML = ele.innerHTML +
                '<option value="' + stat[i].number+stat[i].status+'">' + stat[i].address+ '</option>';
                
            }
           } 
              
          };
        
        xmlReq.open("GET", "json_current_data.json", false);
        xmlReq.send(null);
    }


    function show(ele) {
        // get the value for selected <select> element and show the data
        var data = document.getElementById('data');
        var myStr = ele.value;
        var status=myStr.split(' ').pop();
        document.getElementById("data").innerHTML = status;
                console.log(status);
        data.innerHTML = 'Selected station: <b>'+ele.options[ele.selectedIndex].text + '</b> </br>' +
        'ID: <b>' + status + '</b> </br>';
//        'Status: <b>' + ele.value+ '</b> </br>'+
//        'Available bikes: <b>' + ele.value+ '</b> </br>';
    }