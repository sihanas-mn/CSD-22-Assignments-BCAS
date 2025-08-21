<?php
session_start();
include 'db_connect.php';

// Check if doctor is logged in
if (!isset($_SESSION['user_type']) || $_SESSION['user_type'] !== 'doctor') {
    header("Location: index.php");
    exit();
}

// Get doctor's ID
$doctor_id = $_SESSION['doctor_id'];

// Fetch doctor's details
$doctor_sql = "SELECT * FROM doctor WHERE doctor_id = ?";
$doctor_stmt = $conn->prepare($doctor_sql);
$doctor_stmt->bind_param("s", $doctor_id);
$doctor_stmt->execute();
$doctor_result = $doctor_stmt->get_result();
$doctor = $doctor_result->fetch_assoc();
?>
<!DOCTYPE html>
<html>
<head>
    <title>Doctor Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            background-color: #f4f4f4;
        }
        .container {
            width: 90%;
            margin: auto;
            padding: 20px;
        }
        .header {
            background: #005792;
            color: white;
            padding: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .content {
            margin-top: 20px;
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .table {
            width: 100%;
            border-collapse: collapse;
        }
        .table th, .table td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: left;
        }
        .table th {
            background: #005792;
            color: white;
        }
        .btn {
            display: inline-block;
            padding: 8px 15px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 5px;
        }
        .btn-danger {
            background: #dc3545;
        }
        .btn-secondary {
            background: #6c757d;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Doctor Dashboard - Dr. <?php echo $doctor['doc_name']; ?></h1>
        <a href="logout.php" class="btn btn-danger">Logout</a>
    </div>

    <div class="container">
        <div class="content">
            <h2>Confirmed Appointments</h2>
            <table class="table">
                <thead>
                    <tr>
                        <th>Reference No</th>
                        <th>Patient Name</th>
                        <th>Date & Time</th>
                        <th>Reason</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    // Fetch confirmed appointments for this doctor
                    $appointments_sql = "SELECT a.*, p.patient_name 
                                         FROM appointment a 
                                         JOIN patient p ON a.reference_no = p.reference_no
                                         WHERE a.doctor_id = ? AND a.isConfirmed = 1 
                                         AND a.status != 'Completed'
                                         ORDER BY a.appointment_date_time";
                    $appointments_stmt = $conn->prepare($appointments_sql);
                    $appointments_stmt->bind_param("s", $doctor_id);
                    $appointments_stmt->execute();
                    $appointments_result = $appointments_stmt->get_result();

                    while ($appointment = $appointments_result->fetch_assoc()) {
                        echo "<tr>";
                        echo "<td>" . $appointment['reference_no'] . "</td>";
                        echo "<td>" . $appointment['patient_name'] . "</td>";
                        echo "<td>" . date('F d, Y h:i A', strtotime($appointment['appointment_date_time'])) . "</td>";
                        echo "<td>" . $appointment['reason'] . "</td>";
                        echo "<td>" . ($appointment['status'] ?? 'Pending') . "</td>";
                        echo "<td>
                                <form action='mark_appointment_status.php' method='POST'>
                                    <input type='hidden' name='appointment_id' value='" . $appointment['appointment_id'] . "'>
                                    <button type='submit' name='status' value='Completed' class='btn btn-secondary'>Mark Completed</button>
                                </form>
                              </td>";
                        echo "</tr>";
                    }
                    ?>
                </tbody>
            </table>

            <h2 style="margin-top: 30px;">Completed Appointments</h2>
            <table class="table">
                <thead>
                    <tr>
                        <th>Reference No</th>
                        <th>Patient Name</th>
                        <th>Date & Time</th>
                        <th>Reason</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    // Fetch completed appointments for this doctor
                    $completed_sql = "SELECT a.*, p.patient_name 
                                      FROM appointment a 
                                      JOIN patient p ON a.reference_no = p.reference_no
                                      WHERE a.doctor_id = ? AND a.status = 'Completed' 
                                      ORDER BY a.appointment_date_time DESC
                                      LIMIT 10";
                    $completed_stmt = $conn->prepare($completed_sql);
                    $completed_stmt->bind_param("s", $doctor_id);
                    $completed_stmt->execute();
                    $completed_result = $completed_stmt->get_result();

                    while ($completed = $completed_result->fetch_assoc()) {
                        echo "<tr>";
                        echo "<td>" . $completed['reference_no'] . "</td>";
                        echo "<td>" . $completed['patient_name'] . "</td>";
                        echo "<td>" . date('F d, Y h:i A', strtotime($completed['appointment_date_time'])) . "</td>";
                        echo "<td>" . $completed['reason'] . "</td>";
                        echo "</tr>";
                    }
                    ?>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
<?php
$doctor_stmt->close();
$appointments_stmt->close();
$completed_stmt->close();
$conn->close();
?>