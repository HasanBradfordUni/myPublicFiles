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
        <h1 class="mainHeading">You are now being registered</h1><br>

        <?php
        // Encrypt the password
        $hashed_password = password_hash($_POST["passwordInput"], PASSWORD_BCRYPT);

        $servername = "localhost";
        $username = "root";
        $password = "";
        $dbname = "smartLife";
        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);
        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        } else {
            echo "<h2 class='subHeading'>Database Connection successfull</h2><br>";
        }
        if (strlen($_POST["username"]) < 4 or strlen($_POST["username"]) > 20) {
            echo "<h3 class='smallHeading'>Username must be at least 4 characters and at most 20 characters</h3><br>";
            echo "<h3 class='subHeading'>You will now be redirected back to the register page</h3><br>";
            // Redirect to the register page after 1.5 seconds using JavaScript
            echo "<script>setTimeout(function(){ window.location.href = '../HTML/register.html'; }, 1500);</script>";
        } elseif (strlen($_POST["passwordInput"]) < 8 or strlen($_POST["passwordInput"]) > 20) {
            echo "<h3 class='smallHeading'>Password must be at least 8 characters and at most 20 characters</h3><br>";
            echo "<h3 class='subHeading'>You will now be redirected back to the register page</h3><br>";
            // Redirect to the register page after 1.5 seconds using JavaScript
            echo "<script>setTimeout(function(){ window.location.href = '../HTML/register.html'; }, 1500);</script>";
        } elseif ($_POST["passwordInput"] != $_POST["passwordConfirmation"]) {
            echo "<h3 class='smallHeading'>Passswords must match!</h3><br>";
            echo "<h3 class='subHeading'>You will now be redirected back to the register page</h3><br>";
            // Redirect to the register page after 1.5 seconds using JavaScript
            echo "<script>setTimeout(function(){ window.location.href = '../HTML/register.html'; }, 1500);</script>";
        } else {
            echo "<h3 class='smallHeading'>Register successfull!</h3><br>";
            echo "<h3 class='subHeading'>You will now be redirected to the login page</h3><br>";
            $stmt = $conn->prepare("INSERT INTO users (Username, Email, UserPassword) VALUES (?, ?, ?)");
            $stmt->bind_param("sss", $_POST["username"], $_POST["emailInput"], $hashed_password);
            $stmt->execute();
            echo "<script>setTimeout(function(){ window.location.href = '../HTML/login.html'; }, 3000);</script>";
            $conn->close();
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