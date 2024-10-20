<?php
// Start the session
session_start();

// ... (code for logout)

// If logout is successful
unset($_SESSION['loggedin']);

