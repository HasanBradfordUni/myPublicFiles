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
    <header>
        <h1>
            <img src="../HTML/Images/logo.png" alt="The logo for this website" width="50" height="50" class="logo">
            Smart Life
            <img src="../HTML/Images/logo.png" alt="The logo for this website" width="50" height="50" class="logo">
        </h1>
        <hr>

        <div class="menuBar">
            <ul class="nav">
                <li class="nav" id="currentPage"><a class="nav" href="../HTML/index.html">Home</a></li>
                <li class="nav"><a class="nav" href="../HTML/about.html">About</a></li>
                <li class="nav"><a class="nav" href="../HTML/contact.html">Contact</a></li>
                <li class="nav"><a class="nav" href="../HTML/shop.html">Shop</a></li>
            </ul>
            <div class="icons">
                <a href="../HTML/cart.html"> <img src="../HTML/Images/cart.png" class="cart"> </a>
                <a href="../HTML/login.html" id="accountButton"> <img src="../HTML/Images/account.png" class="account"> </a>
            </div>
        </div>
    </header>

    <section class="mainBody">
        <div class="container">
            <h1 class="mainHeading">My Account (Admin)</h1>
            <h2 class="subHeading">Log out at bottom of page</h2>
            <div class="account-info">
                <h2 class="subHeading">Account Information</h2>
                <h3 class="smallHeading">Current Details</h3><br>
                <p id="currentEmail">Your email: hakhta26@bradford.ac.uk</p>
                <p id="hashedPassword">Your hashed password: $2y$10$A/KjcDuGjhM1EzbKxao29exsDj9dRxs40PMOOiGt9nuVaZ4PKxdJ.</p><br>
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
            </div>
            <hr>
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
            </table><br>

            <div class="buttonsPanel">
                <button onclick='logoutUser()'>Log Out</button>
            </div>
        </div>
    </section>

    <script>
        function logoutUser() {
            fetch('../PHP/logoutUser.php', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                })
                .then(response => response.text())
                .then(data => {
                    alert("You have been logged out"); // Alert the message
                    window.location.href = '../HTML/index.html';
                })
                .catch(error => console.error('Error:', error));
        }
    </script>
</body>

</html>