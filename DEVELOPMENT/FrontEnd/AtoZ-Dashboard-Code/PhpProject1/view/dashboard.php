<?php
include_once("../controller/default_controller.php");  
$default_controller = new default_controller();  
?>

<!DOCTYPE html>
<!--
To change this license header, choose License Headers in Project Properties.
To change this template file, choose Tools | Templates
and open the template in the editor.
-->
<html>
    <head>
        <title>Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" type="text/css" href="../view/css/pie_chart.css"/>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript" src="../view/default_chart.js.php"></script>
        <script type="text/javascript" src="../view/draw_pie_chart.js"></script>
        <script>
            google.charts.load('current', {'packages':['corechart']});  
            google.charts.load('current', {'packages':['table']});
            google.charts.setOnLoadCallback(default_piechart);
            google.charts.setOnLoadCallback(default_table_pie_chart);
        </script>
    </head>
    <body>
        <!---   
        
        Pie Chart
        
        --->
        <div id="current_pie_segment_div">
            <p>Selected Segment:</p>
            <p id="current_pie_segment"></p>
        </div>
        <div id="year_selector_pie">
            Year:   <select name="pie_year">
                        <option value="">Choose year</option>
                        <?php $default_controller->list_year_pie_chart();?>   
                    </select>
        </div>
        <div id="year_select_pie_apply">    
            <button onclick="pie_chart();pie_chart_table();">Apply</button>
        </div>    
        <div id="pie_chart"></div>
        <div id="pie_chart_table"></div>
        <div id="pie_chart_data_export">
            <form action="../controller/export_controller.php" method="POST">
                <input type="hidden" id="year_pie" name="year_pie" <?php $default_controller->latest_year_pie_chart();?>/>
                <input type="hidden" id="segment_pie" name="segment_pie" <?php $default_controller->largest_segment_pie_chart();?>/>
                <input type="submit" name="export" value="CSV Export">
            </form>    
        </div>  
    </body>
</html>
