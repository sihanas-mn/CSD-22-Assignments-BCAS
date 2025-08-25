<?php
session_start();
include 'db_connect.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $user_type = $_POST['user_type'];
    $username = $_POST['username'];
    $password = $_POST['password'];
    
    switch($user_type) {
        case 'admin':
            $sql = "SELECT * FROM admin WHERE username = ? AND password = ?";
            break;
        case 'doctor':
            $sql = "SELECT * FROM doctor WHERE username = ? AND password = ?";
            break;
        case 'receptionist':
            $sql = "SELECT * FROM receptionist WHERE username = ? AND password = ?";
            break;
    }
    
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ss", $username, $password);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $_SESSION['user_type'] = $user_type;
        
        switch($user_type) {
            case 'admin':
                $_SESSION['admin_id'] = $row['admin_id'];
                header("Location: admin_dashboard.php");
                break;
            case 'doctor':
                $_SESSION['doctor_id'] = $row['doctor_id'];
                header("Location: doctor_dashboard.php");
                break;
            case 'receptionist':
                $_SESSION['receptionist_id'] = $row['receptionist_id'];
                header("Location: receptionist_dashboard.php");
                break;
        }
    } else {
        header("Location: index.php?error=1");
    }
    
    $stmt->close();
}
$conn->close();
?>