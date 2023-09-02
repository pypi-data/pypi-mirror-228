-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 19, 2022 at 01:34 PM
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
-- Table structure for table `apartament`
--

CREATE TABLE `apartament` (
  `id` int NOT NULL,
  `documente_id` int NOT NULL DEFAULT '2',
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `contract_number` varchar(50) DEFAULT NULL,
  `valid_from` date NOT NULL,
  `valid_to` date DEFAULT NULL,
  `value` decimal(10,5) DEFAULT NULL,
  `pay_day` int DEFAULT NULL,
  `freq` int DEFAULT NULL,
  `auto_ext` tinyint(1) DEFAULT NULL,
  `post_pay` tinyint(1) DEFAULT NULL,
  `myconto` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `identification` json DEFAULT NULL,
  `path` text CHARACTER SET utf8 COLLATE utf8_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `apartament`
--

INSERT INTO `apartament` (`id`, `documente_id`, `name`, `contract_number`, `valid_from`, `valid_to`, `value`, `pay_day`, `freq`, `auto_ext`, `post_pay`, `myconto`, `identification`, `path`) VALUES
(1, 2, 'ARD-ZDF', '473 841 212', '2019-05-15', NULL, '-52.50000', 15, 3, 1, NULL, 'Siri&Radu', '{\"IBAN\": \"DE28700500000002024100\", \"Mandatsreferenz\": \"4738412121501\"}', '\"D:\\Documente\\Apartament\\ARD-ZDF\"'),
(2, 2, 'PYUR', '8446757', '2017-11-08', '2022-02-28', '-28.00000', 31, 1, 1, NULL, 'Siri&Radu', '{\"IBAN\": \"DE58100100100918984104\", \"Mandatsreferenz\": \"MC08446757-001\"}', '\"D:\\Documente\\Apartament\\Internet_TV\\PYUR\"'),
(3, 2, 'SWK', '21344633', '2020-11-02', '2021-07-25', '-73.00000', 15, 1, 0, NULL, 'Siri&Radu', '{\"IBAN\": \"DE91320500000000301341\", \"Mandatsreferenz\": \"L759938-101\"}', '\"D:\\Documente\\Apartament\\Strom\\SWK\"'),
(4, 2, 'SWK', '21344633', '2021-07-25', NULL, '-49.00000', 15, 1, 1, NULL, 'Siri&Radu', '{\"IBAN\": \"DE91320500000000301341\", \"Mandatsreferenz\": \"L759938-102\"}', '\"D:\\Documente\\Apartament\\Strom\\SWK\"'),
(5, 2, 'Chiria_Königteinstr1', NULL, '2020-10-01', NULL, '-1110.00000', 30, 1, 1, NULL, 'Siri&Radu', '{\"IBAN\": \"DE38700202706060775476\", \"Verwendungszweck\": \"Miete für die Wohnung\"}', '\"D:\\Documente\\Apartament\\München Königsteinstraße\\Draft-MV Lazaryan-Radu.pdf\"'),
(6, 2, 'Chiria_Garaj', NULL, '2020-10-01', '2022-04-30', '-90.00000', 30, 1, 0, NULL, 'Siri&Radu', '{\"IBAN\": \"DE78700800000463427500\"}', '\"D:\\Documente\\Apartament\\München Königsteinstraße\"'),
(7, 2, 'Chiria_DachauerStr', NULL, '2017-11-01', '2020-11-15', '-992.00000', 30, 1, 0, NULL, 'EC', '{\"IBAN\": \"DE36701500001001399391\"}', 'D:/Documente/Apartament/München Dachauerstr 175A/Vertrag.pdf'),
(8, 2, 'Miete Garage 4', NULL, '2022-05-31', NULL, '-45.00000', 31, 1, 1, NULL, 'Siri&Radu', '{\"IBAN\": \"DE56701500001006445553\"}', NULL),
(9, 2, 'Chiria_Garaj', NULL, '2022-05-01', NULL, '-80.00000', 30, 1, 1, NULL, 'Siri&Radu', '{\"IBAN\": \"DE38700202706060775476\", \"Verwendungszweck\": \"Tiefgaragenstellplatz\"}', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `apartament`
--
ALTER TABLE `apartament`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `apartament`
--
ALTER TABLE `apartament`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
