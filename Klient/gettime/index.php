<?php
header('Access-Control-Allow-Origin: *');
header('Content-type: application/json');

$time = microtime(true);
$res = sprintf('%0.2f', $time);

$data = [ 'time' => $res ];
echo json_encode( $data );
?>