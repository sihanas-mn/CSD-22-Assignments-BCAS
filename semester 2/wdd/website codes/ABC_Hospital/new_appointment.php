<?php
session_start();
include 'db_connect.php';

// Function to generate unique reference number
function generateReferenceNumber($conn) {
    // Try to generate a unique reference number
    do {
        // Generate a random 10-character reference number
        $reference_no = 'REF' . str_pad(rand(0, 9999999999), 10, '0', STR_PAD_LEFT);
        
        // Check if this reference number already exists
        $check_sql = "SELECT * FROM appointment WHERE reference_no = ?";
        $check_stmt = $conn->prepare($check_sql);
        $check_stmt->bind_param("s", $reference_no);
        $check_stmt->execute();
        $result = $check_stmt->get_result();
    } while ($result->num_rows > 0);
    
    return $reference_no;
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Book New Appointment</title>
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
        .form-group input, .form-group select {
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
        .success-box {
            background: #4CAF50;
            color: white;
            padding: 15px;
            text-align: center;
            margin-top: 20px;
            border-radius: 5px;
        }
        .error-box {
            background: #f44336;
            color: white;
            padding: 15px;
            text-align: center;
            margin-top: 20px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Book New Appointment</h1>
    </div>
    
    <div class="container">
        <?php
        // Check if form is submitted
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            // Collect form data
            $patient_name = $_POST['patient_name'];
            $email = $_POST['email'];
            $address = $_POST['address'];
            $dob = $_POST['dob'];
            $contact_no = $_POST['contact_no'];
            $specialization_id = $_POST['specialization'];
            $appointment_datetime = $_POST['appointment_datetime'];
            $reason = $_POST['reason'];

            // Start transaction
            $conn->begin_transaction();

            try {
                // First, check if specialization exists and get a doctor
                $doctor_sql = "SELECT doctor_id FROM doctor WHERE specialization_id = ? LIMIT 1";
                $doctor_stmt = $conn->prepare($doctor_sql);
                $doctor_stmt->bind_param("s", $specialization_id);
                $doctor_stmt->execute();
                $doctor_result = $doctor_stmt->get_result();

                if ($doctor_result->num_rows == 0) {
                    throw new Exception("No doctor available for selected specialization");
                }

                $doctor_row = $doctor_result->fetch_assoc();
                $doctor_id = $doctor_row['doctor_id'];

                // Generate unique reference number
                $reference_no = generateReferenceNumber($conn);

                // Insert patient first
                $patient_sql = "INSERT INTO patient (reference_no, patient_name, email, address, DoB, contactNo) 
                                VALUES (?, ?, ?, ?, ?, ?)";
                $patient_stmt = $conn->prepare($patient_sql);
                $patient_stmt->bind_param("sssssi", $reference_no, $patient_name, $email, $address, $dob, $contact_no);
                $patient_stmt->execute();

                // Then insert appointment
                $appointment_sql = "INSERT INTO appointment 
                                    (appointment_id, appointment_date_time, reason, isConfirmed, 
                                    doctor_id, reference_no) 
                                    VALUES (?, ?, ?, false, ?, ?)";
                $appointment_stmt = $conn->prepare($appointment_sql);
                $appointment_id = generateReferenceNumber($conn); // Use similar generation for appointment ID
                $appointment_stmt->bind_param("sssss", $appointment_id, $appointment_datetime, $reason, $doctor_id, $reference_no);
                $appointment_stmt->execute();

                // Commit transaction
                $conn->commit();

                // Display success message with reference number
                echo "<div class='success-box'>";
                echo "<h2>Appointment Booked Successfully!</h2>";
                echo "<p>Your Reference Number is: <strong>$reference_no</strong></p>";
                echo "<p>Please save this reference number to check your appointment status.</p>";
                echo "</div>";
            } catch (Exception $e) {
                // Rollback transaction
                $conn->rollback();

                // Display error message
                echo "<div class='error-box'>";
                echo "Error: " . $e->getMessage();
                echo "</div>";
            }
        }
        ?>

        <form method="POST" action="">
            <div class="form-group">
                <label>Patient Name:</label>
                <input type="text" name="patient_name" required>
            </div>
            <div class="form-group">
                <label>Email:</label>
                <input type="email" name="email" required>
            </div>
            <div class="form-group">
                <label>Address:</label>
                <input type="text" name="address" required>
            </div>
            <div class="form-group">
                <label>Date of Birth:</label>
                <input type="date" name="dob" required>
            </div>
            <div class="form-group">
                <label>Contact Number:</label>
                <input type="tel" name="contact_no" required>
            </div>
            <div class="form-group">
                <label>Specialization:</label>
                <select name="specialization" required>
                    <?php
                    // Fetch specializations
                    $spec_sql = "SELECT * FROM specialization";
                    $spec_result = $conn->query($spec_sql);
                    while ($spec_row = $spec_result->fetch_assoc()) {
                        echo "<option value='" . $spec_row['specialization_id'] . "'>" 
                             . $spec_row['specialization_title'] . "</option>";
                    }
                    ?>
                </select>
            </div>
            <div class="form-group">
                <label>Appointment Date and Time:</label>
                <input type="datetime-local" name="appointment_datetime" required>
            </div>
            <div class="form-group">
                <label>Reason for Appointment:</label>
                <input type="text" name="reason" required>
            </div>
            <button type="submit" class="btn">Book Appointment</button>
        </form>
    </div>
</body>
</html>
<?php $conn->close(); ?>