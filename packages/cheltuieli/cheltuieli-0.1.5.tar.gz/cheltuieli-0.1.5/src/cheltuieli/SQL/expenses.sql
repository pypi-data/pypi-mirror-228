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
-- Table structure for table `expenses`
--

CREATE TABLE `expenses` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `valid_from` date NOT NULL,
  `valid_to` date DEFAULT NULL,
  `freq` int NOT NULL,
  `auto_ext` tinyint(1) DEFAULT NULL,
  `post_pay` tinyint(1) DEFAULT NULL,
  `value` decimal(10,5) NOT NULL,
  `pay_day` int DEFAULT NULL,
  `myconto` varchar(50) NOT NULL,
  `IBAN` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `identification` json DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `expenses`
--

INSERT INTO `expenses` (`id`, `name`, `valid_from`, `valid_to`, `freq`, `auto_ext`, `post_pay`, `value`, `pay_day`, `myconto`, `IBAN`, `identification`) VALUES
(2, 'MasterCard', '2020-10-05', NULL, 1, 1, NULL, '-8.00000', 4, 'EC', 'DE61701500009900294274', '{\"IBAN\": \"DE61701500009900294274\"}'),
(3, 'Mancare munca', '2020-10-15', NULL, 3, 1, NULL, '-50.00000', 15, 'EC', 'DE59700202706130340006', '{\"IBAN\": \"DE59700202706130340006\"}'),
(5, 'CartelaPrepaid', '2020-10-15', NULL, 2, 1, NULL, '-15.00000', 15, 'EC', 'DE02250500009010470514', '{\"IBAN\": \"DE02250500009010470514\"}'),
(6, 'Siri&Radu_ENTGELTABSCHLUSS', '2021-01-30', NULL, 1, 1, NULL, '-5.24000', 31, 'Siri&Radu', NULL, '{\"IBAN\": \"0000000000\", \"Buchungstext\": \"ENTGELTABSCHLUSS\", \"Auftragskonto\": \"DE25701500001006057044\"}'),
(7, 'EC_ENTGELTABSCHLUSS', '2021-01-30', NULL, 1, 1, NULL, '-2.25000', 31, 'EC', NULL, '{\"IBAN\": \"0000000000\", \"Buchungstext\": \"ENTGELTABSCHLUSS\", \"Auftragskonto\": \"DE76701500001005090491\"}'),
(8, 'ExtraCredit', '2021-01-30', NULL, 1, 1, NULL, '-600.00000', 5, 'EC', 'DE27701500006001569521', '{\"IBAN\": \"DE27701500006001569521\", \"Buchungstext\": \"ONLINE-UEBERWEISUNG\"}'),
(9, 'cash', '2021-01-30', NULL, 1, NULL, NULL, '0.00000', NULL, 'EC', NULL, '{\"IBAN\": \"0000000000\", \"Buchungstext\": \"BARGELDAUSZAHLUNG\", \"Auftragskonto\": \"DE76701500001005090491\"}'),
(10, 'Credit', '2021-01-30', NULL, 1, 1, NULL, '-532.00000', 30, 'EC', 'DE27701500006001569521', '{\"IBAN\": \"DE27701500006001569521\", \"Buchungstext\": \"EINZUG RATE/ANNUITAET\"}'),
(11, 'CreditMasina', '2022-02-01', NULL, 1, 1, NULL, '-138.60000', 1, 'EC', '', '{\"IBAN\": \"DE27701500006001569521\"}');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `expenses`
--
ALTER TABLE `expenses`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `expenses`
--
ALTER TABLE `expenses`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
