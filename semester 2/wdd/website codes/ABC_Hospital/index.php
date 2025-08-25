<?php
session_start();
include 'db_connect.php';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ABC Hospital - Healthcare Solutions</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --accent-color: #2ecc71;
            --light-bg: #f4f6f7;
            --text-color: #333;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background: linear-gradient(135deg, #f6f8f9 0%, #e5ebee 100%);
        }

        .navbar {
            background-color: var(--primary-color);
            padding: 1rem 5%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .logo {
            display: flex;
            align-items: center;
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
        }

        .logo i {
            margin-right: 10px;
            color: var(--secondary-color);
        }

        .hero {
            display: flex;
            align-items: center;
            padding: 4rem 5%;
            background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
            color: white;
        }

        .hero-content {
            flex: 1;
            padding-right: 4rem;
        }

        .hero-content h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            color: white;
        }

        .hero-content p {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            color: rgba(255,255,255,0.8);
        }

        .hero-image {
            flex: 1;
            text-align: right;
        }

        .hero-image img {
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .services {
            display: flex;
            justify-content: space-between;
            padding: 4rem 5%;
            background: white;
        }

        .service-card {
            flex: 1;
            margin: 0 15px;
            text-align: center;
            padding: 2rem;
            background: var(--light-bg);
            border-radius: 10px;
            transition: transform 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .service-card:hover {
            transform: translateY(-10px);
        }

        .service-card i {
            font-size: 3rem;
            color: var(--secondary-color);
            margin-bottom: 1rem;
        }

        .login-section {
            background: var(--light-bg);
            padding: 4rem 5%;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .login-container {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            width: 400px;
        }

        .login-container h2 {
            text-align: center;
            color: var(--primary-color);
            margin-bottom: 1.5rem;
        }

        .form-group {
            margin-bottom: 1rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: var(--text-color);
        }

        .form-group select,
        .form-group input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 5px;
            transition: border-color 0.3s ease;
        }

        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: var(--secondary-color);
        }

        .btn {
            display: block;
            width: 100%;
            padding: 0.75rem;
            background: var(--secondary-color);
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s ease;
        }

        .btn:hover {
            background: var(--primary-color);
        }

        .patient-options {
            display: flex;
            justify-content: space-between;
            margin-top: 2rem;
        }

        .patient-btn {
            flex: 1;
            margin: 0 10px;
            padding: 0.75rem;
            background: var(--accent-color);
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s ease;
        }

        .patient-btn:hover {
            background: var(--primary-color);
        }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar">
        <div class="logo">
            <i class="fas fa-hospital"></i> ABC Hospital
        </div>
        <div>
            <a href="#" class="btn">Emergency</a>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <h1>Your Health, Our Priority</h1>
            <p>Providing compassionate and advanced healthcare solutions with cutting-edge medical technology and expert care.</p>
        </div>
        <div class="hero-image">
            <img src="/api/placeholder/600/400" alt="Hospital Image" />
        </div>
    </section>

    <!-- Services Section -->
    <section class="services">
        <div class="service-card">
            <i class="fas fa-user-md"></i>
            <h3>Expert Doctors</h3>
            <p>Highly qualified and experienced medical professionals</p>
        </div>
        <div class="service-card">
            <i class="fas fa-ambulance"></i>
            <h3>Emergency Care</h3>
            <p>24/7 emergency medical services and rapid response</p>
        </div>
        <div class="service-card">
            <i class="fas fa-heartbeat"></i>
            <h3>Advanced Treatment</h3>
            <p>State-of-the-art medical equipment and treatments</p>
        </div>
    </section>

    <!-- Login Section -->
    <section class="login-section">
        <div style="flex: 1; padding-right: 4rem;">
            <h2>Patient Services</h2>
            <div class="patient-options">
                <a href="new_appointment.php" class="patient-btn">
                    <i class="fas fa-calendar-plus"></i> Book Appointment
                </a>
                <a href="check_status.php" class="patient-btn">
                    <i class="fas fa-search"></i> Check Status
                </a>
            </div>
        </div>

        <div class="login-container">
            <h2>Staff Login</h2>
            <form action="login_process.php" method="POST">
                <div class="form-group">
                    <label>User Type</label>
                    <select name="user_type" required>
                        <option value="">Select User Type</option>
                        <option value="admin">Admin</option>
                        <option value="doctor">Doctor</option>
                        <option value="receptionist">Receptionist</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit" class="btn">Login</button>
            </form>
        </div>
    </section>
</body>
</html>