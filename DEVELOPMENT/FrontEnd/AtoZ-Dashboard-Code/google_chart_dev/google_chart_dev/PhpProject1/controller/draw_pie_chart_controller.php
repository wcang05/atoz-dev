<?php 
    include("../model/db_connect.php");  
    include("../model/pie_chart_model.php");  
    
    // These php code act as controller for draw pie chart
    
    class draw_pie_chart_controller{
        public static function draw_pie_chart(){
            $action = $_GET['action'];
            
            if($action=="draw_table"){
                $year = $_GET['year'];
                $segname = $_GET['segname'];
                draw_charts::draw_table($segname, $year);
            }
            if($action=="draw_pie_chart"){
                $year = $_GET['year'];
                draw_charts::draw_pie_chart($year);
            }
            if($action=="draw_table_by_year"){
                $year = $_GET['year'];
                draw_charts::draw_table_by_year($year);
            }
        }
    }
    
    draw_pie_chart_controller::draw_pie_chart();
?>
