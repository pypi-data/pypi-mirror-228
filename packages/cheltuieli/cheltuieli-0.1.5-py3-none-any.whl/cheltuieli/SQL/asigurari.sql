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
-- Table structure for table `asigurari`
--

CREATE TABLE `asigurari` (
  `id` int NOT NULL,
  `documente_id` int NOT NULL DEFAULT '3',
  `lastModification` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `company` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `value` decimal(10,5) NOT NULL,
  `pay_day` int DEFAULT NULL,
  `valid_from` date NOT NULL,
  `valid_to` date DEFAULT NULL,
  `freq` int NOT NULL,
  `auto_ext` tinyint(1) DEFAULT NULL,
  `post_pay` tinyint(1) DEFAULT NULL,
  `AsigNo` varchar(50) NOT NULL,
  `myconto` varchar(50) DEFAULT NULL,
  `comments` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `identification` json DEFAULT NULL,
  `path` text CHARACTER SET utf8 COLLATE utf8_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `asigurari`
--

INSERT INTO `asigurari` (`id`, `documente_id`, `lastModification`, `company`, `name`, `value`, `pay_day`, `valid_from`, `valid_to`, `freq`, `auto_ext`, `post_pay`, `AsigNo`, `myconto`, `comments`, `identification`, `path`) VALUES
(2, 3, '2015-03-12 00:00:00', 'Huk-Coburg', 'Auto-Versicherung', '-799.59000', 1, '2021-01-01', '2021-12-31', 12, 0, NULL, '601/947052-J', 'EC', 'Auto: BMW M-RA8612', '{\"IBAN\": \"DE14700500000002034343\", \"Mandatsreferenz\": \"MG025371000\", \"Verwendungszweck\": \"M-RA 8612\"}', '\"D:\\Documente\\Asigurari\\Autoversicherung\\2022-2023\\Rechnung.pdf\"'),
(3, 3, '2021-08-31 15:38:51', 'dieBayerische', 'Zahnzusatz-Versicherung', '-32.60000', 31, '2019-03-01', NULL, 1, 1, NULL, 'S0075374048', 'EC', '', '{\"IBAN\": \"DE30700500000000035273\", \"Mandatsreferenz\": \"S0075374048\"}', 'D:\\Documente\\Asigurari\\Zahnzusatz_Versicherung'),
(4, 3, '2021-10-03 17:26:23', 'ADAC', 'ADAC-Membership', '-94.00000', 1, '2020-11-01', '2021-10-31', 12, 0, NULL, '574088054', 'EC', 'Mitglieds-Nr,: 574088054', '{\"IBAN\": \"DE16700500000006055830\", \"Mandatsreferenz\": \"AD57408805420201106001\"}', '\"D:\\Documente\\Asigurari\\ADAC\\Auto\\ADAC Plus-Mitgliedschaft.pdf\"'),
(5, 3, '2021-10-03 17:26:23', 'ADAC', 'ADAC-Reiserücktritts', '-88.70000', 1, '2021-07-28', '2022-07-27', 12, 0, NULL, '574088054', 'EC', 'Mitglieds-Nr,: 574088054', '{\"IBAN\": \"DE13700500000008055830\", \"Mandatsreferenz\": \"AD5740880542021072700\"}', '\"D:\\Documente\\Asigurari\\ADAC\\Reiseversicherung\\reisevers.pdf\"'),
(6, 3, '2021-10-03 17:26:23', 'VersicherungsKammerBayern', 'RisikoLebenVersicherung', '-19.31000', 31, '2018-09-01', NULL, 1, 1, NULL, 'LV-0001 -0670-5101', 'EC', '', '{\"IBAN\": \"DE47700500000003024022\", \"Mandatsreferenz\": \"LV000106705101\"}', 'D:\\Documente\\Asigurari\\Lebens_versicherung_BAYERN'),
(7, 3, '2021-10-03 17:26:23', 'Huk-Coburg', 'Privathaftpflichtversicherung', '-77.00000', 1, '2020-11-20', '2021-11-19', 12, 0, NULL, '701/259223-A-14', 'Siri&Radu', '', '{\"IBAN\": \"DE14700500000002034343\", \"Mandatsreferenz\": \"MM035374679\"}', '\"D:\\Documente\\Asigurari\\Privathaftpflichtversicherung_Huk-Coburg\\Familie\\IMG_20201022_0004.pdf\"'),
(8, 3, '2021-10-03 20:07:35', 'VersicherungsKammerBayern', 'Rechtsschutzversicherung', '-277.20000', 1, '2020-07-16', '2023-07-16', 12, 1, NULL, '840-4563636', 'Siri&Radu', '', '{\"IBAN\": \"DE49700500000000032700\", \"Mandatsreferenz\": \"840-4563636-S-1\"}', '\"D:\\Documente\\Asigurari\\Rechtsschutz_Versicherung_Huk-Coburg\\KammerBayern\\IMG_20200724_0002.pdf\"'),
(9, 3, '2021-10-03 20:09:59', 'Huk-Coburg', 'Unfallversicherung', '-82.01000', 1, '2020-12-23', '2021-12-22', 12, 0, NULL, '701/259223-A-15', 'EC', '', '{\"IBAN\": \"DE14700500000002034343\", \"Mandatsreferenz\": \"MP038158605\"}', '\"D:\\Documente\\Asigurari\\Unfallversicherung_Huk-Coburg\\IMG_20201110_0002.pdf\"'),
(10, 3, '2021-10-03 20:09:59', 'Huk-Coburg', 'Hausratversicherung', '-45.05000', 1, '2020-11-06', '2021-11-05', 12, 0, NULL, '701/259223-A-16', 'Siri&Radu', '', '{\"IBAN\": \"DE14700500000002034343\", \"Mandatsreferenz\": \"MU040309174\"}', '\"D:\\Documente\\Asigurari\\HausRatVersicherung\\IMG_20201110_0007.pdf\"'),
(15, 3, '2021-10-03 17:26:23', 'ADAC', 'ADAC-Membership', '-94.00000', 1, '2021-11-01', '2022-10-31', 12, 1, NULL, '574088054', 'DeutscheBank', 'Mitglieds-Nr,: 574088054', '{\"IBAN\": \"DE16700500000006055830\", \"Mandatsreferenz\": \"AD57408805420201106001\"}', '\"D:\\Documente\\Asigurari\\ADAC\\Auto\\ADAC_membership2021-2022.pdf\"'),
(16, 3, '2015-03-12 00:00:00', 'Huk-Coburg', 'Auto-Versicherung', '-660.60000', 1, '2022-01-01', '2022-12-31', 12, 1, NULL, '601/947052-J', 'DeutscheBank', 'Auto: BMW M-RA8612', '{\"IBAN\": \"DE14700500000002034343\", \"Mandatsreferenz\": \"MG025371000\", \"Verwendungszweck\": \"M-RA 8612\"}', '\"D:\\Documente\\Asigurari\\Autoversicherung\\2022-2023\\Rechnung.pdf\"'),
(17, 3, '2021-10-03 17:26:23', 'ADAC', 'ADAC-Reiserücktritts', '-88.70000', 1, '2022-07-28', NULL, 12, 1, NULL, '574088054', 'Siri&Radu', 'Mitglieds-Nr,: 574088054', '{\"IBAN\": \"DE13700500000008055830\", \"Mandatsreferenz\": \"AD5740880542021072700\"}', NULL),
(18, 3, '2021-10-03 20:09:59', 'Huk-Coburg', 'Unfallversicherung', '-84.96000', 1, '2021-12-23', '2022-12-22', 12, 1, NULL, '701/259223-A-15', 'DeutscheBank', '', '{\"IBAN\": \"DE14700500000002034343\", \"Mandatsreferenz\": \"MP038158605\"}', '\"D:\\Documente\\Asigurari\\Unfallversicherung_Huk-Coburg\\2021-2022Unfalvers.pdf\"'),
(21, 3, '2021-10-03 20:09:59', 'Huk-Coburg', 'Hausratversicherung', '-45.05000', 1, '2021-11-06', '2022-11-05', 12, 1, NULL, '701/259223-A-16', 'Siri&Radu', '', '{\"IBAN\": \"DE14700500000002034343\", \"Mandatsreferenz\": \"MU040309174\"}', 'D:/Documente/Asigurari/HausRatVersicherung/HausRatVersicherung.pdf'),
(23, 3, '2021-10-03 17:26:23', 'Huk-Coburg', 'Privathaftpflichtversicherung', '-77.00000', 1, '2021-11-20', '2022-11-19', 12, 1, NULL, '701/259223-A-14', 'Siri&Radu', '', '{\"IBAN\": \"DE14700500000002034343\", \"Mandatsreferenz\": \"MM035374679\"}', 'D:/Documente/Asigurari/Privathaftpflichtversicherung_Huk-Coburg/Familie/2021-2022HaftpflichtVers.pdf');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `asigurari`
--
ALTER TABLE `asigurari`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `asigurari`
--
ALTER TABLE `asigurari`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Constraints for dumped tables
--


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
