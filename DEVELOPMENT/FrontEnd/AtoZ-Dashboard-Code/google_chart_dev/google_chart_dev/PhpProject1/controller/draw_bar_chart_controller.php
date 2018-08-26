<?php 
    include("../model/db_connect.php");  
    include("../model/bar_chart_model.php");  
    
    // These php code act as controller for draw bar chart
    
    class draw_bar_chart_controller{
        public static function draw_bar_chart(){
            $action = $_GET['action'];
            
            if($action=="draw_table"){
                $year = $_GET['year'];
                $segname = $_GET['segname'];
                draw_charts::draw_table($segname, $year);
            }
            if($action=="draw_bar_chart"){
                $year = $_GET['year'];
                draw_charts::draw_bar_chart($year);
            }
            if($action=="draw_table_by_year"){
                $year = $_GET['year'];
                draw_charts::draw_table_by_year($year);
            }
        }
    }
    
    draw_bar_chart_controller::draw_bar_chart();
?>
