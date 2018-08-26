<?php 
include_once("../model/db_connect.php");    
include("../model/default_bar_model.php");  

// These php code act as controller for default parameters.
  
class default_bar_controller {  
      
        public function list_year_bar_chart(){  
            default_bar_parameters::list_year_bar_chart();
        }  
        public function latest_year_bar_chart(){  
            default_bar_parameters::latest_year_bar_chart();
        }  
        public function largest_segment_bar_chart(){  
            default_bar_parameters::largest_segment_bar_chart();
        } 
        public function default_bar_chart(){
            default_bar_charts::default_bar_chart();
        }
        public function default_bar_chart_table(){
            default_bar_charts::default_bar_chart_table();
        }
    }    
?>
