<html>
    <head>
        <meta charset="UTF-8">
        <title>World of Books</title>
        <link rel="stylesheet" href="../CSS/Styles1.css">
        <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    </head>
    <body>
        <?php
            $servername = "localhost";
            $username = "root";
            $password = "";
            $dbname = "myDB";
            // Create connection
            $conn = new mysqli($servername, $username, $password, $dbname);
            // Check connection
            if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            } else {
                echo "<h4>Database connection successfull!</h4><br><hr>";
                echo "<br><h1>The data is as follows: </h1>";
            }
            // Perform the SQL query
            $sql = "SELECT * FROM users";
            $result = $conn->query($sql);
            if ($result->num_rows > 0) {
            // output data of each row
            while($row = $result->fetch_assoc()) {
                echo "<br><h2> Email: " . $row["Email_address"] . " Username: " . $row["Username"] . "</h2>";
                if ($row["Role"] == 1) {
                    echo "<br><h3> User (with username) " . $row["Username"] . " is an admin</h3>";
                } else { 
                    echo "<br><h3> User (with username) " . $row["Username"] . " is not an admin</h3>";
                }
            }
            } else {
                echo "No data.";
            }
            $conn->close();
        ?>
    </body>
</html>