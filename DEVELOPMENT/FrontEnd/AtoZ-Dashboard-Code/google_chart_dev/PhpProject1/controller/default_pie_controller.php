<?php 
include_once("../model/db_connect.php");  
include("../model/default_pie_model.php");  

// These php code act as controller for default parameters.
  
class default_pie_controller {  
      
        public function list_year_pie_chart(){  
            default_pie_parameters::list_year_pie_chart();
        }  
        public function latest_year_pie_chart(){  
            default_pie_parameters::latest_year_pie_chart();
        }  
        public function largest_segment_pie_chart(){  
            default_pie_parameters::largest_segment_pie_chart();
        } 
        public function default_pie_chart(){
            default_pie_charts::default_pie_chart();
        }
        public function default_pie_chart_table(){
            default_pie_charts::default_pie_chart_table();
        }
    }    
?>
