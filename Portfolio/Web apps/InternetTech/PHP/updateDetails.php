<html>

<head>
    <meta charset="UTF-8">
    <title>World of Books</title>
    <link rel="stylesheet" href="../CSS/Styles1.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>
    <h1>Email address and/or Password are being updated...</h1>
    <hr>
    <?php
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "worldOfBooks";
    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    } else {
        echo "<h5>Database Connection successfull</h5><br>";
    }
    $userExists = false;
    $sql = "SELECT * FROM logins";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        // output data of each row
        while ($row = $result->fetch_assoc()) {
            if ($row["Email"] == $_POST["email"] and password_verify($_POST["password"], $row["UserPassword"])) {
                echo "<h4>Password and email match, updating record...</h4><br>";
                $userExists = true;
                $userID = $row["UserID"];
                $ogEmail = $row["OriginalEmail"];
            }
        }
    } else {
        echo "<h4>Password and email don't match</h4><br>";
        $userExists = false;
    }

    // Get the username from the email
    $username = strstr($ogEmail, '@', true);
    // Define the path of the new account page
    $pagePath = "../Accounts/$username.php";

    if ($userExists) {
        $passwordValid = false;
        $email = $_POST['email1'];
        $password = $_POST['password1'];
        if (empty($email)) {
            $email = $_POST['email'];
            $passwordValid = true;
        } elseif (empty($password)) {
            $password = $_POST['password'];
            $passwordValid = true;
        } elseif ($password != $_POST['password2']) {
            echo "<h3>Password not valid, cannot update!</h3><br>";
            $passwordValid = false;
        } else {
            $passwordValid = true;
        }

        if ($passwordValid) {
            // Encrypt the password
            $hashed_password = password_hash($password, PASSWORD_BCRYPT);
            $updateSql = "UPDATE logins SET Email='$email', UserPassword='$hashed_password' WHERE UserID=$userID";
            // Load the HTML document
            $doc = new DOMDocument();
            libxml_use_internal_errors(true); // Disable libxml errors
            $doc->loadHTMLFile($pagePath);

            // Get the elements by ids
            $element1 = $doc->getElementById('currentEmail');
            $element2 = $doc->getElementById('hashedPassword');

            // Check if the element was found
            if ($element1 and $element2) {
                // Change the content of the element
                $element1->nodeValue = 'Your email: '.$email;
                $element2->nodeValue = 'Your hashed password: '.$hashed_password;

                // Save the changes to the file
                $doc->saveHTMLFile($pagePath);
            } else {
                echo "Elements not found";
            }
        }

        // Execute query and check for errors
        if ($conn->query($updateSql) === TRUE) {
            echo "<h3>Password and/or email updated successfully!</h3><br>";
        } else {
            echo "<h3>Password and/or email cannot be updated!</h3><br>";
        }
    } else {
        echo "<h3>Password and/or email cannot be updated!</h3><br>";
    }

    echo "<hr><h2>You will now be redirected back to your account page</h2><br>";

    // Redirect to the account page after 5 seconds using JavaScript
    echo "<script>setTimeout(function(){ window.location.href = '../Accounts/$username.php'; }, 5000);</script>";

    $conn->close();
    ?>
</body>

</html>