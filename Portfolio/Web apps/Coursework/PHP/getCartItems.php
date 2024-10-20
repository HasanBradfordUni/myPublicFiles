<?php
// Start the session
session_start();

// Check if the user is logged in
if (isset($_SESSION['UserId'])) {
    $userID = $_SESSION['UserId'];
}

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
// Perform the SQL query
$totalPrice = 0.00;
$sql = "SELECT * FROM cart_products";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    // output data of each row
    while ($row = $result->fetch_assoc()) {
        if ($row["userId"] == $userID) {
            $sql2 = "SELECT * FROM products";
            $result2 = $conn->query($sql2);
            if ($result2->num_rows > 0) {
                // output data of each row
                while ($row2 = $result2->fetch_assoc()) {
                    if ($row2["productID"] == $row["productId"]) {
                        echo $row2["productName"] .";". $row2["productPrice"] .";".$row2["productImgSrc"]."\n";
                        $totalPrice += $row2["productPrice"];
                    }
                }
            }
        }
    }
    echo $totalPrice;
} else {
    echo "No data.";
}
exit();
