<?php 

include("../model/db_connect.php");  

// Class to retrieve and store some default parameters
class default_parameters {  
    
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
                            SELECT MAX(sample_data.Year) AS year FROM google_chart_dev.sample_data)
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
class default_charts{
    
    static function default_pie_chart(){
        
        // For Pie Chart
        // Generate an array of segment name against their head counts. ()Latest year
        $default_piechart_query = "SELECT metadata.Seg_Name AS segname, COUNT(*) AS head_count 
                                    FROM google_chart_dev.sample_data
                                    INNER JOIN google_chart_dev.metadata ON sample_data.Ttl_Spt_Amt >= metadata.Low_Range
                                    AND sample_data.Ttl_Spt_Amt < metadata.High_Range
                                    WHERE sample_data.Year= (SELECT MAX(sample_data.Year) FROM google_chart_dev.sample_data)
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
                                               GROUP BY metadata.Seg_Name
                                               ORDER BY head_count DESC LIMIT 1) AS x) 
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

class draw_charts{
    
    // For Pie Chart's table
    static function draw_pie_chart($year){
        
        // Draw pie chart (selected year)
        $pie_chart_query =   "SELECT metadata.Seg_Name AS segname, COUNT(*) AS head_count FROM google_chart_dev.sample_data
                                    INNER JOIN google_chart_dev.metadata ON sample_data.Ttl_Spt_Amt >= metadata.Low_Range
                                    AND sample_data.Ttl_Spt_Amt < metadata.High_Range
                                    WHERE sample_data.Year=  '$year' 
                                    GROUP BY metadata.Seg_Name
                                    ORDER BY head_count DESC
                                    ";  
        
        $pie_chart_result = mysqli_query(db_connect::connect(), $pie_chart_query);  
        
        while($result = mysqli_fetch_array($pie_chart_result))
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
                                    WHERE Seg_Name = '$segname' AND sample_data.Year='$year'
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
                                               SELECT MAX(sample_data.Year) AS year FROM google_chart_dev.sample_data)
                                               GROUP BY metadata.Seg_Name
                                               ORDER BY head_count DESC LIMIT 1) AS x) 
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
                                 WHERE Seg_Name = '$segname' AND sample_data.Year='$year'
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
?>

