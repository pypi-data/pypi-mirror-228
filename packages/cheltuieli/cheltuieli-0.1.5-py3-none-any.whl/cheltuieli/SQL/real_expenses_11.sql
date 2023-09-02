-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 10, 2021 at 02:38 PM
-- Server version: 8.0.22
-- PHP Version: 8.0.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cheltuieli`
--

-- --------------------------------------------------------

--
-- Table structure for table `test_real_expenses`
--

CREATE TABLE `test_real_expenses` (
  `id` int NOT NULL,
  `Auftragskonto` varchar(100) DEFAULT NULL,
  `Buchungstag` date DEFAULT NULL,
  `Valutadatum` date DEFAULT NULL,
  `Buchungstext` varchar(100) DEFAULT NULL,
  `Verwendungszweck` varchar(300) DEFAULT NULL,
  `Glaeubiger` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Mandatsreferenz` varchar(100) DEFAULT NULL,
  `Kundenreferenz` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Sammlerreferenz` varchar(100) DEFAULT NULL,
  `Lastschrift` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Auslagenersatz` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Beguenstigter` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IBAN` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BIC` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Betrag` decimal(10,5) DEFAULT NULL,
  `Waehrung` varchar(100) DEFAULT NULL,
  `Info` varchar(100) DEFAULT NULL,
  `table_name` varchar(50) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `value` decimal(10,5) DEFAULT NULL,
  `inptimestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `path2inp` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


--
-- Indexes for dumped tables
--

--
-- Indexes for table `test_real_expenses`
--
ALTER TABLE `test_real_expenses`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `test_real_expenses`
--
ALTER TABLE `test_real_expenses`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1253;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
