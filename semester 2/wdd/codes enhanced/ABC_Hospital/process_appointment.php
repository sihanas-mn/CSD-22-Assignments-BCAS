<?php
session_start();
include 'db_connect.php';

// Function to generate unique 10-character reference number
function generateReferenceNumber($conn) {
    while (true) {
        // Generate a random 10-character alphanumeric reference number
        $reference_no = strtoupper(substr(md5(uniqid(mt_rand(), true)), 0, 10));
        
        // Check if this reference number already exists in the patient table
        $check_sql = "SELECT * FROM patient WHERE reference_no = ?";
        $stmt = $conn->prepare($check_sql);
        $stmt->bind_param("s", $reference_no);
        $stmt->execute();
        $result = $stmt->get_result();
        
        // If no existing reference number found, return it
        if ($result->num_rows == 0) {
            return $reference_no;
        }
    }
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Generate unique reference number
    $reference_no = generateReferenceNumber($conn);

    // Collect patient information
    $patient_name = $_POST['patient_name'];
    $email = $_POST['email'];
    $address = $_POST['address'];
    $dob = $_POST['dob'];
    $contactNo = $_POST['contactNo'];

    // Collect appointment information
    $doctor_id = $_POST['doctor_id'];
    $appointment_datetime = $_POST['appointment_datetime'];
    $reason = $_POST['reason'];

    // Start transaction to ensure data consistency
    $conn->begin_transaction();

    try {
        // Insert patient information
        $patient_sql = "INSERT INTO patient (reference_no, patient_name, email, address, DoB, contactNo) 
                        VALUES (?, ?, ?, ?, ?, ?)";
        $patient_stmt = $conn->prepare($patient_sql);
        $patient_stmt->bind_param("sssssi", $reference_no, $patient_name, $email, $address, $dob, $contactNo);
        $patient_stmt->execute();

        // Insert appointment information
        // We'll leave receptionist_id NULL as it will be assigned later
        $appointment_sql = "INSERT INTO appointment 
                            (appointment_id, appointment_date_time, reason, isConfirmed, doctor_id, reference_no) 
                            VALUES (?, ?, ?, false, ?, ?)";
        $appointment_stmt = $conn->prepare($appointment_sql);
        $appointment_id = generateReferenceNumber($conn); // Generate another unique ID for appointment
        $appointment_stmt->bind_param("sssss", $appointment_id, $appointment_datetime, $reason, $doctor_id, $reference_no);
        $appointment_stmt->execute();

        // Commit transaction
        $conn->commit();

        // Redirect to success page with reference number
        header("Location: appointment_confirmation.php?ref=" . urlencode($reference_no));
        exit();

    } catch (Exception $e) {
        // Rollback transaction in case of error
        $conn->rollback();
        
        // Redirect to error page
        header("Location: new_appointment.php?error=" . urlencode($e->getMessage()));
        exit();
    }
}
?>