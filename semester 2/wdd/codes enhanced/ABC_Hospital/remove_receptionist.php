<?php
session_start();
include 'db_connect.php';

// Check if user is admin
if (!isset($_SESSION['user_type']) || $_SESSION['user_type'] !== 'admin') {
    header("Location: index.php");
    exit();
}

// Check if receptionist ID is provided
if (!isset($_GET['id']) || empty($_GET['id'])) {
    // Redirect back to admin dashboard with error
    header("Location: admin_dashboard.php?error=Invalid Receptionist ID");
    exit();
}

$receptionist_id = $_GET['id'];

// First, check if the receptionist has any pending appointments
$check_appointments = "SELECT COUNT(*) as appointment_count 
                       FROM appointment 
                       WHERE receptionist_id = ?";
$stmt_check = $conn->prepare($check_appointments);
$stmt_check->bind_param("s", $receptionist_id);
$stmt_check->execute();
$result_check = $stmt_check->get_result();
$appointment_data = $result_check->fetch_assoc();

if ($appointment_data['appointment_count'] > 0) {
    // If there are pending appointments, prevent deletion
    header("Location: admin_dashboard.php?error=Cannot remove receptionist with active appointments");
    exit();
}

// Prepare and execute delete statement
$sql = "DELETE FROM receptionist WHERE receptionist_id = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $receptionist_id);

if ($stmt->execute()) {
    // Successful deletion
    header("Location: admin_dashboard.php?success=Receptionist removed successfully");
} else {
    // Error in deletion
    header("Location: admin_dashboard.php?error=Failed to remove receptionist");
}

$stmt->close();
$conn->close();
?>