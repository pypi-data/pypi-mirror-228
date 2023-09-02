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
-- Table structure for table `munca`
--

CREATE TABLE `munca` (
  `id` int NOT NULL,
  `documente_id` int NOT NULL DEFAULT '6',
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
-- Dumping data for table `munca`
--

INSERT INTO `munca` (`id`, `documente_id`, `company`, `name`, `valid_from`, `valid_to`, `value`, `pay_day`, `freq`, `myconto`, `identification`, `auto_ext`, `post_pay`) VALUES
(1, 6, 'MTU-AeroEngines', 'Salariu', '2019-08-01', NULL, '3318.00000', 30, 1, 'EC', '{\"IBAN\": \"DE48700400410220400600\", \"Buchungstext\": \"LOHN  GEHALT\"}', 1, NULL),
(7, 6, 'MTU-AeroEngines', 'T-Geld', '2022-02-27', NULL, '600.00000', 30, 12, 'EC', '{\"IBAN\": \"DE48700400410220400600\", \"Buchungstext\": \"LOHN  GEHALT\"}', 0, NULL),
(8, 6, 'MTU-AeroEngines', 'ErfolgsBeteiligung', '2022-04-30', NULL, '500.00000', 30, 12, 'EC', '{\"IBAN\": \"DE48700400410220400600\", \"Buchungstext\": \"LOHN  GEHALT\"}', 0, NULL),
(9, 6, 'MTU-AeroEngines', 'UrlaubsGeld', '2019-04-30', NULL, '2000.00000', 30, 12, 'EC', '{\"IBAN\": \"DE48700400410220400600\", \"Buchungstext\": \"LOHN  GEHALT\"}', 1, NULL),
(10, 6, 'MTU-AeroEngines', 'T-Geld B', '2022-07-30', NULL, '300.00000', 30, 12, 'EC', '{\"IBAN\": \"DE48700400410220400600\", \"Buchungstext\": \"LOHN  GEHALT\"}', 1, NULL),
(11, 6, 'MTU-AeroEngines', 'Weinachtsgeld', '2019-11-30', NULL, '1500.00000', 30, 12, 'EC', '{\"IBAN\": \"DE48700400410220400600\", \"Buchungstext\": \"LOHN  GEHALT\"}', 1, NULL),
(12, 6, 'MTU-AeroEngines', 'MitarbeiterAktienProgram', '2022-05-01', NULL, '322.00000', 30, 12, 'EC', '{\"IBAN\": \"DE48700400410220400600\", \"Buchungstext\": \"LOHN  GEHALT\"}', 1, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `munca`
--
ALTER TABLE `munca`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `munca`
--
ALTER TABLE `munca`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
