<?php
session_start();
$reference_no = $_GET['ref'] ?? '';
?>
<!DOCTYPE html>
<html>
<head>
    <title>Appointment Booked - ABC Hospital</title>
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
            max-width: 600px;
            margin: auto;
            padding: 20px;
        }
        .success-box {
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            text-align: center;
            margin-top: 50px;
        }
        .reference {
            font-size: 24px;
            color: #005792;
            margin: 20px 0;
            padding: 10px;
            border: 2px dashed #005792;
            display: inline-block;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: #005792;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            margin: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="success-box">
            <h1>Appointment Booked Successfully!</h1>
            <p>Your reference number is:</p>
            <div class="reference">
                <?php echo htmlspecialchars($reference_no); ?>
            </div>
            <p>Please save this reference number to check your appointment status later.</p>
            <div>
                <a href="index.php" class="btn">Back to Home</a>
                <a href="check_status.php" class="btn">Check Status</a>
            </div>
        </div>
    </div>
</body>
</html>