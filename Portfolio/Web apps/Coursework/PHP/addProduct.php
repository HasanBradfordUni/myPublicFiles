<?php
// Start the session
session_start();

// Retrieve the product details
$name = $_POST['prodName'];
$image = $_POST['prodImg'];
$cost = $_POST['prodCost'];
$desc = $_POST['prodDesc'];

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
$cost = number_format($cost, 2, ".", "");
$stmt = $conn->prepare("INSERT INTO products (productName, productImgSrc, productDesc, productPrice) VALUES (?, ?, ?, ?)");
$stmt->bind_param("sssd", $name, $image, $desc, $cost);
$stmt->execute();
$conn->close();
// Check if the INSERT was successful
if ($stmt->affected_rows > 0) {
    echo "The product was successfully added.";
    $pagePath = "../HTML/Products/".$name.".html";
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
        $element0->nodeValue = $_SESSION["productID"];
        $element1->nodeValue = $name;
        $element2->nodeValue = $desc;
        $element3->nodeValue = "Product Price: £".$cost;
        $element4->setAttribute('src', '../'.$image);

        // Save the changes to the file
        $doc->saveHTMLFile($pagePath);
    } else {
        echo "Elements not found";
    }
} else {
    echo "Product adding unsuccessful.";
}
exit();
