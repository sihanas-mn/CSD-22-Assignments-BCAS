<?php
session_start();
include 'db_connect.php';
?>
<!DOCTYPE html>
<html>
<head>
    <title>Check Appointment Status</title>
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
            width: 60%;
            margin: auto;
            overflow: hidden;
            padding: 20px;
            background: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            border-radius: 5px;
            margin-top: 2rem;
        }
        .header {
            background: #005792;
            color: white;
            text-align: center;
            padding: 1rem;
        }
        .form-group {
            margin-bottom: 1rem;
        }
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
        }
        .form-group input {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: #005792;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
        }
        .status-box {
            background-color: #e9ecef;
            border: 1px solid #ced4da;
            padding: 15px;
            margin-top: 20px;
        }
        .status-confirmed {
            color: green;
        }
        .status-pending {
            color: orange;
        }
        .status-rejected {
            color: red;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Check Appointment Status</h1>
    </div>
    
    <div class="container">
        <?php 
        if (isset($_GET['reference'])) {
            $reference_no = $_GET['reference'];
            
            // Query to get appointment details
            $sql = "SELECT p.patient_name, a.appointment_date_time, a.reason, 
                           d.doc_name, s.specialization_title, a.isConfirmed
                    FROM appointment a
                    JOIN patient p ON a.reference_no = p.reference_no
                    JOIN doctor d ON a.doctor_id = d.doctor_id
                    JOIN specialization s ON d.specialization_id = s.specialization_id
                    WHERE a.reference_no = ?";
            
            $stmt = $conn->prepare($sql);
            $stmt->bind_param("s", $reference_no);
            $stmt->execute();
            $result = $stmt->get_result();
            
            if ($result->num_rows > 0) {
                $appointment = $result->fetch_assoc();
                ?>
                <div class="status-box">
                    <h2>Appointment Details</h2>
                    <p><strong>Patient Name:</strong> <?php echo htmlspecialchars($appointment['patient_name']); ?></p>
                    <p><strong>Doctor:</strong> <?php echo htmlspecialchars($appointment['doc_name']); ?> 
                       (<?php echo htmlspecialchars($appointment['specialization_title']); ?>)</p>
                    <p><strong>Date and Time:</strong> <?php echo htmlspecialchars($appointment['appointment_date_time']); ?></p>
                    <p><strong>Reason:</strong> <?php echo htmlspecialchars($appointment['reason']); ?></p>
                    <p><strong>Status:</strong> 
                        <?php 
                        if ($appointment['isConfirmed'] === 1) {
                            echo "<span class='status-confirmed'>Confirmed</span>";
                        } else {
                            echo "<span class='status-pending'>Pending</span>";
                        }
                        ?>
                    </p>
                </div>
                <?php
            } else {
                echo "<div class='status-box status-rejected'>No appointment found with this reference number.</div>";
            }
        }
        ?>
        
        <form method="GET" action="">
            <div class="form-group">
                <label>Enter Reference Number:</label>
                <input type="text" name="reference" required maxlength="10" 
                       placeholder="Enter your 10-character reference number">
            </div>
            <button type="submit" class="btn">Check Status</button>
        </form>
    </div>
</body>
</html>