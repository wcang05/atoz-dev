<?php 
include("../model/model.php");  

  
class default_controller {  
      
        public function list_year_pie_chart(){  
            default_parameters::list_year_pie_chart();
        }  
        public function latest_year_pie_chart(){  
            default_parameters::latest_year_pie_chart();
        }  
        public function largest_segment_pie_chart(){  
            default_parameters::largest_segment_pie_chart();
        } 
        public function default_pie_chart(){
            default_charts::default_pie_chart();
        }
        public function default_pie_chart_table(){
            default_charts::default_pie_chart_table();
        }
    }    
?>
