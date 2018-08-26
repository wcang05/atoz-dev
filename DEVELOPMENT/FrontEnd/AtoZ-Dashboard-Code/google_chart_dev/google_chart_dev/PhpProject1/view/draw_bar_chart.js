// Call function to draw google chart.
google.charts.load('current', {'packages':['corechart']});  
google.charts.setOnLoadCallback(bar_chart);

function bar_chart() {
    
    // Get the value for year
    var year = document.getElementsByName("bar_year")[0].value;  
    
    var xhttp;    

    // If year is not define, do nothing.
    if (year == "") {
        return;
    } 
     
    // Launch new request to backend
    xhttp = new XMLHttpRequest();
    
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {    // If request finished and response is ready/ OK
        
        // Load the JSON data in the table
        var data = new google.visualization.DataTable(this.responseText);
        
        // Chart option
        var options = {
                    title: 'Customer Lifetime value Base on Total Spending on year '+year,
                    height: 325,
                    width: 650
                    };

        // Instantiate and draw our chart, passing in some options.
        var bar_chart = new google.visualization.BarChart(document.getElementById('bar_chart'));  
        bar_chart.draw(data, options);
        
        // Set the selected default bar chart segment
        bar_chart.setSelection([{row: 0}]); 
        var selected = bar_chart.getSelection()[0];
        var segment = data.getValue(selected.row, 0);
        if(segment == "Low"){
            document.getElementById("current_bar_segment_div").style.backgroundColor = "blue";
            document.getElementById("current_bar_segment_div").style.color = "white";
        }else if(segment == "Medium"){
            document.getElementById("current_bar_segment_div").style.backgroundColor = "red";
            document.getElementById("current_bar_segment_div").style.color = "white";
        }else if(segment == "Average"){
            document.getElementById("current_bar_segment_div").style.backgroundColor = "orange";
            document.getElementById("current_bar_segment_div").style.color = "black";
        }else if(segment == "High"){
            document.getElementById("current_bar_segment_div").style.backgroundColor = "green";
            document.getElementById("current_bar_segment_div").style.color = "white";
        }else if(segment == "Very High"){
            document.getElementById("current_bar_segment_div").style.backgroundColor = "purple";
            document.getElementById("current_bar_segment_div").style.color = "white";
        }
        
        // Print the selected segment name
        document.getElementById("current_bar_segment").innerHTML = segment;

        // Save the segment name in hidden input
        document.getElementById("segment_bar").value = segment;

        // Save the selected year in hidden input
        document.getElementById("year_bar").value = year;
        
        // Define function to generate table for selected segment
        function genTableBySeg() {
            
            var selectedItem = bar_chart.getSelection()[0];
            
            if (selectedItem) {
                // Get segment name
                var segname = data.getValue(selectedItem.row, 0);
                
                if(segname == "Low"){
                    document.getElementById("current_bar_segment_div").style.backgroundColor = "blue";
                    document.getElementById("current_bar_segment_div").style.color = "white";
                }else if(segname == "Medium"){
                    document.getElementById("current_bar_segment_div").style.backgroundColor = "red";
                    document.getElementById("current_bar_segment_div").style.color = "white";
                }else if(segname == "Average"){
                    document.getElementById("current_bar_segment_div").style.backgroundColor = "orange";
                    document.getElementById("current_bar_segment_div").style.color = "black";
                }else if(segname == "High"){
                    document.getElementById("current_bar_segment_div").style.backgroundColor = "green";
                    document.getElementById("current_bar_segment_div").style.color = "white";
                }else if(segname == "Very High"){
                    document.getElementById("current_bar_segment_div").style.backgroundColor = "purple";
                    document.getElementById("current_bar_segment_div").style.color = "white";
                }
   
                // Print the selected segment name
                document.getElementById("current_bar_segment").innerHTML = segname;
                
                // Save the segment name in hidden input
                document.getElementById("segment_bar").value = segname;
                
                // Launch new request to backend
                xhttp = new XMLHttpRequest();
                
                xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {   // If request finished and response is ready/ OK
                    
                     // Load the JSON data in the table
                    var data = new google.visualization.DataTable(this.responseText);

                    // Instantiate and draw our chart, passing in some options.
                    var table = new google.visualization.Table(document.getElementById('bar_chart_table'));
                    table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
                    }
                }
                
                 // Forward parameters to PHP file
                xhttp.open("GET", "../controller/draw_bar_chart_controller.php?action=draw_table&year="+year+"&segname="+segname, true);
                xhttp.send();
            }
          }
          
        // Enable the bar chart's event listener after its segment being selected 
        google.visualization.events.addListener(bar_chart, 'select', genTableBySeg);
    }
  };
  
  // Forward parameters to PHP file
  xhttp.open("GET", "../controller/draw_bar_chart_controller.php?action=draw_bar_chart&year="+year, true);
  xhttp.send();
}

function bar_chart_table(){
    // Get the value for year
    var year = document.getElementsByName("bar_year")[0].value;  
    
    if (year == "") {
        return;
    } 
    
    var xhttp;   
    
    // Launch new request to backend
    xhttp = new XMLHttpRequest();
    
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {    // If request finished and response is ready/ OK

            // Load the JSON data in the table
            var data = new google.visualization.DataTable(this.responseText);

            // Specify the container for chart drawing
            var default_table_by_year = new google.visualization.Table(document.getElementById('bar_chart_table'));
            default_table_by_year.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
            }
        }
        
         // Forward parameters to PHP file
        xhttp.open("GET", "../controller/draw_bar_chart_controller.php?action=draw_table_by_year&year="+year, true);
        xhttp.send();
    }   
    
   

