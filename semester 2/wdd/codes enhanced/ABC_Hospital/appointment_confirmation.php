<?php
include 'db_connect.php';

// Check if reference number is provided
if (!isset($_GET['ref']) || empty($_GET['ref'])) {
    header("Location: index.php");
    exit();
}

$reference_no = $_GET['ref'];

// Fetch appointment details
$sql = "SELECT p.*, a.*, d.doc_name, s.specialization_title 
        FROM patient p
        JOIN appointment a ON p.reference_no = a.reference_no
        JOIN doctor d ON a.doctor_id = d.doctor_id
        JOIN specialization s ON d.specialization_id = s.specialization_id
        WHERE p.reference_no = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $reference_no);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows == 0) {
    header("Location: index.php");
    exit();
}

$appointment = $result->fetch_assoc();
?>
<!DOCTYPE html>
<html>
<head>
    <title>Appointment Confirmation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .confirmation-card {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 30px;
            width: 400px;
            text-align: center;
        }
        .reference-number {
            background-color: #005792;
            color: white;
            padding: 10px;
            margin: 20px 0;
            font-size: 1.5em;
            letter-spacing: 2px;
        }
        .details {
            text-align: left;
            margin-top: 20px;
        }
        .details p {
            margin: 10px 0;
            border-bottom: 1px solid #eee;
            padding-bottom: 5px;
        }
    </style>
</head>
<body>
    <div class="confirmation-card">
        <h1>Appointment Booked Successfully!</h1>
        
        <div class="reference-number">
            Reference Number: <?php echo $reference_no; ?>
        </div>
        
        <div class="details">
            <p><strong>Patient Name:</strong> <?php echo $appointment['patient_name']; ?></p>
            <p><strong>Doctor:</strong> <?php echo $appointment['doc_name']; ?></p>
            <p><strong>Specialization:</strong> <?php echo $appointment['specialization_title']; ?></p>
            <p><strong>Appointment Date:</strong> 
                <?php echo date('F d, Y h:i A', strtotime($appointment['appointment_date_time'])); ?>
            </p>
            <p><strong>Reason:</strong> <?php echo $appointment['reason']; ?></p>
        </div>

        <p>Please save your reference number. You can use it to check your appointment status.</p>
        
        <a href="index.php" style="text-decoration: none; color: white; background-color: #005792; padding: 10px; border-radius: 5px;">Back to Home</a>
    </div>
</body>
</html>