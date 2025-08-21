<?php
include 'db_connect.php';

// Check if specialization_id is provided
if (!isset($_GET['specialization_id']) || empty($_GET['specialization_id'])) {
    echo json_encode([]);
    exit();
}

$specialization_id = $_GET['specialization_id'];

// Fetch doctors for the given specialization
$sql = "SELECT doctor_id, doc_name FROM doctor WHERE specialization_id = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $specialization_id);
$stmt->execute();
$result = $stmt->get_result();

$doctors = [];
while ($row = $result->fetch_assoc()) {
    $doctors[] = $row;
}

// Return doctors as JSON
header('Content-Type: application/json');
echo json_encode($doctors);
?>