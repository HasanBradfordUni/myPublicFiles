-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 30, 2024 at 02:14 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smartlife`
--

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `productID` int(5) NOT NULL,
  `productName` varchar(50) NOT NULL,
  `productImgSrc` varchar(100) DEFAULT NULL,
  `productDesc` text DEFAULT NULL,
  `productPrice` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`productID`, `productName`, `productImgSrc`, `productDesc`, `productPrice`) VALUES
(1, 'Smart Life Basic Smart Watch', '../HTML/Images/basicSmartWatch1.avif', 'A basic, cheap and reliable smart watch that can connect to a smart phone via bluetooth and has a range of digital features', 23.99),
(2, 'Advanced Smart Fridge', '', '', 115.99),
(3, 'Smart Life Intermediate Smart Thermostat', '', 'A smart thermostat manufactured and sold only by Smart Life', 99.54),
(4, 'UberX self-driving car', '', 'A self-driving car manufactured and advertised by UberX', 20346.99);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `UserID` int(4) NOT NULL,
  `Username` varchar(20) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Role` tinyint(1) NOT NULL DEFAULT 0,
  `UserPassword` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`UserID`, `Username`, `Email`, `Role`, `UserPassword`) VALUES
(1, 'H.Akhtar', 'akhtarhasan2005@gmail.com', 0, '$2y$10$5lphMqsqYQMeO5U743zcPe8z8ql6pxlykArmlgNrLNTD7Fb1Zextu'),
(2, 'Hakhta26', 'hakhta26@bradford.ac.uk', 1, '$2y$10$dnzJwDYNhCJAABopfq3Lp.XdRE/B1v2EmpjIxOKkPZMDfwBMeZwsi'),
(4, 'Haziz', 'haziz@bradford.ac.uk', 1, '$2y$10$srqfVo37JypaCa.nyQrGcueVrHe6bz2ag.azvATHTM1Jn1wbN0xm2'),
(5, '', '', 1, '$2y$10$toIsyXIFN103.2OvkthttODzIka40/1xCxiTeMv7DNGzAxjxl3xpS'),
(6, 'YusufQ', 'quraishiYusuf@gmail.com', 0, '$2y$10$5pyvQ9O6g36D4y6m93YZ8u20TjoNag/fi1svuszFkkTLgKqdL9qPm');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`productID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`UserID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `productID` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `UserID` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
