<?php
session_start();
include 'db_connect.php';

// Function to generate unique 10-character reference number
function generateReferenceNumber($conn) {
    while (true) {
        // Generate a random 10-character alphanumeric reference number
        $reference_no = strtoupper(substr(md5(uniqid(mt_rand(), true)), 0, 10));
        
        // Check if this reference number already exists in the patient table
        $check_sql = "SELECT * FROM patient WHERE reference_no = ?";
        $stmt = $conn->prepare($check_sql);
        $stmt->bind_param("s", $reference_no);
        $stmt->execute();
        $result = $stmt->get_result();
        
        // If no existing reference number found, return it
        if ($result->num_rows == 0) {
            return $reference_no;
        }
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>New Appointment</title>
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
        .form-group input, 
        .form-group select, 
        .form-group textarea {
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
        .btn:hover {
            background: #003d66;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Book New Appointment</h1>
    </div>
    
    <div class="container">
        <form action="process_appointment.php" method="POST">
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
                <textarea name="address" required></textarea>
            </div>
            
            <div class="form-group">
                <label>Date of Birth:</label>
                <input type="date" name="dob" required>
            </div>
            
            <div class="form-group">
                <label>Contact Number:</label>
                <input type="number" name="contactNo" required>
            </div>
            
            <div class="form-group">
                <label>Select Doctor Specialization:</label>
                <select name="specialization_id" id="specialization" required>
                    <option value="">Select Specialization</option>
                    <?php
                    // Fetch specializations from database
                    $sql = "SELECT * FROM specialization";
                    $result = $conn->query($sql);
                    while($row = $result->fetch_assoc()) {
                        echo "<option value='" . $row['specialization_id'] . "'>" 
                             . $row['specialization_title'] . "</option>";
                    }
                    ?>
                </select>
            </div>
            
            <div class="form-group">
                <label>Select Doctor:</label>
                <select name="doctor_id" id="doctor" required>
                    <option value="">Select Doctor</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Appointment Date and Time:</label>
                <input type="datetime-local" name="appointment_datetime" required>
            </div>
            
            <div class="form-group">
                <label>Reason for Appointment:</label>
                <textarea name="reason" required></textarea>
            </div>
            
            <button type="submit" class="btn">Book Appointment</button>
        </form>
    </div>

    <script>
        // Dynamic doctor selection based on specialization
        document.getElementById('specialization').addEventListener('change', function() {
            var specializationId = this.value;
            var doctorSelect = document.getElementById('doctor');
            
            // Clear previous doctor options
            doctorSelect.innerHTML = '<option value="">Select Doctor</option>';
            
            if (specializationId) {
                // Fetch doctors for selected specialization via AJAX
                fetch('get_doctors.php?specialization_id=' + specializationId)
                    .then(response => response.json())
                    .then(doctors => {
                        doctors.forEach(doctor => {
                            var option = document.createElement('option');
                            option.value = doctor.doctor_id;
                            option.text = doctor.doc_name;
                            doctorSelect.appendChild(option);
                        });
                    });
            }
        });
    </script>
</body>
</html>