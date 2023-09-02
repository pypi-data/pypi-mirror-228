-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 31, 2023 at 09:54 AM
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
-- Table structure for table `income_MTU`
--

CREATE TABLE `income_MTU` (
  `id` int NOT NULL,
  `company` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `valid_from` date NOT NULL,
  `valid_to` date DEFAULT NULL,
  `value` decimal(10,5) NOT NULL,
  `pay_day` int DEFAULT NULL,
  `freq` int NOT NULL,
  `myconto` varchar(50) NOT NULL,
  `identification` json DEFAULT NULL,
  `auto_ext` tinyint(1) DEFAULT NULL,
  `post_pay` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `income_MTU`
--

INSERT INTO `income_MTU` (`id`, `company`, `name`, `valid_from`, `valid_to`, `value`, `pay_day`, `freq`, `myconto`, `identification`, `auto_ext`, `post_pay`) VALUES
(1, 'MTU-AeroEngines', 'Salariu', '2019-08-01', NULL, '3780.27000', 30, 1, 'EC', '{\"IBAN\": \"DE48700400410220400600\", \"Buchungstext\": \"LOHN  GEHALT\"}', 1, NULL),
(7, 'MTU-AeroEngines', 'T-Geld', '2022-02-27', NULL, '600.00000', 30, 12, 'EC', '{\"IBAN\": \"DE48700400410220400600\", \"Buchungstext\": \"LOHN  GEHALT\"}', 0, NULL),
(8, 'MTU-AeroEngines', 'ErfolgsBeteiligung', '2022-04-30', NULL, '500.00000', 30, 12, 'EC', '{\"IBAN\": \"DE48700400410220400600\", \"Buchungstext\": \"LOHN  GEHALT\"}', 0, NULL),
(9, 'MTU-AeroEngines', 'UrlaubsGeld', '2019-06-30', NULL, '2000.00000', 30, 12, 'EC', '{\"IBAN\": \"DE48700400410220400600\", \"Buchungstext\": \"LOHN  GEHALT\"}', 1, NULL),
(10, 'MTU-AeroEngines', 'T-Geld B', '2022-07-30', NULL, '300.00000', 30, 12, 'EC', '{\"IBAN\": \"DE48700400410220400600\", \"Buchungstext\": \"LOHN  GEHALT\"}', 1, NULL),
(11, 'MTU-AeroEngines', 'Weinachtsgeld', '2019-11-30', NULL, '1500.00000', 30, 12, 'EC', '{\"IBAN\": \"DE48700400410220400600\", \"Buchungstext\": \"LOHN  GEHALT\"}', 1, NULL),
(12, 'MTU-AeroEngines', 'MitarbeiterAktienProgram', '2022-05-01', NULL, '322.00000', 30, 12, 'EC', '{\"IBAN\": \"DE48700400410220400600\", \"Buchungstext\": \"LOHN  GEHALT\"}', 1, NULL),
(13, 'StadtMünchen', 'KinderGeld', '2022-01-15', '2040-01-15', '219.00000', 15, 1, 'Siri_Radu', NULL, 1, NULL),
(14, 'StadtMünchen', 'FamilienGeld', '2023-01-15', '2023-09-14', '250.00000', 15, 1, 'Siri_Radu', NULL, 1, NULL),
(15, 'MTU-AeroEngines', 'Inflationsausgleichprämie', '2023-01-31', NULL, '1500.00000', 30, 1, 'EC', NULL, NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `income_MTU`
--
ALTER TABLE `income_MTU`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `income_MTU`
--
ALTER TABLE `income_MTU`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
