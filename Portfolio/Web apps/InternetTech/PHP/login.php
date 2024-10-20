<html>

<head>
    <meta charset="UTF-8">
    <title>World of Books</title>
    <link rel="stylesheet" href="../CSS/Styles1.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>
    <h1>Your login details are as follows:</h1>
    <?php
    echo "<h2>Your email is: " . $_POST["email"] . "</h2><br>";
    // Encrypt the password
    $hashed_password = password_hash($_POST["password"], PASSWORD_BCRYPT);
    echo "<h3>Your encrypted password (as stored in database) is: " . $hashed_password . "</h3><br><hr>";
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
        echo "<h2>Connection successfull</h2><br>";
    }
    $userExists = false;
    $sql = "SELECT * FROM logins";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        // output data of each row
        while ($row = $result->fetch_assoc()) {
            if ($row["Email"] == $_POST["email"] and password_verify($_POST["password"], $row["UserPassword"])) {
                echo "<h4>User exists, logging you in...</h4><br>";
                $userExists = true;
            }
        }
    } else {
        echo "<h4>User doesn't exist, you will now be registered</h4><br>";
        $userExists = false;
    }
    // Get the username from the email
    $username = strstr($_POST["email"], '@', true);
    // Define the path of the new account page
    $pagePath = "../Accounts/$username.php";
    if ($userExists) {
        echo "<h4>User exists, logging you in...</h4><br>";
    } else {
        echo "<h4>User doesn't exist, you will now be registered</h4><br>";
        $stmt = $conn->prepare("INSERT INTO logins (Email, UserPassword, OriginalEmail) VALUES (?, ?, ?)");
        $stmt->bind_param("sss", $_POST["email"], $hashed_password, $_POST["email"]);
        $stmt->execute();
    }
    try {
        // Check if the page exists
        if (file_exists($pagePath)) {
            // Redirect to the account page after 5 seconds using JavaScript
            echo "<script>setTimeout(function(){ window.location.href = '../Accounts/$username.php'; }, 5000);</script>";
        } else {
            throw new Exception('Page not found');
        }
    } catch (Exception $e) {
        // Get the content of the template file
        $templateContent = file_get_contents('../Accounts/template.php');
        // Create the new account page with the template content
        file_put_contents($pagePath, $templateContent);
        // Replace placeholders with actual data
        $pageContent = str_replace(['{{email}}', '{{password}}'], [$_POST["email"], $hashed_password], $templateContent);
        // Write the content to a new file
        file_put_contents("../Accounts/$username.php", $pageContent);
        // Redirect to the account page after 5 seconds using JavaScript
        echo "<script>setTimeout(function(){ window.location.href = '../Accounts/$username.php'; }, 5000);</script>";
    }   
    $conn->close();
    ?>
</body>

</html>