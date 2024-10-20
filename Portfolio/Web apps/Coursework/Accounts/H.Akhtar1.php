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
            <h1 class="mainHeading">My Account (Dev)</h1>
            <h2 class="subHeading">Log out at bottom of page</h2>
            <div class="account-info">
                <h2 class="subHeading">Account Information</h2>
                <h3 class="smallHeading">Current Details</h3><br>
                <p id="currentEmail">Your email: akhtarhasan2005@gmail.com</p>
                <p id="hashedPassword">Your hashed password: $2y$10$h31FNsCUk38yBPjndqS0RusQ1revM8hB82jE9r4r3VtsnuDpnzO76</p><br>
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
            </div><br><br>
            <p>Developer controls for H.Akhtar1:</p>
            <div class="buttonsPanel">
                <button onclick="window.location.href = '#addAdmin'" id="addAdmin">Go to add Admin section</button>
                <button onclick="window.location.href = '#addProduct'">Go to add Product section</button>
                <button onclick="window.location.href = '#removeAdmin'">Go to remove Admin section</button>
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
            <hr>
            <h2 class="subHeading" id="addProduct">Fill out this form to add an admin to the database</h2><br>
            <form class="adminForm" id="addAdminForm">
                <label for="username">Admin Username: </label>
                <input type="text" id="newAdminUsername" name="username" class="halfWidthInput"><br>
                <label for="email">Admin Email: </label>
                <input type="email" id="newAdminEmail" name="email" class="halfWidthInput"><br>
                <label for="password">Admin Password:</label>
                <input type="password" id="newAdminPassword" name="password" class="halfWidthInput"><br><br>
                <input type="submit" name="submit" value="Add this Admin" class="submitButton"><br><br>
            </form>
            <hr>
            <h2 class="subHeading">Fill out this form to add a product to the database</h2><br>
            <form method="post" action="../PHP/addProduct.php" class="productForm" id="addProdForm">
                <label for="prodName">Product Name*: </label>
                <input type="text" id="prodName" name="prodName" class="halfWidthInput" required><br>
                <label for="prodImg">Product Image (Link): </label>
                <input type="text" id="prodImg" name="prodImg" class="halfWidthInput"><br>
                <label for="prodCost">Product Cost*:</label>
                <input type="number" id="prodCost" name="prodCost" class="halfWidthInput" required step="0.01"><br><br>
                <label for="prodDesc">Product Description: </label>
                <input type="text" id="prodDesc" name="prodDesc" class="halfBoxInput"><br><br>
                <input type="submit" name="submit" value="Add Product" class="submitButton"><br><br>
            </form>
            <hr>
            <h2 class="subHeading">All current admins are listed below</h2>
            <table id="adminsTable">
                <tr>
                    <th>Admin Username</th>
                    <th>Admin Email</th>
                </tr>
                <tr id="row1">
                    <td>User123</td>
                    <td>user123@gmail.com</td>
                </tr>
            </table><br>
            <h2 class="subHeading" id="removeAdmin">Fill out this form to remove an admin from the database</h2><br>
            <form method="post" action="../PHP/removeAdmin.php" class="adminForm" id="removeAdminForm">
                <label for="username">Admin Username: </label>
                <input type="text" id="adminUsername" name="username" class="halfWidthInput"><br>
                <label for="email">Admin Email: </label>
                <input type="email" id="adminEmail" name="email" class="halfWidthInput"><br>
                <label for="password">Admin Password:</label>
                <input type="password" id="adminPassword" name="password" class="halfWidthInput"><br><br>
                <input type="submit" name="submit" value="Remove this Admin" class="submitButton"><br><br>
            </form><br>

            <div class="buttonsPanel">
                <button onclick='logoutUser()'>Log Out</button>
            </div>
        </div>
    </section>

    <script>
        try {
            fetch('../PHP/getAdmins.php')
                .then(response => response.text())
                .then(data => {
                    var lines = data.split('\n');
                    var table = document.getElementById("adminsTable");
                    var rows = table.getElementsByTagName("tr");

                    // Start from the second row (skip the heading row)
                    for (var i = rows.length - 1; i > 0; i--) {
                        table.deleteRow(i);
                    }

                    console.log(data);

                    for (let index = 0; index < lines.length; index++) {
                        const line = lines[index];
                        var words = line.split(' ');
                        var newRow = table.insertRow(); // Insert at the last position
                        newRow.id = "row" + (table.rows.length - 1); // Set the ID for the row

                        var adminUsername = words[0];
                        var adminEmail = words[1];

                        var cell1 = newRow.insertCell(0); // Insert at the first position
                        var cell2 = newRow.insertCell(1); // Insert at the second position

                        cell1.innerHTML = adminUsername;
                        cell2.innerHTML = adminEmail;
                    }
                });
        } catch (error) {
            console.log(error);
        }

        document.getElementById('addAdminForm').addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent the form from submitting normally

            var username = document.getElementById('newAdminUsername').value;
            var email = document.getElementById('newAdminEmail').value;
            var password = document.getElementById('newAdminPassword').value;

            fetch('../PHP/addAdmin.php', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: 'username=' + encodeURIComponent(username) + '&email=' + encodeURIComponent(email) + '&password=' + encodeURIComponent(password),
                })
                .then(response => response.text())
                .then(data => {
                    alert(data); // Alert the message
                    window.location.href = '../Accounts/H.Akhtar1.php';
                })
                .catch(error => console.error('Error:', error));
        });

        document.getElementById('addProdForm').addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent the form from submitting normally

            var name = document.getElementById('prodName').value;
            var image = document.getElementById('prodImg').value;
            var cost = document.getElementById('prodCost').value;
            var desc = document.getElementById('prodDesc').value;

            fetch('../PHP/addProduct.php', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: 'prodName=' + encodeURIComponent(name) + '&prodImg=' + encodeURIComponent(image) + '&prodCost=' + encodeURIComponent(cost) + '&prodDesc=' + encodeURIComponent(desc),
                })
                .then(response => response.text())
                .then(data => {
                    alert(data); // Alert the message
                    window.location.href = '../Accounts/H.Akhtar1.php';
                })
                .catch(error => console.error('Error:', error));
        });

        document.getElementById('removeAdminForm').addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent the form from submitting normally

            var username = document.getElementById('adminUsername').value;
            var email = document.getElementById('adminEmail').value;
            var password = document.getElementById('adminPassword').value;

            fetch('../PHP/removeAdmin.php', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: 'username=' + encodeURIComponent(username) + '&email=' + encodeURIComponent(email) + '&password=' + encodeURIComponent(password),
                })
                .then(response => response.text())
                .then(data => {
                    alert(data); // Alert the message
                    window.location.href = '../Accounts/H.Akhtar1.php';
                })
                .catch(error => console.error('Error:', error));
        });

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