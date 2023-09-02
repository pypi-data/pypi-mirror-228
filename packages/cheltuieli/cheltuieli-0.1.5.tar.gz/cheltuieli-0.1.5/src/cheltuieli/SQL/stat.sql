-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 19, 2022 at 01:36 PM
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
-- Table structure for table `stat`
--

CREATE TABLE `stat` (
  `id` int NOT NULL,
  `documente_id` int NOT NULL DEFAULT '8',
  `name` varchar(50) NOT NULL,
  `valid_from` date NOT NULL,
  `valid_to` date DEFAULT NULL,
  `value` decimal(10,5) DEFAULT NULL,
  `pay_day` int DEFAULT NULL,
  `freq` int DEFAULT NULL,
  `myconto` varchar(50) DEFAULT NULL,
  `auto_ext` tinyint(1) DEFAULT NULL,
  `post_pay` tinyint(1) DEFAULT NULL,
  `path` text NOT NULL,
  `identification` json DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `stat`
--

INSERT INTO `stat` (`id`, `documente_id`, `name`, `valid_from`, `valid_to`, `value`, `pay_day`, `freq`, `myconto`, `auto_ext`, `post_pay`, `path`, `identification`) VALUES
(1, 8, 'Steuererklärung_2018', '2018-01-01', '2018-12-30', '312.00000', NULL, 12, 'EC', 0, NULL, 'D:\\Documente\\Stat\\Steuererklärung\\2018', NULL),
(2, 8, 'Steuererklärung_2019', '2019-01-01', '2019-12-30', '428.00000', NULL, 12, 'EC', 0, NULL, 'D:\\Documente\\Stat\\Steuererklärung\\2019', NULL),
(3, 8, 'Steuererklärung_2020', '2020-01-01', '2021-12-30', '-62.35000', NULL, 12, 'EC', 0, NULL, 'D:\\Documente\\Stat\\Steuererklärung\\2020', NULL),
(4, 8, 'LOHNSTEUERHILFE BAY.', '2021-01-01', '2021-12-31', '-242.00000', 1, 12, 'EC', 0, NULL, '', '{\"IBAN\": \"DE43700202700654745099\", \"Mandatsreferenz\": \"162021153\"}'),
(6, 8, 'Kfz-Steuer fuer M RA 8612', '2015-08-30', NULL, '-92.00000', 1, 12, 'EC', 1, NULL, '', '{\"IBAN\": \"DE78750000000075001008\", \"Mandatsreferenz\": \"KFZFK1163682580903092018\"}'),
(7, 8, 'LOHNSTEUERHILFE BAY.', '2022-01-01', '2022-12-31', '-242.00000', 1, 12, 'DeutscheBank', 1, NULL, '', '{\"IBAN\": \"DE43700202700654745099\", \"Mandatsreferenz\": \"162021153\"}');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `stat`
--
ALTER TABLE `stat`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `stat`
--
ALTER TABLE `stat`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
