<?php
session_start();
include 'db_connect.php';

function generateReferenceNumber() {
    // Generate a unique 10-character reference number
    $characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $reference = '';
    for ($i = 0; $i < 10; $i++) {
        $reference .= $characters[rand(0, strlen($characters) - 1)];
    }
    return $reference;
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Patient Details
    $patient_name = $_POST['patient_name'];
    $email = $_POST['email'];
    $contactNo = $_POST['contactNo'];
    $address = $_POST['address'];
    $DoB = $_POST['DoB'];
    
    // Appointment Details
    $doctor_id = $_POST['doctor_id'];
    $appointment_datetime = $_POST['appointment_datetime'];
    $reason = $_POST['reason'];
    
    // Start a transaction
    $conn->begin_transaction();
    
    try {
        // Generate unique reference number
        $reference_no = generateReferenceNumber();
        
        // Check if reference number is unique
        $check_ref_sql = "SELECT * FROM patient WHERE reference_no = ?";
        $check_ref_stmt = $conn->prepare($check_ref_sql);
        $check_ref_stmt->bind_param("s", $reference_no);
        $check_ref_stmt->execute();
        $check_ref_result = $check_ref_stmt->get_result();
        
        // If reference number exists, regenerate
        while ($check_ref_result->num_rows > 0) {
            $reference_no = generateReferenceNumber();
            $check_ref_stmt->bind_param("s", $reference_no);
            $check_ref_stmt->execute();
            $check_ref_result = $check_ref_stmt->get_result();
        }
        
        // Insert Patient Details
        $patient_sql = "INSERT INTO patient (reference_no, patient_name, email, address, DoB, contactNo) 
                        VALUES (?, ?, ?, ?, ?, ?)";
        $patient_stmt = $conn->prepare($patient_sql);
        $patient_stmt->bind_param("sssssi", $reference_no, $patient_name, $email, $address, $DoB, $contactNo);
        $patient_stmt->execute();
        
        // Get the receptionist with the least number of appointments
        $receptionist_sql = "SELECT receptionist_id FROM receptionist 
                             LEFT JOIN (
                                 SELECT receptionist_id, COUNT(*) as appointment_count 
                                 FROM appointment 
                                 GROUP BY receptionist_id
                             ) AS recep_counts ON receptionist.receptionist_id = recep_counts.receptionist_id
                             ORDER BY IFNULL(appointment_count, 0) ASC 
                             LIMIT 1";
        $receptionist_result = $conn->query($receptionist_sql);
        $receptionist_row = $receptionist_result->fetch_assoc();
        $receptionist_id = $receptionist_row['receptionist_id'];
        
        // Insert Appointment
        $appointment_sql = "INSERT INTO appointment (
            appointment_id, 
            appointment_date_time, 
            reason, 
            isConfirmed, 
            doctor_id, 
            receptionist_id, 
            reference_no
        ) VALUES (?, ?, ?, false, ?, ?, ?)";
        
        // Generate unique appointment ID
        $appointment_id = generateReferenceNumber();
        
        $appointment_stmt = $conn->prepare($appointment_sql);
        $appointment_stmt->bind_param(
            "sssiss", 
            $appointment_id, 
            $appointment_datetime, 
            $reason, 
            $doctor_id, 
            $receptionist_id, 
            $reference_no
        );
        $appointment_stmt->execute();
        
        // Commit transaction
        $conn->commit();
        
        // Redirect to new_appointment.php with reference number
        header("Location: new_appointment.php?reference=" . urlencode($reference_no));
        exit();
        
    } catch (Exception $e) {
        // Rollback transaction
        $conn->rollback();
        
        // Redirect with error
        header("Location: new_appointment.php?error=" . urlencode($e->getMessage()));
        exit();
    }
}
$conn->close();
?>