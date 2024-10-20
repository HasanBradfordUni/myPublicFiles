<!DOCTYPE html>
<?php // Start the session
session_start();

// Check if the form is submitted
if (isset($_POST['submit'])) {
    // Update the session variables
    $_SESSION['email'] = $_POST['email'];
    $_SESSION['password'] = $_POST['password'];
}
?><html>
<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta charset="UTF-8">
    <title>Your World of Books account</title>
    <link rel="stylesheet" href="../CSS/AccountStyles.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <div class="container">
        <h1>My Account</h1>
        <div class="account-info">
            <h2>Account Information</h2>
            <h3>Current Details</h3><br>
            <p id="currentEmail">Your email: hakhta26@bradford.ac.uk</p>
            <p id="hashedPassword">Your hashed password: $2y$10$74J7axtrjfPAENrfSm8uJOz2PoCpf/5GqN5dNQfA..51l8Ca3QG1q</p><br>
            <h3>Update your details</h3><br>
            <form method="post" action="../PHP/updateDetails.php">
                <label for="email">Current Email: </label>
                <input type="email" id="email" name="email"><br>
                <script type="text/javascript">
                    var pContent = document.getElementById("currentEmail").innerHTML;
                    var subString = pContent.substring(12);
                    
                    var emailInput = document.getElementById("email");
                    emailInput.value = subString;
                    emailInput.readOnly = true;
                </script>
                <label for="email1">New Email: </label>
                <input type="email" id="email1" name="email1">
                <label for="email2">Confirm New Email:</label>
                <input type="email" id="email2" name="email2"><br><br>
                <label for="password">Current Password:</label>
                <input type="password" id="password" name="password"><br>
                <label for="password1">New Password:</label>
                <input type="password" id="password1" name="password1">
                <label for="password2">Confirm New Password:</label>
                <input type="password" id="password2" name="password2"><br><br>
                <input type="submit" name="submit" value="Update">
            </form>
        </div><hr>
        <div class="purchased-books">
            <h2>Purchased Books</h2>
            <div class="book">
                <h3>Book Title 1</h3>
                <p>Author: Author Name 1</p>
            </div>
            <div class="book">
                <h3>Book Title 2</h3>
                <p>Author: Author Name 2</p>
            </div>
            <!-- More books can be added here -->
        </div>
    </div>
</body>
</html>
