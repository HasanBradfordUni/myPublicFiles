<html>

<head>
    <meta charset="UTF-8">
    <title>Smart Life - Home</title>
    <link rel="stylesheet" href="../CSS/Styles.css">
    <link rel="stylesheet" href="../CSS/homePageStyles.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="../JavaScript/basicJs.js"></script>
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
                <a href="../HTML/login.html"> <img src="../HTML/Images/account.png" class="account"> </a>
            </div>
        </div>
    </header>

    <section class="mainBody">
        <h1 class="mainHeading">You are now being logged in</h1><br>

        <?php
        $servername = "localhost";
        $username = "root";
        $password = "";
        $dbname = "smartlife";
        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);
        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        } else {
            echo "<h5>Database Connection successfull</h5><br>";
        }
        $userExists = false;
        $sql = "SELECT * FROM users";
        $result = $conn->query($sql);
        if ($result->num_rows > 0) {
            // output data of each row
            while ($row = $result->fetch_assoc()) {
                if ($row["Email"] == $_POST["email"] and password_verify($_POST["password"], $row["UserPassword"])) {
                    echo "<h4>Password and email match, updating record...</h4><br>";
                    $userExists = true;
                    $userID = $row["UserID"];
                    $username =$row["Username"];
                }
            }
        } else {
            echo "<h4>Password and email don't match</h4><br>";
            $userExists = false;
        }

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
                $updateSql = "UPDATE users SET Email='$email', UserPassword='$hashed_password' WHERE UserID=$userID";
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
                    $element1->nodeValue = 'Your email: ' . $email;
                    $element2->nodeValue = 'Your hashed password: ' . $hashed_password;

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

    </section>

    <footer>
        <div class="footer">
            <div class="w-container">
                <div class="w-row">
                    <div class="w-col w-col-4">
                        <h3>About</h3>
                        <div></div>
                        <div>Made with Html, Css, JavaScript...</div>
                        <div>...PhP and Sql, etc.</div>
                        <div>Smart Life</div>
                        <div>Your go-to company for IoT devices and solutions</div>
                        <div>Welcome to Smart Life, the forefront of the Internet of Things revolution.</div>
                    </div>
                    <div class="w-col w-col-4">
                        <h3>Useful Links</h3>
                        <div class="footer-link-row">
                            <a href="index.html" target="_blank" class="footer-link">Home</a>
                            <a href="shop.html" target="_blank" class="footer-link">Shop</a>
                        </div>
                        <div class="footer-link-row">
                            <a href="about.html" target="_blank" class="footer-link">About</a>
                            <a href="iotShowroom.html" target="_blank" class="footer-link">IoT Showroom</a>
                        </div>
                        <div class="footer-link-row">
                            <a href="contact.html" target="_blank" class="footer-link">Contact</a>
                            <a href="cart.html" target="_blank" class="footer-link">Cart</a>
                        </div>
                        <div class="footer-link-row">
                            <a href="#" target="_blank" class="footer-link">Account</a>
                            <a href="login.html" target="_blank" class="footer-link">Login</a>
                            <a href="#" target="_blank" class="footer-link">Sign-up</a>
                        </div>
                    </div>
                    <div class="f-col">
                        <h3>Socials</h3>
                        <div>
                            <img src="https://assets-global.website-files.com/5739f5a49fbb0b705633b84e/5739f5a59fbb0b705633b875_social-18.svg" width="20" alt="" class="info-icon">
                            <a href="https://twitter.com/toninif" class="footer-link with-icon">Twitter</a>
                        </div>
                        <div>
                            <img src="https://assets-global.website-files.com/5739f5a49fbb0b705633b84e/5739f5a59fbb0b705633b864_social-03.svg" width="20" alt="" class="info-icon">
                            <a href="https://www.facebook.com/ftonini" class="footer-link with-icon">Facebook</a>
                        </div>
                        <div>
                            <img src="https://assets-global.website-files.com/5739f5a49fbb0b705633b84e/5739f5a59fbb0b705633b86a_social-11.svg" width="20" alt="" class="info-icon">
                            <a href="https://www.pinterest.com/ftonini" class="footer-link with-icon">Pinterest</a>
                        </div>
                        <div>
                            <img src="https://assets-global.website-files.com/5739f5a49fbb0b705633b84e/5739f5a59fbb0b705633b866_social-06.svg" width="20" alt="" class="info-icon">
                            <a href="https://plus.google.com/ftonini" class="footer-link with-icon">Google</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <hr>
        <h1>Copyright Hasan Akhtar 2024</h1>
    </footer>
</body>

</html>