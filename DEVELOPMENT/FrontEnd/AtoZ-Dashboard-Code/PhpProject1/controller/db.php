<?php
//MySQL Hostname
$hostname = "localhost";

//MySQL Root Username
$username = "root";

//MySQL Root Password
$password = "";

//Connect MySQL 
$connect = mysqli_connect($hostname, $username, $password);  

//If connection failed
if ($connect->connect_error) {
    die("Connection failed: " . $connect->connect_error);
} 
?>