<?php
    header("Content-Type: application/javasctipt");
    include_once("../controller/default_controller.php");  
    $default_controller = new default_controller(); 
?>
    function default_piechart(){  
        // Get the value for year
        var year = document.getElementById("year_pie").value;
        
        // Get the segment name
        var segment_pie = document.getElementById("segment_pie").value;

        var data = google.visualization.arrayToDataTable([  
            //Column name
            ['segname', 'head_count'],  

            //for loop to generate rows from pre-defiend SQL
            <?php $default_controller->default_pie_chart();?>
        ]);  
        var options = { 
              //Pie chart title
              title: "Customer Lifetime value Base on Total Spending on year "+year
             };         
        //Define container id to draw the chart     
        var default_piechart = new google.visualization.PieChart(document.getElementById('pie_chart'));  

        //Draw the chart
        default_piechart.draw(data, options); 
        
        // Tell users which segment is selected
        if(segment_pie == "Low"){
            document.getElementById("current_pie_segment_div").style.backgroundColor = "blue";
            document.getElementById("current_pie_segment_div").style.color = "white";
        }else if(segment_pie == "Medium"){
            document.getElementById("current_pie_segment_div").style.backgroundColor = "red";
            document.getElementById("current_pie_segment_div").style.color = "white";
        }else if(segment_pie == "Average"){
            document.getElementById("current_pie_segment_div").style.backgroundColor = "orange";
            document.getElementById("current_pie_segment_div").style.color = "black";
        }else if(segment_pie == "High"){
            document.getElementById("current_pie_segment_div").style.backgroundColor = "green";
            document.getElementById("current_pie_segment_div").style.color = "white";
        }else if(segment_pie == "Very High"){
            document.getElementById("current_pie_segment_div").style.backgroundColor = "purple";
            document.getElementById("current_pie_segment_div").style.color = "white";
        }
        
        // Print the selected segment name
        document.getElementById("current_pie_segment").innerHTML = segment_pie;

        // Set the selected default pie chart segment
        default_piechart.setSelection([{row: 0}]); 
        
        function genTableBySeg() {
            var selectedItem = default_piechart.getSelection()[0];

            if (selectedItem) {
                // Get segment name
                var segment_pie = data.getValue(selectedItem.row, 0);

                // Tell users which segment is selected
                if(segment_pie == "Low"){
                    document.getElementById("current_pie_segment_div").style.backgroundColor = "blue";
                    document.getElementById("current_pie_segment_div").style.color = "white";
                }else if(segment_pie == "Medium"){
                    document.getElementById("current_pie_segment_div").style.backgroundColor = "red";
                    document.getElementById("current_pie_segment_div").style.color = "white";
                }else if(segment_pie == "Average"){
                    document.getElementById("current_pie_segment_div").style.backgroundColor = "orange";
                    document.getElementById("current_pie_segment_div").style.color = "black";
                }else if(segment_pie == "High"){
                    document.getElementById("current_pie_segment_div").style.backgroundColor = "green";
                    document.getElementById("current_pie_segment_div").style.color = "white";
                }else if(segment_pie == "Very High"){
                    document.getElementById("current_pie_segment_div").style.backgroundColor = "purple";
                    document.getElementById("current_pie_segment_div").style.color = "white";
                }

                // Save the segment name in hidden input
                document.getElementById("segment_pie").value = segment_pie;

                // Print the selected segment name
                document.getElementById("current_pie_segment").innerHTML = segment_pie; 

                // Launch new request to backend
                xhttp = new XMLHttpRequest();

                xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {   // If request finished and response is ready/ OK
                     // Load the JSON data in the table
                    var data = new google.visualization.DataTable(this.responseText);

                    // Instantiate and draw our chart, passing in some options.
                    var table = new google.visualization.Table(document.getElementById('pie_chart_table'));
                    table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
                }
            }

            // Forward parameters to PHP file
           xhttp.open("GET", "../controller/draw_pie_chart_controller.php?action=draw_table&year="+year+"&segname="+segment_pie, true);
           xhttp.send();
           }
       }

        // Enable pie chart event listener 
        google.visualization.events.addListener(default_piechart, 'select', genTableBySeg);
    } 
    
function default_table_pie_chart(){
        var data = google.visualization.arrayToDataTable([  
        //Column name
        ['Firtname', 'Lastname', 'PCode', 'Cpny/ Ind', 'Min_Spt_Gap', 'Max_Spt_Gap', 'Avg_Spt_Gap', 'Ttl_Spt_Amt', 'Ave_Spt_AmtBuy_Cat', 'Year'],  

        <?php $default_controller->default_pie_chart_table();?> 
        ]);  

        //Define container id to draw the table     
        var default_table = new google.visualization.Table(document.getElementById('pie_chart_table'));

        //Draw the table
        default_table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});                    
    }    
    
