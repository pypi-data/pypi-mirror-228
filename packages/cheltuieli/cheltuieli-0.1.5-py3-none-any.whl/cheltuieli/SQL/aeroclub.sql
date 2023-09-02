-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 19, 2022 at 01:33 PM
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
-- Table structure for table `aeroclub`
--

CREATE TABLE `aeroclub` (
  `id` int NOT NULL,
  `documente_id` int NOT NULL DEFAULT '1',
  `name` varchar(50) NOT NULL,
  `number` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `valid_from` date NOT NULL,
  `valid_to` date DEFAULT NULL,
  `country` varchar(15) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `value` decimal(10,5) DEFAULT NULL,
  `pay_day` int DEFAULT NULL,
  `freq` int DEFAULT NULL,
  `auto_ext` tinyint(1) DEFAULT NULL,
  `post_pay` tinyint(1) DEFAULT NULL,
  `myconto` varchar(50) NOT NULL,
  `identification` json DEFAULT NULL,
  `path` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `aeroclub`
--

INSERT INTO `aeroclub` (`id`, `documente_id`, `name`, `number`, `valid_from`, `valid_to`, `country`, `value`, `pay_day`, `freq`, `auto_ext`, `post_pay`, `myconto`, `identification`, `path`) VALUES
(1, 1, 'License ULM', '41570/18', '2018-03-19', NULL, 'DE', NULL, NULL, NULL, NULL, NULL, '', NULL, '\"D:\\Documente\\Aeroclub\\License\\Luftfahrerschein für Luftsportgeräteführer.pdf\"'),
(2, 1, 'License SPL', 'SPL-866', '2009-02-04', '2011-11-07', 'RO', NULL, NULL, NULL, NULL, NULL, '', NULL, '\"D:\\Documente\\Aeroclub\\License\\SPL 07.11.2011.pdf\"'),
(3, 1, 'License ULM', '0464', '2010-03-24', '2011-09-28', 'RO', NULL, NULL, 24, NULL, NULL, '', NULL, '\"D:\\Documente\\Aeroclub\\License\\ULM 28.09.2011.pdf\"'),
(4, 1, 'License ULM', '0464', '2015-09-15', '2017-09-09', 'RO', NULL, NULL, 24, NULL, NULL, '', NULL, '\"D:\\Documente\\Aeroclub\\License\\ULM 09.09.2017.pdf\"'),
(5, 1, 'License ULM', '0464', '2017-08-09', '2019-08-02', 'RO', NULL, NULL, 24, NULL, NULL, '', NULL, '\"D:\\Documente\\Aeroclub\\License\\ULM 02.08.2019.pdf\"'),
(6, 1, 'License ULM', '0464', '2019-08-06', '2021-07-12', 'RO', NULL, NULL, 24, 0, NULL, '', NULL, '\"D:\\Documente\\Aeroclub\\License\\ULM 12.07.2021.pdf\"'),
(7, 1, 'BZF I', '19/496507-B1', '2021-04-21', NULL, 'DE', NULL, NULL, NULL, NULL, NULL, '', NULL, '\"D:\\Documente\\Aeroclub\\License\\BZF1.pdf\"'),
(8, 1, 'Medical', NULL, '2013-09-30', '2018-09-30', 'RO', NULL, NULL, NULL, NULL, NULL, '', NULL, '\"D:\\Documente\\Aeroclub\\Medical\\Medical Certificate 30.09.2018.pdf\"'),
(9, 1, 'Medical', 'DE 1178704-2', '2018-09-25', '2023-09-30', 'DE', NULL, NULL, NULL, NULL, NULL, '', NULL, '\"D:\\Documente\\Aeroclub\\Medical\\Medical Certificate 30.09.2023.pdf\"'),
(10, 1, 'Radio', '10008', '2013-10-30', '2018-10-15', 'RO', NULL, NULL, NULL, NULL, NULL, '', NULL, '\"D:\\Documente\\Aeroclub\\Radio\\Radio 15.10.2018.pdf\"'),
(11, 1, 'Radio', '23786', '2018-10-10', '2023-10-10', 'RO', NULL, NULL, NULL, NULL, NULL, '', NULL, '\"D:\\Documente\\Aeroclub\\Radio\\Radio 10.10.2023.pdf\"'),
(12, 1, 'Mitgliedsgebuhr', NULL, '2018-02-22', '2021-08-17', 'DE', '-439.30000', 1, 12, 0, NULL, 'EC', '{\"IBAN\": \"DE58711500000000292391\", \"Mandatsreferenz\": \"2018-38\", \"Verwendungszweck\": \"Mitgliedsgebuhr\"}', '\"D:\\Documente\\Aeroclub\\Bad_Endorf\\Rechnung_20210097.pdf\"'),
(13, 1, 'Fluggebuehren', NULL, '2021-08-18', '2021-08-17', 'DE', '-232.33000', 1, 3, 0, NULL, 'EC', '{\"IBAN\": \"DE58711500000000292391\", \"Mandatsreferenz\": \"2018-38\", \"Verwendungszweck\": \"Fluggebuehren\"}', '\"D:\\Documente\\Aeroclub\\Bad_Endorf\\Rechnung_20210173.pdf\"'),
(14, 1, 'BadEndorf Quartalabrechnung_Q3', NULL, '2021-07-01', '2021-09-30', 'DE', '-185.58000', 1, 12, 0, NULL, 'DeutscheBank', '{\"IBAN\": \"DE58711500000000292391\", \"Mandatsreferenz\": \"2018-38\", \"Verwendungszweck\": \"Fluggebuehren\"}', '\"D:\\Documente\\Aeroclub\\Bad_Endorf\\Rechnung_20210173.pdf\"'),
(16, 1, 'BadEndorf Jahresbeitrag', NULL, '2021-02-22', '2021-02-21', 'DE', '-439.30000', 1, 12, 1, NULL, 'DeutscheBank', '{\"IBAN\": \"DE58711500000000292391\", \"Mandatsreferenz\": \"2018-38\", \"Verwendungszweck\": \"Mitgliedsgebuhr\"}', '\"D:\\Documente\\Aeroclub\\Bad_Endorf\\Rechnung_20210097.pdf\"'),
(18, 1, 'License ULM', '0464', '2021-07-13', '2023-07-08', 'RO', NULL, NULL, 24, 0, NULL, '', NULL, 'D:\\Documente\\Aeroclub\\License\\ULM 08.07.2023.pdf'),
(19, 1, 'BadEndorf Quartalabrechnung_Q2', NULL, '2021-04-01', '2021-06-30', 'DE', '-232.33000', 1, 12, 0, NULL, 'EC', '{\"IBAN\": \"DE58711500000000292391\", \"Mandatsreferenz\": \"2018-38\", \"Verwendungszweck\": \"Fluggebuehren\"}', '\"D:\\Documente\\Aeroclub\\Bad_Endorf\\Rechnung_20210173.pdf\"'),
(20, 1, 'BadEndorf Quartalabrechnung_Q4', NULL, '2021-10-01', '2021-12-31', 'DE', '-110.50000', 1, 12, 0, 1, 'DeutscheBank', '{\"IBAN\": \"DE58711500000000292391\", \"Mandatsreferenz\": \"2018-38\", \"Verwendungszweck\": \"Fluggebuehren\"}', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `aeroclub`
--
ALTER TABLE `aeroclub`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `aeroclub`
--
ALTER TABLE `aeroclub`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- Constraints for dumped tables
--


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
