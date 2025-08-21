<?php
session_start();
include 'db_connect.php';

// Check if doctor is logged in
if (!isset($_SESSION['user_type']) || $_SESSION['user_type'] !== 'doctor') {
    header("Location: index.php");
    exit();
}

// Check if form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['appointment_id']) && isset($_POST['status'])) {
    $appointment_id = $_POST['appointment_id'];
    $status = $_POST['status'];

    // Prepare SQL to update appointment status
    $sql = "UPDATE appointment SET status = ? WHERE appointment_id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ss", $status, $appointment_id);

    if ($stmt->execute()) {
        // Redirect back to doctor dashboard with success message
        header("Location: doctor_dashboard.php?success=Appointment marked as " . $status);
    } else {
        // Redirect back to doctor dashboard with error message
        header("Location: doctor_dashboard.php?error=Failed to update appointment status");
    }

    $stmt->close();
}

$conn->close();
?>