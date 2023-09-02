CREATE TABLE `real_expenses` (
  `id` int NOT NULL,
  `Auftragskonto` varchar(100) DEFAULT NULL,
  `Buchungstag` date DEFAULT NULL,
  `Valutadatum` date DEFAULT NULL,
  `Buchungstext` varchar(100) DEFAULT NULL,
  `Verwendungszweck` varchar(300) DEFAULT NULL,
  `GlaeubigerID` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Mandatsreferenz` varchar(100) DEFAULT NULL,
  `Kundenreferenz` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Sammlerreferenz` varchar(100) DEFAULT NULL,
  `Lastschrift` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Auslagenersatz` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Beguenstigter` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IBAN` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BIC` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Betrag` varchar(50) DEFAULT NULL,
  `Waehrung` varchar(100) DEFAULT NULL,
  `Info` varchar(100) DEFAULT NULL,
  `inptimestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `path2inp` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `real_expenses`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `real_expenses`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;
COMMIT;

