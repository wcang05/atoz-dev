<?php
    header("Content-Type: application/javasctipt");
    include_once("../controller/default_bar_controller.php");  
    $default_bar_controller = new default_bar_controller(); 
?>
    function default_barchart(){  
        // Get the value for year
        var year = document.getElementById("year_bar").value;
        
        // Get the segment name
        var segment_bar = document.getElementById("segment_bar").value;

        var data = google.visualization.arrayToDataTable([  
            //Column name
            ['segname', 'head_count'],  

            //for loop to generate rows from pre-defiend SQL
            <?php $default_bar_controller->default_bar_chart();?>
        ]);  
        var options = { 
              //bar chart title
              title: "Customer Lifetime value Base on Total Spending on year "+year,
              height: 325,
              width: 650
             };         
        //Define container id to draw the chart     
        var default_barchart = new google.visualization.BarChart(document.getElementById('bar_chart'));  

        //Draw the chart
        default_barchart.draw(data, options); 
        
        // Tell users which segment is selected
        if(segment_bar == "Low"){
            document.getElementById("current_bar_segment_div").style.backgroundColor = "blue";
            document.getElementById("current_bar_segment_div").style.color = "white";
        }else if(segment_bar == "Medium"){
            document.getElementById("current_bar_segment_div").style.backgroundColor = "red";
            document.getElementById("current_bar_segment_div").style.color = "white";
        }else if(segment_bar == "Average"){
            document.getElementById("current_bar_segment_div").style.backgroundColor = "orange";
            document.getElementById("current_bar_segment_div").style.color = "black";
        }else if(segment_bar == "High"){
            document.getElementById("current_bar_segment_div").style.backgroundColor = "green";
            document.getElementById("current_bar_segment_div").style.color = "white";
        }else if(segment_bar == "Very High"){
            document.getElementById("current_bar_segment_div").style.backgroundColor = "purple";
            document.getElementById("current_bar_segment_div").style.color = "white";
        }
        
        // Print the selected segment name
        document.getElementById("current_bar_segment").innerHTML = segment_bar;

        // Set the selected default bar chart segment
        default_barchart.setSelection([{row: 0}]); 
        
        function genTableBySeg() {
            var selectedItem = default_barchart.getSelection()[0];

            if (selectedItem) {
                // Get segment name
                var segment_bar = data.getValue(selectedItem.row, 0);

                // Tell users which segment is selected
                if(segment_bar == "Low"){
                    document.getElementById("current_bar_segment_div").style.backgroundColor = "blue";
                    document.getElementById("current_bar_segment_div").style.color = "white";
                }else if(segment_bar == "Medium"){
                    document.getElementById("current_bar_segment_div").style.backgroundColor = "red";
                    document.getElementById("current_bar_segment_div").style.color = "white";
                }else if(segment_bar == "Average"){
                    document.getElementById("current_bar_segment_div").style.backgroundColor = "orange";
                    document.getElementById("current_bar_segment_div").style.color = "black";
                }else if(segment_bar == "High"){
                    document.getElementById("current_bar_segment_div").style.backgroundColor = "green";
                    document.getElementById("current_bar_segment_div").style.color = "white";
                }else if(segment_bar == "Very High"){
                    document.getElementById("current_bar_segment_div").style.backgroundColor = "purple";
                    document.getElementById("current_bar_segment_div").style.color = "white";
                }

                // Save the segment name in hidden input
                document.getElementById("segment_bar").value = segment_bar;

                // Print the selected segment name
                document.getElementById("current_bar_segment").innerHTML = segment_bar; 

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
           xhttp.open("GET", "../controller/draw_bar_chart_controller.php?action=draw_table&year="+year+"&segname="+segment_bar, true);
           xhttp.send();
           }
       }

        // Enable bar chart event listener 
        google.visualization.events.addListener(default_barchart, 'select', genTableBySeg);
    } 
    
function default_table_bar_chart(){
        var data = google.visualization.arrayToDataTable([  
        //Column name
        ['Firtname', 'Lastname', 'PCode', 'Cpny/ Ind', 'Min_Spt_Gap', 'Max_Spt_Gap', 'Avg_Spt_Gap', 'Ttl_Spt_Amt', 'Ave_Spt_AmtBuy_Cat', 'Year'],  

        <?php $default_bar_controller->default_bar_chart_table();?> 
        ]);  

        //Define container id to draw the table     
        var default_table = new google.visualization.Table(document.getElementById('bar_chart_table'));

        //Draw the table
        default_table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});                    
    }    
    
