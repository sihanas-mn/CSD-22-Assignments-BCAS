<?php
session_start();
include 'db_connect.php';

// Check if user is admin
if (!isset($_SESSION['user_type']) || $_SESSION['user_type'] !== 'admin') {
    header("Location: index.php");
    exit();
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Validate input fields
    if (
        empty($_POST['receptionist_id']) || 
        empty($_POST['recep_name']) || 
        empty($_POST['contactNo']) || 
        empty($_POST['username']) || 
        empty($_POST['password'])
    ) {
        $_SESSION['error'] = "All fields are required";
        header("Location: admin_dashboard.php");
        exit();
    }

    // Sanitize inputs
    $receptionist_id = $conn->real_escape_string($_POST['receptionist_id']);
    $recep_name = $conn->real_escape_string($_POST['recep_name']);
    $contactNo = $conn->real_escape_string($_POST['contactNo']);
    $username = $conn->real_escape_string($_POST['username']);
    $password = $conn->real_escape_string($_POST['password']);

    // Check if receptionist_id already exists
    $check_query = "SELECT receptionist_id FROM receptionist WHERE receptionist_id = ?";
    $check_stmt = $conn->prepare($check_query);
    $check_stmt->bind_param("s", $receptionist_id);
    $check_stmt->execute();
    $check_result = $check_stmt->get_result();

    if ($check_result->num_rows > 0) {
        $_SESSION['error'] = "Receptionist ID already exists";
        header("Location: admin_dashboard.php");
        $check_stmt->close();
        exit();
    }
    $check_stmt->close();

    // Check if username already exists
    $check_username_query = "SELECT username FROM receptionist WHERE username = ?";
    $check_username_stmt = $conn->prepare($check_username_query);
    $check_username_stmt->bind_param("s", $username);
    $check_username_stmt->execute();
    $check_username_result = $check_username_stmt->get_result();

    if ($check_username_result->num_rows > 0) {
        $_SESSION['error'] = "Username already exists";
        header("Location: admin_dashboard.php");
        $check_username_stmt->close();
        exit();
    }
    $check_username_stmt->close();

    // Prepare and execute the insert query
    $insert_query = "INSERT INTO receptionist (receptionist_id, recep_name, contactNo, username, password) VALUES (?, ?, ?, ?, ?)";
    $insert_stmt = $conn->prepare($insert_query);
    $insert_stmt->bind_param("sssss", $receptionist_id, $recep_name, $contactNo, $username, $password);

    try {
        if ($insert_stmt->execute()) {
            // Success message
            $_SESSION['success'] = "Receptionist added successfully";
        } else {
            // Error message
            $_SESSION['error'] = "Error adding receptionist: " . $conn->error;
        }
    } catch (Exception $e) {
        $_SESSION['error'] = "Error adding receptionist: " . $e->getMessage();
    }

    $insert_stmt->close();
    header("Location: admin_dashboard.php");
    exit();
} else {
    // If someone tries to access this file directly without POST data
    header("Location: admin_dashboard.php");
    exit();
}

$conn->close();
?>