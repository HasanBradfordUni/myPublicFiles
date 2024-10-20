-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 03, 2024 at 10:06 AM
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
-- Table structure for table `cart_products`
--

CREATE TABLE `cart_products` (
  `userId` int(4) NOT NULL,
  `productId` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `cart_products`
--

INSERT INTO `cart_products` (`userId`, `productId`) VALUES
(1, 2),
(1, 5),
(1, 6),
(2, 1),
(6, 1),
(6, 2),
(6, 3),
(7, 5),
(7, 6);

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
(2, 'Advanced Smart Fridge', '../HTML/Images/smartFridge1.png', '', 115.99),
(3, 'Smart Life Intermediate Smart Thermostat', '../HTML/Images/thermostat1.jpg', 'A smart thermostat manufactured and sold only by Smart Life', 99.54),
(4, 'UberX self-driving car', '../HTML/Images/smartCar1.webp', 'A self-driving car manufactured and advertised by UberX', 20346.99),
(5, 'EGL 32E23HDS1 32 Inch HDR LED Smart TV', '../HTML/Images/smartTV1.webp', 'Enjoy crisp, vibrant HD displays with the new 2022 EGL TV range. Watch all your favourite apps easily with our Smart features. whether youâ€™re watching the big game, entertaining the kids or playing your favourite gaming console, this TV is perfect for all the family.', 99.99),
(6, 'Samsung Add-wash Smart Washing Machine', '../HTML/Images/washingMachine1.jpeg', 'A smart washing machine manufactured by Samsung that you can pair with your phone.', 125.99),
(7, 'Smart Life Smart Sofa', '', 'A smart sofa...', 104.99);

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
(6, 'YusufQ', 'quraishiYusuf@gmail.com', 0, '$2y$10$5pyvQ9O6g36D4y6m93YZ8u20TjoNag/fi1svuszFkkTLgKqdL9qPm'),
(7, 'DaveJK', 'davejk@gmail.com', 1, '$2y$10$Y0WA.qk5qT/F5AR5eWsBr.BkaLUVM84VIiGz4SRAhdlC2pC702xF.'),
(8, 'helloDave', 'helloDave@gmail.com', 0, '$2y$10$jbvxX6yr2kfoR2JRrrH3aO/R52.5YZXdrkVYOwUi29KdztXSR8sHO');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart_products`
--
ALTER TABLE `cart_products`
  ADD PRIMARY KEY (`userId`,`productId`),
  ADD KEY `productId` (`productId`);

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
  MODIFY `productID` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `UserID` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart_products`
--
ALTER TABLE `cart_products`
  ADD CONSTRAINT `cart_products_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`UserID`),
  ADD CONSTRAINT `cart_products_ibfk_2` FOREIGN KEY (`productId`) REFERENCES `products` (`productID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
