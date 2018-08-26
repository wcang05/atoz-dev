<?php
include_once("../controller/default_pie_controller.php");  
$default_pie_controller = new default_pie_controller();  

include_once("../controller/default_bar_controller.php");  
$default_bar_controller = new default_bar_controller();  
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
        <link rel="stylesheet" type="text/css" href="../view/css/bar_chart.css"/>
        <link rel="stylesheet" type="text/css" href="../view/css/multiple_bar_chart.css"/>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript" src="../view/default_pie_chart.js.php"></script>
        <script type="text/javascript" src="../view/draw_pie_chart.js"></script>
        <script type="text/javascript" src="../view/default_bar_chart.js.php"></script>
        <script type="text/javascript" src="../view/draw_bar_chart.js"></script>
        <script>
            google.charts.load('current', {'packages':['corechart']});  
            google.charts.load('current', {'packages':['table']});
            google.charts.setOnLoadCallback(default_piechart);
            google.charts.setOnLoadCallback(default_table_pie_chart);
            google.charts.setOnLoadCallback(default_barchart);
            google.charts.setOnLoadCallback(default_table_bar_chart);
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
                        <?php $default_pie_controller->list_year_pie_chart();?>   
                    </select>
        </div>
        <div id="year_select_pie_apply">    
            <button onclick="pie_chart();pie_chart_table();">Apply</button>
        </div>    
        <div id="pie_chart"></div>
        <div id="pie_chart_table"></div>
        <div id="pie_chart_data_export">
            <form action="../controller/export_controller.php" method="POST">
                <input type="hidden" id="year_pie" name="year_pie" <?php $default_pie_controller->latest_year_pie_chart();?>/>
                <input type="hidden" id="segment_pie" name="segment_pie" <?php $default_pie_controller->largest_segment_pie_chart();?>/>
                <input type="submit" name="export" value="CSV Export">
            </form>    
        </div>  
        <!---   
        
        Bar Chart
        
        --->
        <div id="current_bar_segment_div">
            <p>Selected Segment:</p>
            <p id="current_bar_segment"></p>
        </div>
        <div id="year_selector_bar">
            Year:   <select name="bar_year">
                        <option value="">Choose year</option>
                        <?php $default_bar_controller->list_year_bar_chart();?>   
                    </select>
        </div>
        <div id="year_select_bar_apply">    
            <button onclick="bar_chart();bar_chart_table();">Apply</button>
        </div>    
        <div id="bar_chart"></div>
        <div id="bar_chart_table"></div>
        <div id="bar_chart_data_export">
            <form action="../controller/export_controller.php" method="POST">
                <input type="hidden" id="year_bar" name="year_bar" <?php $default_bar_controller->latest_year_bar_chart();?>/>
                <input type="hidden" id="segment_bar" name="segment_bar" <?php $default_bar_controller->largest_segment_bar_chart();?>/>
                <input type="submit" name="export" value="CSV Export">
            </form>    
        </div>  
        
    </body>
</html>
