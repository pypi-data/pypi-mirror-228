-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 19, 2022 at 01:35 PM
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
-- Database: `myfolderstructure`
--

-- --------------------------------------------------------

--
-- Table structure for table `knowntrans`
--

CREATE TABLE `knowntrans` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `value` decimal(10,5) DEFAULT NULL,
  `identification` json DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `knowntrans`
--

INSERT INTO `knowntrans` (`id`, `name`, `value`, `identification`, `category`) VALUES
(1, 'KAUFLAND', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"Kaufland\"}', 'lebensmittel'),
(2, 'REWE', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"REWE\"}', 'lebensmittel'),
(3, 'REAL', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"REAL\"}', 'lebensmittel'),
(4, 'NORMA', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"NORMA\"}', 'lebensmittel'),
(5, 'NETTO', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"NETTO\"}', 'lebensmittel'),
(6, 'LIDL', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"LIDL\"}', 'lebensmittel'),
(7, 'FAMILIENBAECKEREI', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"FAMILIENBAECKEREI\"}', 'lebensmittel'),
(8, 'ROSSMANN', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"ROSSMANN\"}', 'hygiene'),
(9, 'ALDI', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"ALDI\"}', 'lebensmittel'),
(10, 'MUELLER', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"MUELLER\"}', 'hygiene'),
(11, 'APOTHEKE', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"APOTHEKE\"}', 'apotheke'),
(12, 'BAUHAUS', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"BAUHAUS\"}', 'baumaterialien'),
(13, 'XXXL', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"XXXL\"}', 'möbel'),
(14, 'MOEMAX', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"MOEMAX\"}', 'möbel'),
(15, 'IKEA', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"IKEA\"}', 'möbel'),
(16, 'EDEKA', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"EDEKA\"}', 'lebensmittel'),
(17, 'PENNY', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"PENNY\"}', 'lebensmittel'),
(18, 'BAECKEREI', NULL, '{\"Buchungstext\": \"KARTENZAHLUNG\", \"Beguenstigter\": \"BAECKEREI\"}', 'lebensmittel');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `knowntrans`
--
ALTER TABLE `knowntrans`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `knowntrans`
--
ALTER TABLE `knowntrans`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
