<?php
session_start();
include 'db_connect.php';

// Check if user is logged in as admin
if (!isset($_SESSION['user_type']) || $_SESSION['user_type'] !== 'admin') {
    header("Location: index.php");
    exit();
}

// Check if doctor ID is provided
if (!isset($_GET['id'])) {
    header("Location: admin_dashboard.php?error=no_id");
    exit();
}

$doctor_id = $_GET['id'];

// Begin transaction
$conn->begin_transaction();

try {
    // First check if there are any pending appointments for this doctor
    $check_appointments = "SELECT appointment_id FROM appointment 
                         WHERE doctor_id = ? AND appointment_date_time > NOW()";
    $stmt = $conn->prepare($check_appointments);
    $stmt->bind_param("s", $doctor_id);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        // There are pending appointments
        $conn->rollback();
        header("Location: admin_dashboard.php?error=pending_appointments");
        exit();
    }

    // Update past appointments to mark doctor as inactive
    $update_appointments = "UPDATE appointment 
                          SET doctor_id = CONCAT('INACTIVE_', doctor_id) 
                          WHERE doctor_id = ? AND appointment_date_time <= NOW()";
    $stmt = $conn->prepare($update_appointments);
    $stmt->bind_param("s", $doctor_id);
    $stmt->execute();

    // Now delete the doctor
    $delete_doctor = "DELETE FROM doctor WHERE doctor_id = ?";
    $stmt = $conn->prepare($delete_doctor);
    $stmt->bind_param("s", $doctor_id);
    $stmt->execute();

    if ($stmt->affected_rows > 0) {
        // Commit transaction
        $conn->commit();
        header("Location: admin_dashboard.php?success=doctor_removed");
        exit();
    } else {
        // No doctor found with this ID
        $conn->rollback();
        header("Location: admin_dashboard.php?error=doctor_not_found");
        exit();
    }

} catch (Exception $e) {
    // If any error occurs, rollback the transaction
    $conn->rollback();
    header("Location: admin_dashboard.php?error=system_error");
    exit();
}

// Close connection
$stmt->close();
$conn->close();
?>

<!DOCTYPE html>
<html>
<head>
    <title>Remove Doctor - Processing</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f4f4f4;
        }
        .message {
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .error {
            color: #dc3545;
        }
        .success {
            color: #28a745;
        }
    </style>
</head>
<body>
    <div class="message">
        <?php
        if (isset($_GET['error'])) {
            switch($_GET['error']) {
                case 'pending_appointments':
                    echo '<p class="error">Cannot remove doctor. There are pending appointments.</p>';
                    break;
                case 'doctor_not_found':
                    echo '<p class="error">Doctor not found in the system.</p>';
                    break;
                case 'system_error':
                    echo '<p class="error">A system error occurred. Please try again.</p>';
                    break;
                default:
                    echo '<p class="error">An error occurred.</p>';
            }
        } elseif (isset($_GET['success'])) {
            echo '<p class="success">Doctor has been successfully removed from the system.</p>';
        }
        ?>
        <p><a href="admin_dashboard.php">Return to Dashboard</a></p>
    </div>
</body>
</html>