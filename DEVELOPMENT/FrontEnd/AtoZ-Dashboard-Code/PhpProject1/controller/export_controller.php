<?php
include("../model/model.php");  

class export_controller{
        public static function export_data(){
            if(isset($_POST["export"]))  //If "export" parameter is set
                {
                    //Accept parameters
                    $year = $_POST['year_pie'];
                    $segname = $_POST['segment_pie'];
                    data::export_data($segname, $year);
                }
            }
    }
    export_controller::export_data();
?>