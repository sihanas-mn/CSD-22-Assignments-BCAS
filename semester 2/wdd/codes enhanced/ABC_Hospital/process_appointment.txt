<?php
session_start();
include 'db_connect.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Generate unique reference number
    function generateReferenceNo() {
        return 'REF' . date('Ymd') . rand(1000, 9999);
    }
    
    $reference_no = generateReferenceNo();
    
    // First, insert patient information
    $stmt = $conn->prepare("INSERT INTO patient (reference_no, patient_name, email, address, DoB, contactNo) 
                           VALUES (?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("sssssi", 
        $reference_no,
        $_POST['patient_name'],
        $_POST['email'],
        $_POST['address'],
        $_POST['dob'],
        $_POST['contactNo']
    );
    
    if ($stmt->execute()) {
        // Now insert appointment
        $stmt = $conn->prepare("INSERT INTO appointment (appointment_id, appointment_date_time, 
                              reason, doctor_id, reference_no) 
                              VALUES (?, ?, ?, ?, ?)");
        
        $appointment_id = 'APT' . date('Ymd') . rand(1000, 9999);
        $stmt->bind_param("sssss",
            $appointment_id,
            $_POST['appointment_date_time'],
            $_POST['reason'],
            $_POST['doctor_id'],
            $reference_no
        );
        
        if ($stmt->execute()) {
            // Success - show reference number to patient
            header("Location: appointment_success.php?ref=" . $reference_no);
        } else {
            echo "Error booking appointment: " . $conn->error;
        }
    } else {
        echo "Error saving patient information: " . $conn->error;
    }
    
    $stmt->close();
    $conn->close();
}
?>