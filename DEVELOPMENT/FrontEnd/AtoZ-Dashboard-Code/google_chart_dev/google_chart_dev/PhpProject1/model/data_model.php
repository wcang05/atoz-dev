<?php

class data{
    
    static function export_data($segname, $year){
        header('Content-Type: text/csv; charset=utf-8');  
       
        // Content-Disposition: Force download using browser
        // Suggest user new file name before download
        header('Content-Disposition: attachment; filename=data.csv');  

        // Write file
        $output = fopen("php://output", "w");  

        // SQL query
        $table_chart_update_query =   "SELECT sample_data.Firtname, sample_data.Lastname, sample_data.PCode, sample_data.custype, sample_data.Min_Spt_Gap, sample_data.Max_Spt_Gap, sample_data.Avg_Spt_Gap, sample_data.Ttl_Spt_Amt, sample_data.Ave_Spt_AmtBuy_Cat, sample_data.Year 
                                 FROM google_chart_dev.sample_data
                                 INNER JOIN google_chart_dev.metadata 
                                 ON sample_data.Ttl_Spt_Amt >= metadata.Low_Range 
                                 AND sample_data.Ttl_Spt_Amt < metadata.High_Range 
                                 WHERE Seg_Name = '$segname' AND sample_data.Year='$year' AND metadata.Conf_Name = 'Ttl_Spt_Amt'
                                 ";  

        // Define column name
        fputcsv($output, array('Firtname', 'Lastname', 'PCode', 'custype', 'Min_Spt_Gap', 'Max_Spt_Gap', 'Avg_Spt_Gap', 'Ttl_Spt_Amt', 'Ave_Spt_AmtBuy_Cat', 'Year'));  
        $table_chart_update_result = mysqli_query(db_connect::connect(), $table_chart_update_query);  
        while($row = mysqli_fetch_assoc($table_chart_update_result))  
        {  
             fputcsv($output, $row);  
        }  
        fclose($output);  
    }
}

