<?php
session_start();
include 'db_connect.php';

if (!isset($_SESSION['user_type']) || $_SESSION['user_type'] !== 'admin') {
    header("Location: index.php");
    exit();
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard</title>
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
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }
        .section {
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
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
        .btn-danger {
            background: #dc3545;
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
    </style>
</head>
<body>
<?php
// Display success or error messages
if (isset($_GET['success'])) {
    echo "<div style='background-color: green; color: white; padding: 10px; text-align: center;'>" 
         . htmlspecialchars($_GET['success']) . "</div>";
}

if (isset($_GET['error'])) {
    echo "<div style='background-color: red; color: white; padding: 10px; text-align: center;'>" 
         . htmlspecialchars($_GET['error']) . "</div>";
}
?>
    <div class="header">
        <h1>Admin Dashboard</h1>
        <a href="logout.php" class="btn">Logout</a>
    </div>
    
    <div class="container">
        <div class="content">
            <div class="section">
                <h2>Add Doctor</h2>
                <form action="add_doctor.php" method="POST">
                    <div class="form-group">
                        <label>Doctor ID:</label>
                        <input type="text" name="doctor_id" required>
                    </div>
                    <div class="form-group">
                        <label>Name:</label>
                        <input type="text" name="doc_name" required>
                    </div>
                    <div class="form-group">
                        <label>Contact Number:</label>
                        <input type="number" name="contactNo" required>
                    </div>
                    <div class="form-group">
                        <label>Username:</label>
                        <input type="text" name="username" required>
                    </div>
                    <div class="form-group">
                        <label>Password:</label>
                        <input type="password" name="password" required>
                    </div>
                    <div class="form-group">
                        <label>Specialization:</label>
                        <select name="specialization_id" required>
                            <?php
                            $sql = "SELECT * FROM specialization";
                            $result = $conn->query($sql);
                            while($row = $result->fetch_assoc()) {
                                echo "<option value='" . $row['specialization_id'] . "'>" . $row['specialization_title'] . "</option>";
                            }
                            ?>
                        </select>
                    </div>
                    <button type="submit" class="btn">Add Doctor</button>
                </form>
            </div>

            <div class="section">
                <h2>Add Receptionist</h2>
                <form action="add_receptionist.php" method="POST">
                    <div class="form-group">
                        <label>Receptionist ID:</label>
                        <input type="text" name="receptionist_id" required>
                    </div>
                    <div class="form-group">
                        <label>Name:</label>
                        <input type="text" name="recep_name" required>
                    </div>
                    <div class="form-group">
                        <label>Contact Number:</label>
                        <input type="number" name="contactNo" required>
                    </div>
                    <div class="form-group">
                        <label>Username:</label>
                        <input type="text" name="username" required>
                    </div>
                    <div class="form-group">
                        <label>Password:</label>
                        <input type="password" name="password" required>
                    </div>
                    <button type="submit" class="btn">Add Receptionist</button>
                </form>
            </div>
        </div>

        <div class="content" style="margin-top: 20px;">
            <div class="section">
                <h2>Doctors List</h2>
                <table class="table">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Contact</th>
                        <th>Specialization</th>
                        <th>Action</th>
                    </tr>
                    <?php
                    $sql = "SELECT d.*, s.specialization_title FROM doctor d 
                            JOIN specialization s ON d.specialization_id = s.specialization_id";
                    $result = $conn->query($sql);
                    while($row = $result->fetch_assoc()) {
                        echo "<tr>";
                        echo "<td>" . $row['doctor_id'] . "</td>";
                        echo "<td>" . $row['doc_name'] . "</td>";
                        echo "<td>" . $row['contactNo'] . "</td>";
                        echo "<td>" . $row['specialization_title'] . "</td>";
                        echo "<td><a href='remove_doctor.php?id=" . $row['doctor_id'] . "' class='btn btn-danger'>Remove</a></td>";
                        echo "</tr>";
                    }
                    ?>
                </table>
            </div>

            <div class="section">
                <h2>Receptionists List</h2>
                <table class="table">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Contact</th>
                        <th>Action</th>
                    </tr>
                    <?php
                    $sql = "SELECT * FROM receptionist";
                    $result = $conn->query($sql);
                    while($row = $result->fetch_assoc()) {
                        echo "<tr>";
                        echo "<td>" . $row['receptionist_id'] . "</td>";
                        echo "<td>" . $row['recep_name'] . "</td>";
                        echo "<td>" . $row['contactNo'] . "</td>";
                        echo "<td><a href='remove_receptionist.php?id=" . $row['receptionist_id'] . "' class='btn btn-danger'>Remove</a></td>";
                        echo "</tr>";
                    }
                    ?>
                </table>
            </div>
        </div>
    </div>
</body>
</html>