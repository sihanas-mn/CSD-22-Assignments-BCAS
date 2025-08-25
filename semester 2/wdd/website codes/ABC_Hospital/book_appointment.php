<?php
session_start();
include 'db_connect.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Generate unique reference number
    $reference_no = 'REF' . date('YmdHis') . rand(100, 999);

    // Patient details
    $patient_name = $_POST['patient_name'];
    $email = $_POST['email'];
    $contactNo = $_POST['contactNo'];
    $address = $_POST['address'];
    $DoB = $_POST['DoB'];

    // Appointment details
    $doctor_id = $_POST['doctor_id'];
    $appointment_date_time = $_POST['appointment_date_time'];
    $reason = $_POST['reason'];

    // Start a transaction
    $conn->begin_transaction();

    try {
        // First, insert patient details
        $patient_sql = "INSERT INTO patient (reference_no, patient_name, email, address, DoB, contactNo) 
                        VALUES (?, ?, ?, ?, ?, ?)";
        $patient_stmt = $conn->prepare($patient_sql);
        $patient_stmt->bind_param("sssssi", $reference_no, $patient_name, $email, $address, $DoB, $contactNo);
        $patient_stmt->execute();

        // Then, insert appointment details
        $appointment_sql = "INSERT INTO appointment 
                            (appointment_id, appointment_date_time, reason, doctor_id, reference_no, isConfirmed) 
                            VALUES (?, ?, ?, ?, ?, 0)";
        $appointment_id = 'APP' . date('YmdHis') . rand(100, 999);
        $appointment_stmt = $conn->prepare($appointment_sql);
        $appointment_stmt->bind_param("sssss", $appointment_id, $appointment_date_time, $reason, $doctor_id, $reference_no);
        $appointment_stmt->execute();

        // Commit the transaction
        $conn->commit();

        // Redirect to a success page with reference number
        header("Location: appointment_confirmation.php?reference_no=" . $reference_no);
        exit();
    } catch (Exception $e) {
        // Rollback the transaction
        $conn->rollback();

        // Redirect to error page
        header("Location: new_appointment.php?error=" . urlencode($e->getMessage()));
        exit();
    }
}
$conn->close();
?>