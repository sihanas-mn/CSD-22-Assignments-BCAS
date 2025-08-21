<?php
session_start();
include 'db_connect.php';

// Check if user is admin
if (!isset($_SESSION['user_type']) || $_SESSION['user_type'] !== 'admin') {
    header("Location: index.php");
    exit();
}

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Collect form data
    $doctor_id = $_POST['doctor_id'];
    $doc_name = $_POST['doc_name'];
    $contactNo = $_POST['contactNo'];
    $username = $_POST['username'];
    $password = $_POST['password'];
    $specialization_id = $_POST['specialization_id'];

    // Validate input
    $errors = [];

    // Check if doctor_id already exists
    $check_id_sql = "SELECT * FROM doctor WHERE doctor_id = ?";
    $check_id_stmt = $conn->prepare($check_id_sql);
    $check_id_stmt->bind_param("s", $doctor_id);
    $check_id_stmt->execute();
    $check_id_result = $check_id_stmt->get_result();

    if ($check_id_result->num_rows > 0) {
        $errors[] = "Doctor ID already exists";
    }

    // Check if username already exists
    $check_username_sql = "SELECT * FROM doctor WHERE username = ?";
    $check_username_stmt = $conn->prepare($check_username_sql);
    $check_username_stmt->bind_param("s", $username);
    $check_username_stmt->execute();
    $check_username_result = $check_username_stmt->get_result();

    if ($check_username_result->num_rows > 0) {
        $errors[] = "Username already exists";
    }

    // Validate contact number
    if (!preg_match("/^[0-9]{10}$/", $contactNo)) {
        $errors[] = "Contact number must be 10 digits";
    }

    // If no errors, proceed with insertion
    if (empty($errors)) {
        // Prepare SQL statement
        $sql = "INSERT INTO doctor (doctor_id, doc_name, contactNo, username, password, specialization_id) 
                VALUES (?, ?, ?, ?, ?, ?)";
        
        // Prepare and bind parameters
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("ssssss", $doctor_id, $doc_name, $contactNo, $username, $password, $specialization_id);

        // Execute the statement
        if ($stmt->execute()) {
            // Redirect to admin dashboard with success message
            header("Location: admin_dashboard.php?success=Doctor added successfully");
            exit();
        } else {
            // Redirect to admin dashboard with error message
            header("Location: admin_dashboard.php?error=Failed to add doctor: " . $stmt->error);
            exit();
        }

        // Close statement
        $stmt->close();
    } else {
        // If there are errors, redirect back with error messages
        $error_string = implode(", ", $errors);
        header("Location: admin_dashboard.php?error=" . urlencode($error_string));
        exit();
    }

    // Close connection
    $conn->close();
}
?>