<html>

<head>
    <meta charset="UTF-8">
    <title>Smart Life</title>
    <link rel="stylesheet" href="../CSS/Styles.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="../JavaScript/basicJs.js"></script>
</head>

<body>
    <?php
    // Start the session
    session_start();

    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "smartLife";
    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    // Perform the SQL query
    $lastProductID = 1;
    $sql = "SELECT * FROM products";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        // output data of each row
        while ($row = $result->fetch_assoc()) {
            echo $row["productID"] . ";" . $row["productName"] . ";" . $row["productDesc"] . ";" . $row["productPrice"] . ";" . $row["productImgSrc"] . "\n";
            $pagePath = "../HTML/Products/" . $row["productName"] . ".html";
            try {
                // Check if the page exists
                if (file_exists($pagePath)) {
                    $string = "";
                } else {
                    throw new Exception('Page not found');
                }
            } catch (Exception $e) {
                // Get the content of the template file
                $templateContent = file_get_contents('../HTML/Products/template.html');
                // Create the new product page with the template content
                file_put_contents($pagePath, $templateContent);
                $doc = new DOMDocument();
                libxml_use_internal_errors(true); // Disable libxml errors
                $doc->loadHTMLFile($pagePath);

                // Get the elements by ids
                $element0 = $doc->getElementById('productID');
                $element1 = $doc->getElementById('prodTitle');
                $element2 = $doc->getElementById('productDesc');
                $element3 = $doc->getElementById('productPrice');
                $element4 = $doc->getElementById('productImage');

                // Check if the element was found
                if ($element1 and $element2 and $element3 and $element4) {
                    // Change the content of the elements
                    $element0->nodeValue = $row["productID"];
                    $element1->nodeValue = $row["productName"];
                    $element2->nodeValue = $row["productDesc"];
                    $element3->nodeValue = "Product Price: £" .  $row["productPrice"];
                    $element4->setAttribute('src', '../' . $row["productImgSrc"]);

                    // Save the changes to the file
                    $doc->saveHTMLFile($pagePath);
                } else {
                    $string = "Elements not found";
                }
            }
            $lastProductID = $row["productID"];
        }
    } else {
        echo "No data.";
    }
    $_SESSION["productID"] = $lastProductID;
    $conn->close();

    // Redirect to the shop page after 3 seconds using JavaScript
    echo "<script>setTimeout(function(){ window.location.href = '../HTML/shop.html'; }, 3000);</script>";
    ?>
</body>

</html>