<?php

  require 'vendor/autoload.php'; // include Composer's autoloader

  // $client = new MongoDB\Client("mongodb://localhost:27017");
  // // connect to mongodb
  //
  // echo "Connection to database successfully";
  $query_nama_acara = array('nama_acara' => 'MasterKey');
  //
  // // select a database
  // $db = $client->nlp_tweet;
  // echo "Database mydb selected";
  // $collection = $db->tweet;
  // echo "Collection created succsessfully";
  //
  // $cursor = $collection->find($query_nama_acara);
  // foreach ($cursor as $doc) {
  //   echo var_dump($doc);
  // }

  $collection = (new MongoDB\Client)->nlp_tweet->tweet;
  $n_data = 0;
  $all_kota = [];
  $positif = array();
  $negatif = array();
  $n_tweet = array();

  $document = $collection->find($query_nama_acara);
  foreach ($document as $doc) {
    $n_data = $n_data + 1;

    $json_obj = json_encode($doc);
    $php_obj = json_decode($json_obj);

    if(array_search($php_obj->location, $all_kota) == null) {
      array_push($all_kota, $php_obj->location);
      $positif[$php_obj->location] = 0;
      $negatif[$php_obj->location] = 0;
      $n_tweet[$php_obj->location] = 0;
    }

    $n_tweet[$php_obj->location] = $n_tweet[$php_obj->location]+1;
    
    if($php_obj->sentiment == "positive") {
      $positif[$php_obj->location] = $positif[$php_obj->location] + 1;
    } else if($php_obj->sentiment == "negative") {
      $negatif[$php_obj->location] = $negatif[$php_obj->location] + 1;
    }
  }
?>
<html>
<head>
  <title>Sentimen Analisis Acara Televisi</title>
</head>
<body>
  <h1>MasterKey</h1>
  <table>
    <thead>
      <tr>
        <th>Nama Kota</th>
        <th>Positif</th>
        <th>Negatif</th>
        <th>Popularitas</th>
      </tr>
    </thead>
    <tbody>
      <?php
        foreach ($all_kota as $kota) {
          echo '<tr>';
          echo '<td>'.$kota.'</td>';
          echo '<td>'.$positif[$kota].'</td>';
          echo '<td>'.$negatif[$kota].'</td>';
          echo '<td>'.$n_tweet[$kota].'</td>';
          echo '<tr>';
        }

      ?>
    </tbody>
  </table>

</body>
</html>