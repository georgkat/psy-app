/*!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.4.2-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: testdb
-- ------------------------------------------------------
-- Server version	11.4.2-MariaDB-ubu2404

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `carddata`
--

DROP TABLE IF EXISTS `carddata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `carddata` (
  `user_id` int(11) NOT NULL,
  `number` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `date` varchar(45) DEFAULT NULL,
  `ccv` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  CONSTRAINT `id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carddata`
--

LOCK TABLES `carddata` WRITE;
/*!40000 ALTER TABLE `carddata` DISABLE KEYS */;
/*!40000 ALTER TABLE `carddata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cards`
--

DROP TABLE IF EXISTS `cards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cards` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `number` varchar(45) NOT NULL,
  `name` varchar(45) NOT NULL,
  `ccv` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `number_UNIQUE` (`number`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `_idx` (`user_id`),
  CONSTRAINT `cards_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cards`
--

LOCK TABLES `cards` WRITE;
/*!40000 ALTER TABLE `cards` DISABLE KEYS */;
/*!40000 ALTER TABLE `cards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `doctors` (
  `doc_id` int(11) NOT NULL,
  `doc_name` varchar(255) DEFAULT NULL COMMENT 'Имя пользователя',
  `doc_date_of_birth` date DEFAULT NULL COMMENT 'Дата рождения',
  `doc_gender` tinyint(1) DEFAULT NULL COMMENT '0 - М\n1 - Ж',
  `doc_edu` text DEFAULT NULL COMMENT 'Образование',
  `doc_method` text DEFAULT NULL,
  `doc_method_other` text DEFAULT NULL,
  `doc_language` text DEFAULT NULL,
  `doc_edu_additional` text DEFAULT NULL,
  `doc_comunity` text DEFAULT NULL,
  `doc_practice_start` text DEFAULT NULL,
  `doc_online_experience` text DEFAULT NULL,
  `doc_citizenship_other` text DEFAULT NULL,
  `doc_ref` text DEFAULT NULL,
  `doc_ref_other` text DEFAULT NULL,
  `doc_customers_amount_current` text DEFAULT NULL,
  `doc_therapy_length` text DEFAULT NULL,
  `doc_personal_therapy` text DEFAULT NULL,
  `doc_supervision` text DEFAULT NULL,
  `doc_another_job` text DEFAULT NULL,
  `doc_customers_slots_available` text DEFAULT NULL,
  `doc_socials_links` text DEFAULT NULL,
  `doc_citizenship` text DEFAULT NULL,
  `doc_email` varchar(100) DEFAULT NULL,
  `doc_additional_info` text DEFAULT NULL,
  `doc_question_1` text DEFAULT NULL,
  `doc_question_2` text DEFAULT NULL,
  `doc_contact` text DEFAULT NULL,
  `user_photo` text DEFAULT NULL,
  `client_age` text DEFAULT NULL,
  `lgbtq` text DEFAULT NULL,
  `therapy_type` text DEFAULT NULL,
  `doc_phone` varchar(20) DEFAULT NULL,
  `approved` tinyint(1) DEFAULT 1 COMMENT '0 / 1',
  `doc_method_0` tinyint(1) DEFAULT 0,
  `doc_method_1` tinyint(1) DEFAULT 0,
  `doc_method_2` tinyint(1) DEFAULT 0,
  `doc_method_3` tinyint(1) DEFAULT 0,
  `doc_method_4` tinyint(1) DEFAULT 0,
  `doc_method_5` tinyint(1) DEFAULT 0,
  `doc_method_6` tinyint(1) DEFAULT 0,
  `doc_method_7` tinyint(1) DEFAULT 0,
  `doc_method_8` tinyint(1) DEFAULT 0,
  `doc_method_9` tinyint(1) DEFAULT 0,
  `doc_method_10` tinyint(1) DEFAULT 0,
  `doc_language_0` tinyint(1) DEFAULT 0 COMMENT 'ru',
  `doc_language_1` tinyint(1) DEFAULT 0 COMMENT 'hun',
  `doc_language_2` tinyint(1) DEFAULT 0 COMMENT 'en',
  `doc_edu_additional_0` tinyint(1) DEFAULT 0 COMMENT 'ru',
  `doc_edu_additional_1` tinyint(1) DEFAULT 0 COMMENT 'ru',
  `doc_edu_additional_2` tinyint(1) DEFAULT 0 COMMENT 'ru',
  `doc_edu_additional_3` tinyint(1) DEFAULT 0 COMMENT 'ru',
  `doc_edu_additional_4` tinyint(1) DEFAULT 0 COMMENT 'ru',
  PRIMARY KEY (`doc_id`),
  UNIQUE KEY `doc_id_UNIQUE` (`doc_id`),
  CONSTRAINT `testdb_doc_user` FOREIGN KEY (`doc_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES
(166,'string','2024-10-03',0,'string',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','test12@test.ts','string','string','string','string','',NULL,NULL,NULL,'string',1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(167,'string','2024-10-03',0,'string',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','test13@test.ts','string','string','string','string','',NULL,NULL,NULL,'string',1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(168,'string','2024-10-03',0,'string',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','test43@test.ts','string','string','string','string','',NULL,NULL,NULL,'string',1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(169,'string','2024-10-03',0,'string',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','test21@test.ts','string','string','string','string','',NULL,NULL,NULL,'string',1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `educations`
--

DROP TABLE IF EXISTS `educations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `educations` (
  `doc_id` int(11) NOT NULL,
  `e_0` tinyint(1) DEFAULT 0 COMMENT 'Зависимости, аддикции',
  `e_1` tinyint(1) DEFAULT 0 COMMENT 'Растройство пищевого поведения',
  `e_2` tinyint(1) DEFAULT 0 COMMENT 'Сексология',
  `e_3` tinyint(1) DEFAULT 0 COMMENT 'Экстремальные ситуации, ПТСР',
  `e_4` tinyint(1) DEFAULT 0 COMMENT 'Другое',
  PRIMARY KEY (`doc_id`),
  CONSTRAINT `doc_id_add_edu` FOREIGN KEY (`doc_id`) REFERENCES `doctors` (`doc_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `educations`
--

LOCK TABLES `educations` WRITE;
/*!40000 ALTER TABLE `educations` DISABLE KEYS */;
INSERT INTO `educations` VALUES
(166,1,0,0,0,1),
(167,1,0,0,0,1),
(168,1,0,0,0,1),
(169,1,0,0,0,1);
/*!40000 ALTER TABLE `educations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `images` (
  `img_id` int(11) NOT NULL AUTO_INCREMENT,
  `data` blob DEFAULT NULL,
  `name` text DEFAULT NULL,
  `type` text DEFAULT NULL,
  PRIMARY KEY (`img_id`),
  UNIQUE KEY `img_id_UNIQUE` (`img_id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `images`
--

LOCK TABLES `images` WRITE;
/*!40000 ALTER TABLE `images` DISABLE KEYS */;
INSERT INTO `images` VALUES
(53,'a','b','c'),
(54,'a','b','c'),
(55,'a','b','c'),
(56,'a','b','c'),
(57,'a','b','c'),
(58,'a','b','c'),
(59,'a','b','c'),
(60,'a','b','c'),
(61,'a','b','c'),
(62,'a','b','c'),
(63,'a','b','c'),
(64,'a','b','c'),
(65,'a','b','c'),
(66,'a','b','c'),
(67,'a','b','c'),
(68,'a','b','c'),
(69,'a','b','c'),
(70,'a','b','c');
/*!40000 ALTER TABLE `images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `languages`
--

DROP TABLE IF EXISTS `languages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `languages` (
  `doc_id` int(11) NOT NULL,
  `l_0` tinyint(1) DEFAULT 0 COMMENT 'RI',
  `l_1` tinyint(1) DEFAULT 0 COMMENT 'EN',
  `l_2` tinyint(1) DEFAULT 0 COMMENT 'HN',
  PRIMARY KEY (`doc_id`),
  CONSTRAINT `doc_id_lang` FOREIGN KEY (`doc_id`) REFERENCES `doctors` (`doc_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `languages`
--

LOCK TABLES `languages` WRITE;
/*!40000 ALTER TABLE `languages` DISABLE KEYS */;
INSERT INTO `languages` VALUES
(166,1,1,0),
(167,1,1,0),
(168,1,1,0),
(169,1,1,0);
/*!40000 ALTER TABLE `languages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `methods`
--

DROP TABLE IF EXISTS `methods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `methods` (
  `doc_id` int(11) NOT NULL,
  `m_0` tinyint(1) DEFAULT 0 COMMENT 'Психоанализ',
  `m_1` tinyint(1) DEFAULT 0 COMMENT 'Терапия внутренних семейных систем (IFS)',
  `m_2` tinyint(1) DEFAULT 0 COMMENT 'Когнитивно-поведенческая терапия (КПТ)',
  `m_3` tinyint(1) DEFAULT 0 COMMENT 'Травма-фокусированный КПТ',
  `m_4` tinyint(1) DEFAULT 0 COMMENT 'Терапия, сфокусированная на сострадании (CFT)',
  `m_5` tinyint(1) DEFAULT 0 COMMENT 'Диалектическая поведенческая терапия (ДБТ/DBT)',
  `m_6` tinyint(1) DEFAULT 0 COMMENT 'Гештальт-терапия',
  `m_7` tinyint(1) DEFAULT 0 COMMENT 'Системная семейная терапия',
  `m_8` tinyint(1) DEFAULT 0 COMMENT 'Системная сексуальная терапия',
  `m_9` tinyint(1) DEFAULT 0 COMMENT 'Терапия принятия и ответственности',
  `m_10` tinyint(1) DEFAULT 0 COMMENT 'Схема-терапия (CBT)',
  `m_11` tinyint(1) DEFAULT 0 COMMENT 'Экзистенциальная психотерапия(лого и клиент-центрированная)',
  `m_12` tinyint(1) DEFAULT 0 COMMENT 'Трансактный анализ',
  `m_13` tinyint(1) DEFAULT 0 COMMENT 'Десенсибилизация и переработка движением глаз(EMDR/ДПДГ)',
  `m_14` tinyint(1) DEFAULT 0 COMMENT 'Рационально эмоционально поведенческая терапия(REBT)',
  `m_15` tinyint(1) DEFAULT 0 COMMENT 'Эмоционально-фокусированная терапия (ЭФТ)',
  `m_16` tinyint(1) DEFAULT 0 COMMENT 'Арт-терапия',
  PRIMARY KEY (`doc_id`),
  CONSTRAINT `doc_id_methods` FOREIGN KEY (`doc_id`) REFERENCES `doctors` (`doc_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `methods`
--

LOCK TABLES `methods` WRITE;
/*!40000 ALTER TABLE `methods` DISABLE KEYS */;
INSERT INTO `methods` VALUES
(166,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0),
(167,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0),
(168,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0),
(169,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `methods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule`
--

DROP TABLE IF EXISTS `schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schedule` (
  `sh_id` int(11) NOT NULL AUTO_INCREMENT,
  `doctor_id` varchar(45) NOT NULL,
  `date_time` datetime NOT NULL,
  `client` int(11) DEFAULT NULL,
  PRIMARY KEY (`sh_id`),
  UNIQUE KEY `sh_id_UNIQUE` (`sh_id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule`
--

LOCK TABLES `schedule` WRITE;
/*!40000 ALTER TABLE `schedule` DISABLE KEYS */;
INSERT INTO `schedule` VALUES
(95,'82','2024-09-15 01:00:00',NULL),
(96,'82','2024-09-15 03:00:00',NULL);
/*!40000 ALTER TABLE `schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `symptoms`
--

DROP TABLE IF EXISTS `symptoms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `symptoms` (
  `doc_id` int(11) NOT NULL,
  `s_1` tinyint(1) DEFAULT 0,
  `s_2` tinyint(1) DEFAULT 0,
  `s_3` tinyint(1) DEFAULT 0,
  `s_4` tinyint(1) DEFAULT 0,
  `s_5` tinyint(1) DEFAULT 0,
  `s_6` tinyint(1) DEFAULT 0,
  `s_7` tinyint(1) DEFAULT 0,
  `s_8` tinyint(1) DEFAULT 0,
  `s_9` tinyint(1) DEFAULT 0,
  `s_10` tinyint(1) DEFAULT 0,
  `s_11` tinyint(1) DEFAULT 0,
  `s_12` tinyint(1) DEFAULT 0,
  `s_13` tinyint(1) DEFAULT 0,
  `s_14` tinyint(1) DEFAULT 0,
  `s_15` tinyint(1) DEFAULT 0,
  `s_16` tinyint(1) DEFAULT 0,
  `s_17` tinyint(1) DEFAULT 0,
  `s_18` tinyint(1) DEFAULT 0,
  `s_19` tinyint(1) DEFAULT 0,
  `s_20` tinyint(1) DEFAULT 0,
  `s_21` tinyint(1) DEFAULT 0,
  `s_22` tinyint(1) DEFAULT 0,
  `s_23` tinyint(1) DEFAULT 0,
  `s_24` tinyint(1) DEFAULT 0,
  `s_25` tinyint(1) DEFAULT 0,
  `s_26` tinyint(1) DEFAULT 0,
  `s_27` tinyint(1) DEFAULT 0,
  `s_28` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`doc_id`),
  CONSTRAINT `doc_id` FOREIGN KEY (`doc_id`) REFERENCES `doctors` (`doc_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `symptoms`
--

LOCK TABLES `symptoms` WRITE;
/*!40000 ALTER TABLE `symptoms` DISABLE KEYS */;
/*!40000 ALTER TABLE `symptoms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tokens`
--

DROP TABLE IF EXISTS `tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tokens` (
  `user_id` int(11) NOT NULL,
  `token` varchar(255) NOT NULL,
  `time` datetime NOT NULL DEFAULT current_timestamp(),
  KEY `fk_tokens_id` (`user_id`),
  CONSTRAINT `fk_tokens_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tokens`
--

LOCK TABLES `tokens` WRITE;
/*!40000 ALTER TABLE `tokens` DISABLE KEYS */;
INSERT INTO `tokens` VALUES
(156,'9fe45c33-8213-44ef-9786-6351836afb2c','2024-10-03 00:09:04'),
(157,'b6b5f91a-dc71-43f5-a4d4-af5f544bfad9','2024-10-03 00:09:39'),
(158,'39a28eb1-cc3b-4b0d-8131-acc203cda3b8','2024-10-03 00:11:10'),
(159,'29fb9df9-421b-4720-9314-2e787052d8cb','2024-10-03 00:12:02'),
(160,'4ecfa209-d7eb-49e9-b235-a4c23cef0bdd','2024-10-03 00:12:51'),
(161,'65f10028-df63-4dcf-a118-63a17d9945aa','2024-10-03 00:13:33'),
(162,'56a06f30-ecc9-4ed1-aabe-83a97e5bba30','2024-10-03 00:13:53'),
(163,'31784de3-7b6b-47fd-bfc0-15747d1cc313','2024-10-03 00:14:15'),
(164,'b8f4c6d3-b58f-4560-ac8b-642eb42fc8e2','2024-10-03 00:16:27'),
(165,'b796d2e7-f7ab-4290-9dee-b5a8418c4ec1','2024-10-03 00:16:42'),
(166,'54bf3718-0d68-4357-b337-9ec7455c4019','2024-10-03 00:16:57'),
(167,'034fb4bc-a936-4e83-bcd7-95814d6eb971','2024-10-03 00:17:13'),
(168,'29629b10-3c53-4f6f-8635-553051f1dfba','2024-10-03 00:19:35'),
(169,'b0308e98-509f-4988-80bd-cd358281488c','2024-10-03 00:20:00'),
(154,'e75827cb-79c3-42dd-80b9-50ec73fdac44','2024-10-03 00:25:36');
/*!40000 ALTER TABLE `tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(64) NOT NULL,
  `is_therapist` tinyint(4) DEFAULT 0,
  `is_admin` tinyint(4) DEFAULT 0,
  `registred_date` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=170 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(154,'test@test.ru','12345678',0,1,'2024-09-30 00:00:00'),
(155,'tes1t@test.ru','12345678',0,0,'2024-09-30 00:00:00'),
(156,'test2@test.ts','E5e4M6U5',1,0,'2024-10-03 00:00:00'),
(157,'test3@test.ts','d7r3K0I0',1,0,'2024-10-03 00:00:00'),
(158,'test4@test.ts','e6C5r7y0',1,0,'2024-10-03 00:00:00'),
(159,'test5@test.ts','u8d4H7i6',1,0,'2024-10-03 00:00:00'),
(160,'test6@test.ts','i3K7p9o4',1,0,'2024-10-03 00:00:00'),
(161,'test7@test.ts','G6i7y5k8',1,0,'2024-10-03 00:00:00'),
(162,'test8@test.ts','w5M2y0A3',1,0,'2024-10-03 00:00:00'),
(163,'test9@test.ts','G2F5U7r9',1,0,'2024-10-03 00:00:00'),
(164,'test10@test.ts','k1D2V8G7',1,0,'2024-10-03 00:00:00'),
(165,'test11@test.ts','M2Y4n2e6',1,0,'2024-10-03 00:00:00'),
(166,'test12@test.ts','H8h6t4d9',1,0,'2024-10-03 00:00:00'),
(167,'test13@test.ts','y2q0W7y3',1,0,'2024-10-03 00:00:00'),
(168,'test43@test.ts','E0d3A3l8',1,0,'2024-10-03 00:00:00'),
(169,'test21@test.ts','t6h5k7z7',1,0,'2024-10-03 00:00:00');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2024-10-03  0:36:20
