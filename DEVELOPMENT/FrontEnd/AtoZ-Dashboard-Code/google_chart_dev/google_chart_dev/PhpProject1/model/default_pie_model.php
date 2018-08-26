<?php

class default_pie_parameters {  
    
    // For Pie Chart
    // Generate an array of years, from earliest until latest
    static function list_year_pie_chart(){
        
        $gen_year = "SELECT DISTINCT(Year) AS year FROM google_chart_dev.sample_data ORDER BY year ASC";  
        $gen_year_result = mysqli_query(db_connect::connect(), $gen_year);  
        
        while($rows = mysqli_fetch_array($gen_year_result))
        {
          echo "<option value='".$rows['year']."'>".$rows['year']."</option>";
        }   
    }   
    
    // Generate latest year
    static function latest_year_pie_chart(){
        $latest_year_query = "SELECT MAX(sample_data.Year) AS year FROM google_chart_dev.sample_data";
        $gen_latest_year_result = mysqli_query(db_connect::connect(), $latest_year_query);  
        
        while($rows = mysqli_fetch_array($gen_latest_year_result))
        {
          echo "value = '".$rows['year']."'";
        }   
    } 
    
    // Generate largest segment of pie chart
    static function largest_segment_pie_chart(){  
        // Generate the results of segment with the largest area
        $default_seg_query = "SELECT segname FROM (SELECT metadata.Seg_Name AS segname, COUNT(*) AS head_count 
                            FROM google_chart_dev.sample_data
                            INNER JOIN google_chart_dev.metadata 
                            ON sample_data.Ttl_Spt_Amt >= metadata.Low_Range
                            AND sample_data.Ttl_Spt_Amt < metadata.High_Range
                            WHERE sample_data.Year= (
                            SELECT MAX(sample_data.Year) AS year FROM google_chart_dev.sample_data
                            )
                            AND metadata.Conf_Name = 'Ttl_Spt_Amt'
                            GROUP BY metadata.Seg_Name
                            ORDER BY head_count DESC LIMIT 1) AS x
                                                    ";
        $default_seg_result = mysqli_query(db_connect::connect(), $default_seg_query);  
        
        while($rows = mysqli_fetch_array($default_seg_result))
        {
          echo "value = '".$rows['segname']."'";
        }   
    }
}  

// Class to draw default chart
class default_pie_charts{
    
    static function default_pie_chart(){
        
        // For Pie Chart
        // Generate an array of segment name against their head counts. ()Latest year
        $default_piechart_query = "SELECT metadata.Seg_Name AS segname, COUNT(*) AS head_count 
                                    FROM google_chart_dev.sample_data
                                    INNER JOIN google_chart_dev.metadata ON sample_data.Ttl_Spt_Amt >= metadata.Low_Range
                                    AND sample_data.Ttl_Spt_Amt < metadata.High_Range
                                    WHERE sample_data.Year= (SELECT MAX(sample_data.Year) FROM google_chart_dev.sample_data)
                                    AND metadata.Conf_Name = 'Ttl_Spt_Amt'
                                    GROUP BY metadata.Seg_Name
                                    ORDER BY head_count DESC
                                    ";
        
        $default_piechart_result = mysqli_query(db_connect::connect(), $default_piechart_query);  
        
        while($row = mysqli_fetch_array($default_piechart_result))
        {
            echo "[`".$row["segname"]."`, ".$row["head_count"]."],";  
        } 
    }
    
    static function default_pie_chart_table(){
        // Draw table (largest area and latest year)
        $default_pie_table_query = "SELECT sample_data.Firtname, 
                                   sample_data.Lastname, 
                                   sample_data.PCode,
                                   sample_data.custype,
                                   sample_data.Min_Spt_Gap , 
                                   sample_data.Max_Spt_Gap , 
                                   sample_data.Avg_Spt_Gap , 
                                   sample_data.Ttl_Spt_Amt , 
                                   sample_data.Ave_Spt_AmtBuy_Cat , 
                                   sample_data.Year
                                   FROM google_chart_dev.sample_data
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
                                               SELECT MAX(sample_data.Year) AS year FROM google_chart_dev.sample_data)
                                               AND metadata.Conf_Name = 'Ttl_Spt_Amt'
                                               GROUP BY metadata.Seg_Name
                                               ORDER BY head_count DESC LIMIT 1) AS x) 
                                   AND metadata.Conf_Name = 'Ttl_Spt_Amt'
                                   AND sample_data.Year=(
                                       SELECT MAX(sample_data.Year) AS year FROM google_chart_dev.sample_data)
                                           ";
        $default_pie_table_result = mysqli_query(db_connect::connect(), $default_pie_table_query);  
        
        while($row = mysqli_fetch_array($default_pie_table_result)){  
                    // echo "['".$row["segname"]."', ".$row["head_count"]."],";  
                    echo "[`".$row["Firtname"]."`, `".$row["Lastname"]."`, `".$row["PCode"]."`, `".$row["custype"]."`, ".$row["Min_Spt_Gap"].", ".$row["Max_Spt_Gap"].", ".$row["Avg_Spt_Gap"].", ".$row["Ttl_Spt_Amt"].", ".$row["Ave_Spt_AmtBuy_Cat"].", `".$row["Year"]."`],";  
                } 
    }
}

