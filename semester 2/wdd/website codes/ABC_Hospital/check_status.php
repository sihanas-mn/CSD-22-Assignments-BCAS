<?php
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
            width: 80%;
            margin: auto;
            overflow: hidden;
            padding: 20px;
            background: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            border-radius: 5px;
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
        }
        .result-box {
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
        }
        .success {
            background-color: #4CAF50;
            color: white;
        }
        .pending {
            background-color: #FFC107;
            color: black;
        }
        .rejected {
            background-color: #F44336;
            color: white;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Check Appointment Status</h1>
    </div>
    
    <div class="container">
        <?php
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $reference_no = $_POST['reference_no'];

            // Prepare SQL to fetch appointment details
            $sql = "SELECT a.*, p.patient_name, d.doc_name, s.specialization_title 
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
                
                // Determine status class
                $status_class = 'pending';
                $status_text = 'Pending';
                if ($appointment['isConfirmed'] == 1) {
                    $status_class = 'success';
                    $status_text = 'Confirmed';
                } elseif ($appointment['isConfirmed'] == 0) {
                    $status_class = 'pending';
                    $status_text = 'Pending';
                }

                echo "<div class='result-box $status_class'>";
                echo "<h2>Appointment Details</h2>";
                echo "<p><strong>Reference Number:</strong> " . $appointment['reference_no'] . "</p>";
                echo "<p><strong>Patient Name:</strong> " . $appointment['patient_name'] . "</p>";
                echo "<p><strong>Appointment Date:</strong> " . $appointment['appointment_date_time'] . "</p>";
                echo "<p><strong>Specialization:</strong> " . $appointment['specialization_title'] . "</p>";
                echo "<p><strong>Doctor:</strong> " . $appointment['doc_name'] . "</p>";
                echo "<p><strong>Reason:</strong> " . $appointment['reason'] . "</p>";
                echo "<p><strong>Status:</strong> " . $status_text . "</p>";
                echo "</div>";
            } else {
                echo "<div class='result-box rejected'>";
                echo "<p>No appointment found with the given reference number.</p>";
                echo "</div>";
            }
        }
        ?>

        <form method="POST" action="">
            <div class="form-group">
                <label>Enter Reference Number:</label>
                <input type="text" name="reference_no" required>
            </div>
            <button type="submit" class="btn">Check Status</button>
        </form>
    </div>
</body>
</html>
<?php $conn->close(); ?>