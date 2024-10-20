<?php
// Start the session
session_start();

// Check if the user is logged in
if (isset($_SESSION['UserId'])) {
    $userID = $_SESSION['UserId'];
}

$productID = $_POST['productId'];
$productID = intval($productID);

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
if (isset($_SESSION['UserId'])) {
    $stmt = $conn->prepare("INSERT INTO cart_products (userId, productId) VALUES (?, ?)");
    $stmt->bind_param("ii", $userID, $productID);
    $stmt->execute();
    $conn->close();
    // Check if the INSERT was successful
    if ($stmt->affected_rows > 0) {
        echo "The product was successfully added to cart.";
    } else {
        echo "Product adding to cart unsuccessful.";
    }
} else {
    echo "User isn't logged in! Must be logged in to add to cart!";
}

exit();
