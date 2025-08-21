<?php
include 'db_connect.php';

// Check if reference number is provided
if (!isset($_GET['reference_no'])) {
    header("Location: index.php");
    exit();
}

$reference_no = $_GET['reference_no'];

// Fetch appointment details
$sql = "SELECT a.*, d.doc_name, s.specialization_title 
        FROM appointment a
        JOIN doctor d ON a.doctor_id = d.doctor_id
        JOIN specialization s ON d.specialization_id = s.specialization_id
        WHERE a.reference_no = ?";

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
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            width: 400px;
            text-align: center;
        }
        .reference-number {
            background-color: #005792;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin: 20px 0;
            font-weight: bold;
        }
        .details {
            margin-top: 20px;
            text-align: left;
        }
    </style>
</head>
<body>
    <div class="confirmation-card">
        <h1>Appointment Booked</h1>
        <p>Your appointment has been successfully booked!</p>
        
        <div class="reference-number">
            Reference Number: <?php echo $reference_no; ?>
        </div>
        
        <div class="details">
            <p><strong>Doctor:</strong> <?php echo $appointment['doc_name']; ?></p>
            <p><strong>Specialization:</strong> <?php echo $appointment['specialization_title']; ?></p>
            <p><strong>Date and Time:</strong> 
                <?php 
                $datetime = new DateTime($appointment['appointment_date_time']);
                echo $datetime->format('F d, Y h:i A'); 
                ?>
            </p>
            <p><strong>Reason:</strong> <?php echo $appointment['reason']; ?></p>
        </div>
        
        <p>Please keep your reference number for future tracking.</p>
        <a href="index.php" style="text-decoration: none; color: #005792;">Back to Home</a>
    </div>
</body>
</html>
<?php
$stmt->close();
$conn->close();
?>