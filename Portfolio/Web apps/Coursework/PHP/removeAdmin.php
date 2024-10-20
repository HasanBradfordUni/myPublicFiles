<?php
// Encrypt the password
$adminUsername = $_POST['username'];
$email = $_POST['email'];
$hashed_password = password_hash($_POST["password"], PASSWORD_BCRYPT);

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "smartLife";
// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$role = 1;
$stmt = $conn->prepare("DELETE FROM users WHERE Username = ? AND Email = ?");
$stmt->bind_param("ss", $adminUsername, $email);
$stmt->execute();
$conn->close();
// Check if the DELETE was successful
if ($stmt->affected_rows > 0) {
    echo "The admin was successfully deleted.";
} else {
    echo "No admin with the provided details exists.";
}
exit();