<!DOCTYPE html>
<!-- 
To change this license header, choose License Headers in Project Properties.
To change this template file, choose Tools | Templates
and open the template in the editor.
-->
<html>
    <head>
        <title>Dashboard 1</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" type="text/css" href="../view/css/multiple_bar_chart.css"/>
    </head>
    <body>
        <div id="year_selector_multi_bar">
            Year:   <select name="bar_all_year">
                        <option value="">Choose year</option>
                    </select>
        </div>
        <div id="year_select_multi_bar_apply">    
            <button onclick="">Apply</button>
        </div>    
        <!---   
        
        Bar All Charts
        
        --->
        
        <div id="bar_all_chart"></div>
  
        <!---   
        
        Bar Ink Charts
        
        --->
  
        <div id="bar_ink_chart"></div>
   
        <!---   
        
        Bar Toner Charts
        
        --->

        <div id="bar_toner_chart"></div>
        <!---   
        
        Bar Printer Charts
        
        --->
  
        <div id="bar_printer_chart"></div>
        <!---   
        
        Bar Paper Charts
        
        --->

        <div id="bar_paper_chart"></div>
        <!---   
        
        Bar Stationary Charts
        
        --->

        <div id="bar_stationary_chart"></div>
        <!---   
        
        Bar Cleaning Charts
        
        --->
 
        <div id="bar_clean_chart"></div>
        <!---   
        
        Bar Break room Charts
        
        --->
 
        <div id="bar_brk_chart"></div>
        <div id="multi_bar_table"></div>
        <div id="multi_bar_data_export">
            <form action="../controller/export_controller.php" method="POST">
                <input type="hidden" id="year_multi_bar" name="year_bar" />
                <input type="hidden" id="segment_multi_bar" name="segment_bar" />
                <input type="submit" name="export" value="CSV Export">
            </form>    
        </div>  
    </body>    
</html>