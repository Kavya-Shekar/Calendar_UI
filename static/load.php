<?php

//load.php

echo "hello";

// $connect = new PDO('mysql:host=localhost;dbname=mydatabase', 'prajwal', '180818');
$servername = "localhost";
$username = "prajwal";
$password = "180818";
$db="mydatabase";

// Create connection
$conn = new mysqli($servername, $username, $password, $db);

// Check connection


$data = array();

$query = "SELECT * FROM my_schedule ORDER BY id";

// $statement = $connect->prepare($query);

// $statement->execute();

// $result = $statement->fetchAll();

$result = mysqli_query($conn, $query);

// foreach($result as $row)
// {
//     $data[] = array(
//     'id'   => $row["id"],
//     'title'   => $row["title"],
//     'start'   => str_replace(' ', 'T', $row["start"]),
//     'end'   => str_replace(' ', 'T', $row["end"]),
//     'allDay' => $row["allDay"]
//  );
//}

if (mysqli_num_rows($result) > 0) {
  // output data of each row
  while($row = mysqli_fetch_assoc($result)) {
      $data[] = $row;
  }
} 



  $fp = fopen('data.txt', 'w');
  fwrite($fp, json_encode($data));
  fclose($fp);

echo json_encode($data);

?>