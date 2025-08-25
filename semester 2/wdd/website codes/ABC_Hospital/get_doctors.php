<?php
include 'db_connect.php';

// Check if specialization_id is provided
if (isset($_GET['specialization_id'])) {
    $specialization_id = $_GET['specialization_id'];
    
    // Prepare SQL to get doctors for specific specialization
    $sql = "SELECT doctor_id, doc_name FROM doctor WHERE specialization_id = ?";
    
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $specialization_id);
    $stmt->execute();
    $result = $stmt->get_result();
    
    $doctors = [];
    
    // Fetch all doctors
    while ($row = $result->fetch_assoc()) {
        $doctors[] = $row;
    }
    
    // Send JSON response
    header('Content-Type: application/json');
    echo json_encode($doctors);
    
    $stmt->close();
}

$conn->close();
?>