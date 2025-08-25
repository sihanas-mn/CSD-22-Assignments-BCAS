<?php
session_start();
include 'db_connect.php';

// Check if user is logged in as receptionist
if (!isset($_SESSION['user_type']) || $_SESSION['user_type'] !== 'receptionist') {
    header("Location: index.php");
    exit();
}

// Handle appointment confirmation/rejection
if (isset($_POST['action']) && isset($_POST['appointment_id'])) {
    $appointment_id = $_POST['appointment_id'];
    if ($_POST['action'] === 'confirm') {
        $sql = "UPDATE appointment SET isConfirmed = true WHERE appointment_id = ?";
    } else if ($_POST['action'] === 'reject') {
        $sql = "DELETE FROM appointment WHERE appointment_id = ?";
    }
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $appointment_id);
    $stmt->execute();
    $stmt->close();
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Receptionist Dashboard</title>
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
            margin-bottom: 20px;
        }
        .section {
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .btn {
            display: inline-block;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            color: white;
            margin: 0 5px;
        }
        .btn-confirm {
            background: #28a745;
        }
        .btn-reject {
            background: #dc3545;
        }
        .btn-logout {
            background: #6c757d;
        }
        .table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
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
        .table tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .status-filter {
            margin-bottom: 20px;
        }
        .status-filter select {
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #ddd;
        }
        .alert {
            padding: 15px;
            margin-bottom: 20px;
            border: 1px solid transparent;
            border-radius: 4px;
        }
        .alert-success {
            color: #155724;
            background-color: #d4edda;
            border-color: #c3e6cb;
        }
        .alert-info {
            color: #0c5460;
            background-color: #d1ecf1;
            border-color: #bee5eb;
        }
        .form-inline {
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Receptionist Dashboard</h1>
        <a href="logout.php" class="btn btn-logout">Logout</a>
    </div>

    <div class="container">
        <div class="section">
            <h2>Pending Appointments</h2>
            <div class="status-filter">
                <label>Filter by Doctor:</label>
                <select id="doctor-filter" onchange="filterAppointments()">
                    <option value="">All Doctors</option>
                    <?php
                    $sql = "SELECT doctor_id, doc_name FROM doctor";
                    $result = $conn->query($sql);
                    while($row = $result->fetch_assoc()) {
                        echo "<option value='" . $row['doctor_id'] . "'>" . $row['doc_name'] . "</option>";
                    }
                    ?>
                </select>
            </div>

            <table class="table">
                <thead>
                    <tr>
                        <th>Reference No</th>
                        <th>Patient Name</th>
                        <th>Doctor</th>
                        <th>Date & Time</th>
                        <th>Reason</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    $sql = "SELECT a.*, p.patient_name, d.doc_name 
                            FROM appointment a 
                            JOIN patient p ON a.reference_no = p.reference_no 
                            JOIN doctor d ON a.doctor_id = d.doctor_id 
                            WHERE a.isConfirmed = false 
                            ORDER BY a.appointment_date_time ASC";
                    $result = $conn->query($sql);

                    if ($result->num_rows > 0) {
                        while($row = $result->fetch_assoc()) {
                            echo "<tr data-doctor='" . $row['doctor_id'] . "'>";
                            echo "<td>" . $row['reference_no'] . "</td>";
                            echo "<td>" . $row['patient_name'] . "</td>";
                            echo "<td>" . $row['doc_name'] . "</td>";
                            echo "<td>" . $row['appointment_date_time'] . "</td>";
                            echo "<td>" . $row['reason'] . "</td>";
                            echo "<td>";
                            echo "<form class='form-inline' method='POST'>";
                            echo "<input type='hidden' name='appointment_id' value='" . $row['appointment_id'] . "'>";
                            echo "<button type='submit' name='action' value='confirm' class='btn btn-confirm'>Confirm</button>";
                            echo "<button type='submit' name='action' value='reject' class='btn btn-reject'>Reject</button>";
                            echo "</form>";
                            echo "</td>";
                            echo "</tr>";
                        }
                    } else {
                        echo "<tr><td colspan='6' style='text-align: center;'>No pending appointments</td></tr>";
                    }
                    ?>
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>Confirmed Appointments</h2>
            <table class="table">
                <thead>
                    <tr>
                        <th>Reference No</th>
                        <th>Patient Name</th>
                        <th>Doctor</th>
                        <th>Date & Time</th>
                        <th>Reason</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    $sql = "SELECT a.*, p.patient_name, d.doc_name 
                            FROM appointment a 
                            JOIN patient p ON a.reference_no = p.reference_no 
                            JOIN doctor d ON a.doctor_id = d.doctor_id 
                            WHERE a.isConfirmed = true 
                            ORDER BY a.appointment_date_time ASC";
                    $result = $conn->query($sql);

                    if ($result->num_rows > 0) {
                        while($row = $result->fetch_assoc()) {
                            echo "<tr>";
                            echo "<td>" . $row['reference_no'] . "</td>";
                            echo "<td>" . $row['patient_name'] . "</td>";
                            echo "<td>" . $row['doc_name'] . "</td>";
                            echo "<td>" . $row['appointment_date_time'] . "</td>";
                            echo "<td>" . $row['reason'] . "</td>";
                            echo "</tr>";
                        }
                    } else {
                        echo "<tr><td colspan='5' style='text-align: center;'>No confirmed appointments</td></tr>";
                    }
                    ?>
                </tbody>
            </table>
        </div>
    </div>

    <script>
    function filterAppointments() {
        const doctorId = document.getElementById('doctor-filter').value;
        const rows = document.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            if (!doctorId || row.getAttribute('data-doctor') === doctorId) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
    </script>
</body>
</html>