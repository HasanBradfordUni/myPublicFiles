<?php
// Start the session
session_start();

// Check if the form is submitted
if (isset($_POST['submit'])) {
    // Update the session variables
    $_SESSION['email'] = $_POST['email'];
    $_SESSION['password'] = $_POST['password'];
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Your Smart Life account</title>
    <link rel="stylesheet" href="../CSS/accountStyles.css">
    <link rel="stylesheet" href="../CSS/Styles.css">
    <script src="../JavaScript/basicJs.js"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <div class="container">
        <h1 class="mainHeading">My Account</h1>
        <div class="account-info">
            <h2 class="subHeading">Account Information</h2>
            <h3 class="smallHeading">Current Details</h3><br>
            <p id="currentEmail">Your email: {{email}}</p>
            <p id="hashedPassword">Your hashed password: {{password}}</p><br>
            <h3>Update your details</h3><br>
            <form method="post" action="../PHP/updateDetails.php" class="detailsForm">
                <label for="email">Current Email: </label>
                <input type="email" id="email" name="email" class="halfWidthInput"><br>
                <script type="text/javascript">
                    var pContent = document.getElementById("currentEmail").innerHTML;
                    var subString = pContent.substring(12);
                    
                    var emailInput = document.getElementById("email");
                    emailInput.value = subString;
                    emailInput.readOnly = true;
                </script>
                <label for="email1">New Email: </label>
                <input type="email" id="email1" name="email1" class="halfWidthInput">
                <label for="email2">Confirm New Email:</label>
                <input type="email" id="email2" name="email2" class="halfWidthInput"><br><br>
                <label for="password">Current Password:</label>
                <input type="password" id="password" name="password" class="halfWidthInput"><br>
                <label for="password1">New Password:</label>
                <input type="password" id="password1" name="password1" class="halfWidthInput">
                <label for="password2">Confirm New Password:</label>
                <input type="password" id="password2" name="password2" class="halfWidthInput"><br><br>
                <input type="submit" name="submit" value="Update" class="submitButton"><br><br>
            </form>
        </div><hr>
        <h2 class="subHeading">Purchased Gadgets</h2>
        <table class="purchased-gadgets">
            <tr>
                <th>Product Image</th>
                <th>Product Name</th>
                <th>Product Price</th>
                <th>Date Purchased</th>
            </tr>
            <tr id="row1">
                <td>No image atm</td>
                <td class="subHeading"><a href="#">Product 1</a></td>
                <td class="prodPrice">&#163;9.99</td>
                <td class="smallHeading">28 April 2024</td>
            </tr>
        </table>
    </div>
</body>
</html>