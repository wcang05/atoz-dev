<?php

class draw_charts{ 
    
    // For Bar Chart's table
    static function draw_bar_chart($year){
        
        // Draw bar chart (selected year)
        $bar_chart_query =   "SELECT metadata.Seg_Name AS segname, COUNT(*) AS head_count FROM google_chart_dev.sample_data
                                    INNER JOIN google_chart_dev.metadata ON sample_data.Ttl_Spt_Amt >= metadata.Low_Range
                                    AND sample_data.Ttl_Spt_Amt < metadata.High_Range
                                    WHERE sample_data.Year=  '$year' 
                                    AND metadata.Conf_Name = 'Ttl_Spt_Amt'    
                                    GROUP BY metadata.Seg_Name
                                    ORDER BY head_count DESC
                                    ";  
        
        $bar_chart_result = mysqli_query(db_connect::connect(), $bar_chart_query);  
        
        while($result = mysqli_fetch_array($bar_chart_result))
            {
                $rows[]=array("c"=>array("0"=>array("v"=>$result['segname'],"f"=>NULL),
                                         "1"=>array("v"=>(int)$result['head_count'],"f" =>NULL)));
            }

        echo $format = '{
        "cols":
        [
        {"id":"","label":"Segment Name","pattern":"","type":"string"},
        {"id":"","label":"Head Count","pattern":"","type":"number"}
        ],
        "rows":'.json_encode($rows).'}';
    }
    
    // Generate table
    static function draw_table($segname,$year){
        
        // Draw table (selected year and segment)
        $table_chart_update_query =   "SELECT * FROM google_chart_dev.sample_data
                                    INNER JOIN google_chart_dev.metadata 
                                    ON sample_data.Ttl_Spt_Amt >= metadata.Low_Range 
                                    AND sample_data.Ttl_Spt_Amt < metadata.High_Range     
                                    WHERE Seg_Name = '$segname' AND sample_data.Year='$year' AND metadata.Conf_Name = 'Ttl_Spt_Amt'
                                    "; 
        $table_chart_update_result = mysqli_query(db_connect::connect(), $table_chart_update_query);  
        
        while($result = mysqli_fetch_array($table_chart_update_result)){
            $rows[]=array("c"=>array("0"=>array("v"=>$result['Firtname'],"f"=>NULL),
                                      "1"=>array("v"=>$result['Lastname'],"f" =>NULL),
                                      "2"=>array("v"=>$result['PCode'],"f"=>NULL),
                                      "3"=>array("v"=>$result['custype'],"f"=>NULL),
                                      "4"=>array("v"=>(double)$result['Min_Spt_Gap'],"f" =>NULL),
                                      "5"=>array("v"=>(double)$result['Max_Spt_Gap'],"f"=>NULL),
                                      "6"=>array("v"=>(double)$result['Avg_Spt_Gap'],"f"=>NULL),
                                      "7"=>array("v"=>(double)$result['Ttl_Spt_Amt'],"f" =>NULL),
                                      "8"=>array("v"=>(double)$result['Ave_Spt_AmtBuy_Cat'],"f"=>NULL),
                                      "9"=>array("v"=>$result['Year'],"f"=>NULL)));
            }

        echo $format = '{
            "cols":
            [
            {"id":"","label":"Firtname","pattern":"","type":"string"},
            {"id":"","label":"Lastname","pattern":"","type":"string"},
            {"id":"","label":"PCode","pattern":"","type":"string"},
            {"id":"","label":"Cpny/Ind","pattern":"","type":"string"},
            {"id":"","label":"Min_Spt_Gap","pattern":"","type":"number"},
            {"id":"","label":"Max_Spt_Gap","pattern":"","type":"number"},
            {"id":"","label":"Avg_Spt_Gap","pattern":"","type":"number"},
            {"id":"","label":"Ttl_Spt_Amt","pattern":"","type":"number"},
            {"id":"","label":"Ave_Spt_AmtBuy_Cat","pattern":"","type":"number"},
            {"id":"","label":"Year","pattern":"","type":"string"}
            ],
            "rows":'.json_encode($rows).'}'; 
    }
    
    static function draw_table_by_year($year){
        
        // Draw table (largest area and laetst year)
        $default_table_query = "SELECT sample_data.Firtname, 
                                   sample_data.Lastname, 
                                   sample_data.PCode,
                                   sample_data.custype,
                                   sample_data.Min_Spt_Gap , 
                                   sample_data.Max_Spt_Gap , 
                                   sample_data.Avg_Spt_Gap , 
                                   sample_data.Ttl_Spt_Amt , 
                                   sample_data.Ave_Spt_AmtBuy_Cat , 
                                   sample_data.Year
                                   from google_chart_dev.sample_data
                                   INNER JOIN google_chart_dev.metadata 
                                   ON sample_data.Ttl_Spt_Amt >= metadata.Low_Range 
                                   AND sample_data.Ttl_Spt_Amt < metadata.High_Range 
                                   WHERE Seg_Name = (
                                       SELECT segname 
                                       FROM (
                                           SELECT metadata.Seg_Name AS segname, COUNT(*) AS head_count 
                                           FROM google_chart_dev.sample_data
                                           INNER JOIN google_chart_dev.metadata 
                                           ON sample_data.Ttl_Spt_Amt >= metadata.Low_Range
                                           AND sample_data.Ttl_Spt_Amt < metadata.High_Range
                                           WHERE sample_data.Year= (
                                               SELECT MAX(sample_data.Year) AS year FROM google_chart_dev.sample_data
                                               )
                                            AND metadata.Conf_Name = 'Ttl_Spt_Amt'   
                                            GROUP BY metadata.Seg_Name
                                            ORDER BY head_count DESC LIMIT 1) AS x) 
                                   AND metadata.Conf_Name = 'Ttl_Spt_Amt'    
                                   AND sample_data.Year='$year'";

        $default_table_result = mysqli_query(db_connect::connect(), $default_table_query);  
        
        while($result = mysqli_fetch_array($default_table_result)){
            $rows[]=array("c"=>array("0"=>array("v"=>$result['Firtname'],"f"=>NULL),
                                      "1"=>array("v"=>$result['Lastname'],"f" =>NULL),
                                      "2"=>array("v"=>$result['PCode'],"f"=>NULL),
                                      "3"=>array("v"=>$result['custype'],"f"=>NULL),
                                      "4"=>array("v"=>(double)$result['Min_Spt_Gap'],"f" =>NULL),
                                      "5"=>array("v"=>(double)$result['Max_Spt_Gap'],"f"=>NULL),
                                      "6"=>array("v"=>(double)$result['Avg_Spt_Gap'],"f"=>NULL),
                                      "7"=>array("v"=>(double)$result['Ttl_Spt_Amt'],"f" =>NULL),
                                      "8"=>array("v"=>(double)$result['Ave_Spt_AmtBuy_Cat'],"f"=>NULL),
                                      "9"=>array("v"=>$result['Year'],"f"=>NULL)));
            }

        echo $format = '{
            "cols":
            [
            {"id":"","label":"Firtname","pattern":"","type":"string"},
            {"id":"","label":"Lastname","pattern":"","type":"string"},
            {"id":"","label":"PCode","pattern":"","type":"string"},
            {"id":"","label":"Cpny/Ind","pattern":"","type":"string"},
            {"id":"","label":"Min_Spt_Gap","pattern":"","type":"number"},
            {"id":"","label":"Max_Spt_Gap","pattern":"","type":"number"},
            {"id":"","label":"Avg_Spt_Gap","pattern":"","type":"number"},
            {"id":"","label":"Ttl_Spt_Amt","pattern":"","type":"number"},
            {"id":"","label":"Ave_Spt_AmtBuy_Cat","pattern":"","type":"number"},
            {"id":"","label":"Year","pattern":"","type":"string"}
            ],
            "rows":'.json_encode($rows).'}'; 
    }
    
}

