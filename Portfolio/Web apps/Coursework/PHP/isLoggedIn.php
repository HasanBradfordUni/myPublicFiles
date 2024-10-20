<?php
// Start the session
session_start();

// Check if the user is logged in
if(isset($_SESSION['loggedin']) && $_SESSION['loggedin'] == true){
    echo "Welcome, you are logged in!\n";
    echo "../Accounts/".$_SESSION['Username'].$_SESSION['UserId'].".php";
} else {
    echo "Please log in first!\n";
    echo "No account path!";
}

