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
        // Start the session
        session_start();

        $servername = "localhost";
        $username = "root";
        $password = "";
        $dbname = "smartlife";
        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);
        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
        $_userValid = "";
        // Perform the SQL query
        $sql = "SELECT * FROM users";
        $result = $conn->query($sql);
        if ($result->num_rows > 0) {
            // output data of each row
            while ($row = $result->fetch_assoc()) {
                if ($_POST['username'] == $row['Username'] and $row["Email"] == $_POST["emailInput"] and password_verify($_POST["passwordInput"], $row["UserPassword"])) {
                    echo "<h2 class='subHeading'>Login successful, you will now be redirected to your account page</h2><br>";
                    // If login is successful
                    $_SESSION['loggedin'] = true;
                    $_SESSION['UserId'] = $row['UserID'];
                    $_SESSION['Username'] = $row['Username'];
                    $_SESSION['Role'] = $row['Role'];
                    $username = $row['Username'] . $row['UserID'];
                    $pagePath = '../Accounts/' . $username . '.php';
                    $hashed_password = password_hash($_POST["passwordInput"], PASSWORD_BCRYPT);
                    try {
                        // Check if the page exists
                        if (file_exists($pagePath)) {
                            // Redirect to the account page after 3 seconds using JavaScript
                            echo "<script>setTimeout(function(){ window.location.href = '../Accounts/$username.php'; }, 3000);</script>";
                        } else {
                            throw new Exception('Page not found');
                        }
                    } catch (Exception $e) {
                        // Get the content of the template file
                        $templateContent = file_get_contents('../Accounts/template.php');
                        // Create the new account page with the template content
                        file_put_contents($pagePath, $templateContent);
                        // Replace placeholders with actual data
                        $pageContent = str_replace(['{{email}}', '{{password}}'], [$_POST["emailInput"], $hashed_password], $templateContent);
                        if ($row['Role'] == 1) {
                            // If Role is 1, replace "My Account" with "My Account (Admin)"
                            $pageContent = str_replace("My Account", "My Account (Admin)", $pageContent);
                        }
                        // Write the content to a new file
                        file_put_contents("../Accounts/$username.php", $pageContent);
                        // Redirect to the account page after 3 seconds using JavaScript
                        echo "<script>setTimeout(function(){ window.location.href = '../Accounts/$username.php'; }, 3000);</script>";
                    }
                    $_userValid = true;
                    break;
                } else {
                    $_userValid = false;
                }
            }
        } else {
            echo "No data.";
            // Redirect to the home page after 3 seconds using JavaScript
            echo "<script>setTimeout(function(){ window.location.href = '../HTML/index.html'; }, 3000);</script>";
        }
        $conn->close();

        if (!$_userValid) {
            echo "<h2 class='subHeading'>Login unsuccessful, user might not exist...</h2><br>";
            // Redirect to the home page after 3 seconds using JavaScript
            echo "<script>setTimeout(function(){ window.location.href = '../HTML/index.html'; }, 3000);</script>";
        }
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