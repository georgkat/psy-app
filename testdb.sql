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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cards`
--

LOCK TABLES `cards` WRITE;
/*!40000 ALTER TABLE `cards` DISABLE KEYS */;
/*!40000 ALTER TABLE `cards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client_languages`
--

DROP TABLE IF EXISTS `client_languages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `client_languages` (
  `client_id` int(11) NOT NULL,
  `l_0` tinyint(1) DEFAULT 0 COMMENT 'RI',
  `l_1` tinyint(1) DEFAULT 0 COMMENT 'RI',
  `l_2` tinyint(1) DEFAULT 0 COMMENT 'RI',
  PRIMARY KEY (`client_id`),
  CONSTRAINT `cli_id_lang` FOREIGN KEY (`client_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client_languages`
--

LOCK TABLES `client_languages` WRITE;
/*!40000 ALTER TABLE `client_languages` DISABLE KEYS */;
INSERT INTO `client_languages` VALUES
(210,1,0,1),
(228,0,1,0),
(229,0,1,0),
(230,0,1,0),
(232,0,0,0),
(233,1,0,0),
(234,0,0,0),
(235,0,0,0),
(236,0,0,0),
(237,0,0,0),
(238,1,0,0),
(244,0,0,1),
(245,0,0,0);
/*!40000 ALTER TABLE `client_languages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client_symptoms`
--

DROP TABLE IF EXISTS `client_symptoms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `client_symptoms` (
  `client_id` int(11) NOT NULL,
  `s_0` tinyint(1) DEFAULT 0,
  `s_1` tinyint(1) DEFAULT 0,
  `s_2` tinyint(1) DEFAULT 0,
  `s_3` tinyint(1) DEFAULT 0,
  `s_4` tinyint(1) DEFAULT 0,
  `s_5` tinyint(1) DEFAULT 0,
  `s_6` tinyint(1) DEFAULT 0,
  `s_7` tinyint(1) DEFAULT 0,
  `s_8` tinyint(1) DEFAULT 0,
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
  `s_9` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`client_id`),
  CONSTRAINT `cli_id_sym` FOREIGN KEY (`client_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client_symptoms`
--

LOCK TABLES `client_symptoms` WRITE;
/*!40000 ALTER TABLE `client_symptoms` DISABLE KEYS */;
INSERT INTO `client_symptoms` VALUES
(210,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(228,1,1,1,0,0,1,1,0,0,1,0,0,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,1),
(229,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0),
(230,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0),
(232,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(233,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(234,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(235,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(236,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(237,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(238,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(244,0,0,0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(245,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `client_symptoms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients`
--

DROP TABLE IF EXISTS `clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients` (
  `client_id` int(11) NOT NULL,
  `name` text DEFAULT NULL,
  `user_age` date DEFAULT NULL,
  `user_experience` tinyint(1) DEFAULT NULL,
  `user_type` tinyint(1) DEFAULT NULL,
  `user_therapist_gender` tinyint(1) DEFAULT NULL,
  `user_time` varchar(45) DEFAULT NULL,
  `user_specific_date_time` varchar(45) DEFAULT NULL,
  `user_price` tinyint(1) DEFAULT NULL,
  `user_phone` varchar(45) DEFAULT NULL,
  `has_therapist` int(11) DEFAULT NULL,
  `user_photo` varchar(45) DEFAULT NULL,
  `user_timezone` tinyint(2) DEFAULT NULL,
  PRIMARY KEY (`client_id`),
  UNIQUE KEY `client_id_UNIQUE` (`client_id`),
  CONSTRAINT `cli_id` FOREIGN KEY (`client_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients`
--

LOCK TABLES `clients` WRITE;
/*!40000 ALTER TABLE `clients` DISABLE KEYS */;
INSERT INTO `clients` VALUES
(210,'Vasyan','2024-10-03',1,1,0,'string','',0,'12345',NULL,NULL,NULL),
(211,'*',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
(228,'Мила','1980-10-01',1,1,0,'2','2024-11-15T15:00',0,'89111111111',NULL,NULL,NULL),
(229,'Василий','1980-10-20',1,1,0,'1','',2,'8911111111',NULL,NULL,NULL),
(230,'Васисуалий','1980-10-10',1,1,2,'2','2024-11-25T15:00',2,'89111111111',NULL,NULL,NULL),
(232,'Иван',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
(233,'Иван','2000-05-01',0,0,1,'0','',0,'',NULL,NULL,NULL),
(234,'Мила',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
(235,'Мила',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
(236,'Мила',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
(237,'Мила',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
(238,'Мила','2000-10-10',0,0,1,'0','',0,'',NULL,NULL,NULL),
(244,'Иван','1325-10-21',1,1,1,'string','',2,'13432525',NULL,'None',3),
(245,'Мила',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,243,NULL,NULL);
/*!40000 ALTER TABLE `clients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doc_symptoms`
--

DROP TABLE IF EXISTS `doc_symptoms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `doc_symptoms` (
  `doc_id` int(11) NOT NULL,
  `s_0` tinyint(1) DEFAULT 0,
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
  CONSTRAINT `doc_sy_id_fk` FOREIGN KEY (`doc_id`) REFERENCES `doctors` (`doc_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doc_symptoms`
--

LOCK TABLES `doc_symptoms` WRITE;
/*!40000 ALTER TABLE `doc_symptoms` DISABLE KEYS */;
INSERT INTO `doc_symptoms` VALUES
(223,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(225,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1),
(227,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(231,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(239,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(240,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(241,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(243,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `doc_symptoms` ENABLE KEYS */;
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
  `doc_client_age` int(1) DEFAULT 0,
  `doc_lgbtq` int(1) DEFAULT 0,
  `doc_therapy_type` int(1) DEFAULT 0,
  `doc_phone` varchar(20) DEFAULT NULL,
  `approved` tinyint(1) DEFAULT 1 COMMENT '0 / 1',
  PRIMARY KEY (`doc_id`),
  UNIQUE KEY `doc_id_UNIQUE` (`doc_id`),
  CONSTRAINT `testdb_doc_user` FOREIGN KEY (`doc_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES
(166,'string','2024-10-03',0,'string',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','test12@test.ts','string','string','string','string','',NULL,NULL,NULL,'string',1),
(167,'string','2024-10-03',0,'string',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','test13@test.ts','string','string','string','string','',NULL,NULL,NULL,'string',1),
(168,'string','2024-10-03',0,'string',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','test43@test.ts','string','string','string','string','',NULL,NULL,NULL,'string',1),
(169,'string','2024-10-03',0,'string',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','test21@test.ts','string','string','string','string','',NULL,NULL,NULL,'string',1),
(170,'string','2024-10-03',0,'[{\'year\': \'str\', \'university\': \'str\', \'faculty\': \'str\', \'degree\': \'str\'}, {\'year\': \'str\', \'university\': \'str\', \'faculty\': \'str\', \'degree\': \'str\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','0-string112','string','string','string','string','',NULL,NULL,NULL,'string',1),
(172,'ываываы','1980-01-15',0,'[{\'year\': \'2000\', \'university\': \'ывапывапыв\', \'faculty\': \'ыекцуе\', \'degree\': \'кевке\'}, {\'year\': \'2001\', \'university\': \'вапвап\', \'faculty\': \'вапвапв\', \'degree\': \'вапвап\'}]',NULL,'',NULL,NULL,'ываываы','09 2002','20','','0','','20','20','yes','yes','впвапваа','5-15','вкпквпкввк','0','test-doc-22@test.ru','rgdrtgrdt','drgrdgdr','drgdrgr','doc_contact_email','',NULL,NULL,NULL,'6165516516',1),
(173,'Doc Simons','2112-09-01',0,'2003 - Moscow State University - Faculty of Psychology, Clinical Psychology - Bachelor.\n',NULL,'',NULL,NULL,'If you do, please specify?\n\n','01 1990','15','','2','','15','15','yes','yes','How are your interests and priorities distributed?\n\n','1-10','mediua','2','samuel@docs.com','Tell us about yourself in free form.*\n\n','What things do you find unacceptable in the psychotherapeutic process? Why?*\n\n','What do you think you can\'t work with online? Why?*\n\n','doc_contact_whatsapp','',NULL,NULL,NULL,'1 234-567-8910',1),
(174,'Doc Simons','2112-09-01',0,'2003 - Moscow State University - Faculty of Psychology, Clinical Psychology - Bachelor.\n',NULL,'',NULL,NULL,'If you do, please specify?\n\n','01 1990','15','','2','','15','15','yes','yes','How are your interests and priorities distributed?\n\n','1-10','mediua','2','samuedl@docs.com','Tell us about yourself in free form.*\n\n','What things do you find unacceptable in the psychotherapeutic process? Why?*\n\n','What do you think you can\'t work with online? Why?*\n\n','doc_contact_whatsapp','',NULL,NULL,NULL,'1 234-567-8910',1),
(175,'Doc Simons','2112-09-01',0,'2003 - Moscow State University - Faculty of Psychology, Clinical Psychology - Bachelor.\n',NULL,'',NULL,NULL,'If you do, please specify?\n\n','01 1990','15','','2','','15','15','yes','yes','How are your interests and priorities distributed?\n\n','1-10','mediua','2','sasmuedl@docs.com','Tell us about yourself in free form.*\n\n','What things do you find unacceptable in the psychotherapeutic process? Why?*\n\n','What do you think you can\'t work with online? Why?*\n\n','doc_contact_whatsapp','',NULL,NULL,NULL,'1 234-567-8910',1),
(176,'Doc Simons','2112-09-01',0,'2003 - Moscow State University - Faculty of Psychology, Clinical Psychology - Bachelor.\n',NULL,'',NULL,NULL,'If you do, please specify?\n\n','01 1990','15','','2','','15','15','yes','yes','How are your interests and priorities distributed?\n\n','1-10','mediua','2','sasmueыdl@docs.com','Tell us about yourself in free form.*\n\n','What things do you find unacceptable in the psychotherapeutic process? Why?*\n\n','What do you think you can\'t work with online? Why?*\n\n','doc_contact_whatsapp','',NULL,NULL,NULL,'1 234-567-8910',1),
(177,'Doc Simons','2112-09-01',0,'2003 - Moscow State University - Faculty of Psychology, Clinical Psychology - Bachelor.\n',NULL,'',NULL,NULL,'If you do, please specify?\n\n','01 1990','15','','2','','15','15','yes','yes','How are your interests and priorities distributed?\n\n','1-10','mediua','2','sassmueыdl@docs.com','Tell us about yourself in free form.*\n\n','What things do you find unacceptable in the psychotherapeutic process? Why?*\n\n','What do you think you can\'t work with online? Why?*\n\n','doc_contact_whatsapp','',NULL,NULL,NULL,'1 234-567-8910',1),
(179,'Doc Simons','2112-09-01',0,'2003 - Moscow State University - Faculty of Psychology, Clinical Psychology - Bachelor.\n',NULL,'',NULL,NULL,'If you do, please specify?\n\n','01 1990','15','','2','','15','15','yes','yes','How are your interests and priorities distributed?\n\n','1-10','mediua','2','sasssmuseыdl@docs.com','Tell us about yourself in free form.*\n\n','What things do you find unacceptable in the psychotherapeutic process? Why?*\n\n','What do you think you can\'t work with online? Why?*\n\n','doc_contact_whatsapp','',NULL,NULL,NULL,'1 234-567-8910',1),
(180,'Doc Simons','2112-09-01',0,'2003 - Moscow State University - Faculty of Psychology, Clinical Psychology - Bachelor.\n',NULL,'',NULL,NULL,'If you do, please specify?\n\n','01 1990','15','','2','','15','15','yes','yes','How are your interests and priorities distributed?\n\n','1-10','mediua','2','sassssmuseыdl@docs.com','Tell us about yourself in free form.*\n\n','What things do you find unacceptable in the psychotherapeutic process? Why?*\n\n','What do you think you can\'t work with online? Why?*\n\n','doc_contact_whatsapp','',NULL,NULL,NULL,'1 234-567-8910',1),
(181,'Doc Simons','2112-09-01',0,'2003 - Moscow State University - Faculty of Psychology, Clinical Psychology - Bachelor.\n',NULL,'',NULL,NULL,'If you do, please specify?\n\n','01 1990','15','','2','','15','15','yes','yes','How are your interests and priorities distributed?\n\n','1-10','mediua','2','sasssdsmuseыdl@docs.com','Tell us about yourself in free form.*\n\n','What things do you find unacceptable in the psychotherapeutic process? Why?*\n\n','What do you think you can\'t work with online? Why?*\n\n','doc_contact_whatsapp','',NULL,NULL,NULL,'1 234-567-8910',1),
(190,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','53s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(191,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','54s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(192,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','541s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(193,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','5141s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(194,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','51411s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(195,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','514s11s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(196,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','51s4s11s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(197,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','51s4ss11s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(198,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','51s4ss1s1s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(199,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','51s4sss1s1s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(200,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','51s4sss1ss1s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(201,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','51s4ssss1ss1s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(202,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','51s4sssss1ss1s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(203,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','51s4ssssss1ss1s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(204,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','51s4sssssss1ss1s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(205,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','51s4sssssss1sfs1s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(206,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','51s4ssssssss1sfs1s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(207,'string','2024-10-04',0,'[{\'year\': \'1990\', \'university\': \'hoggwards\', \'faculty\': \'griffindor\', \'degree\': \'B\'}, {\'year\': \'1995\', \'university\': \'hoggwards\', \'faculty\': \'hoggwards\', \'degree\': \'M\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','51s4sssыsssss1sfs1s','string','string','string','string','',NULL,NULL,NULL,'string',1),
(216,'string','2024-10-04',0,'[{\'year\': 1999, \'university\': \'MUS\', \'faculty\': \'FUS\', \'degree\': \'Bc\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','1f','string','string','string','string','',NULL,NULL,NULL,'string',1),
(220,'string','2024-10-05',0,'[{\'year\': 1234, \'university\': \'a\', \'faculty\': \'b\', \'degree\': \'c\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','stddring','string','string','string','string','',NULL,NULL,NULL,'string',1),
(222,'string','2024-10-05',0,'[{\'year\': 1234, \'university\': \'a\', \'faculty\': \'b\', \'degree\': \'c\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','stddrfаing','string','string','string','string','',NULL,NULL,NULL,'string',1),
(223,'string','2024-10-06',0,'[{\'year\': 0, \'university\': \'U\', \'faculty\': \'F\', \'degree\': \'D\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','stringgggg','blablablablablablabla','string','string','string','',1,1,2,'string',1),
(225,'string','2075-01-07',0,'[{\'year\': 0, \'university\': \'U\', \'faculty\': \'F\', \'degree\': \'D\'}]',NULL,'',NULL,NULL,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','stringggggg','НОВЫЕ ДАННЫЕ','string','string','string','',1,0,0,'string',1),
(227,'Петр Петров','1970-01-01',0,'[{\'year\': \'2000\', \'university\': \'ываыва\', \'faculty\': \'ываывавы\', \'degree\': \'ываываыва\'}]',NULL,'',NULL,NULL,'аывываыва','01 2000','10','','other','','10','10','yes','yes','ываывавыа','5','ваывыавыа','other','kksdfnsffkjf@jskdjfsdf.fd','sgsdsdsfsdf','sdfsdfsdfsf','sdfsdfsdfsdf','doc_contact_email','',0,0,0,'89111111111',1),
(231,'Васисуалий Лоханкин','1980-10-25',0,'[{\'year\': \'2001\', \'university\': \'лвдаоывадо\', \'faculty\': \'двалоыдваоад\', \'degree\': \'двлаоывдао\'}, {\'year\': \'2002\', \'university\': \'дывалоывад\', \'faculty\': \'ыдвлоадываод\', \'degree\': \'дывлаоывдало\'}]',NULL,'',NULL,NULL,'фывфыфв','04 2005','10','','0','','10','10','yes','yes','авпвапв','5-15','вапаввп','0','test-doc@test111.ru','d;fldsk;l','ds;flksdf;kl','fsfdsdfsf','doc_contact_email','',0,0,0,'89111111111',1),
(239,'Иван Иванов','1980-01-01',0,'[{\'year\': \'2000\', \'university\': \'МГУ\', \'faculty\': \'психологии\', \'degree\': \'психолог\'}, {\'year\': \'2002\', \'university\': \'СПбГУ\', \'faculty\': \'психологии\', \'degree\': \' психолог\'}]',NULL,'',NULL,NULL,'-','03 2005','10','','0','','10','10','yes','yes','-','5-10','-','0','ivanov.ivan@test.ru','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.','-','-','doc_contact_email','',0,0,0,'89111111111',1),
(240,'Петр Петров','1979-10-10',0,'[{\'year\': \'2001\', \'university\': \'МГУ\', \'faculty\': \'психологии\', \'degree\': \'бакалавр\'}, {\'year\': \'2003\', \'university\': \'РГМУ\', \'faculty\': \'психиатрия\', \'degree\': \'врач-психиатр\'}]',NULL,'',NULL,NULL,'-','03 2001','10','','0','','10','10','yes','yes','-','5-10','-','0','','','','','','',0,0,0,'891',1),
(241,'Василий Васильев','1995-05-05',0,'[{\'year\': \'2005\', \'university\': \'ФГУ\', \'faculty\': \'психологии\', \'degree\': \'психолог\'}]',NULL,'',NULL,NULL,'-','06 2008','5','','0','','5','5','yes','yes','-','5-10','-','0','vasili.vasilyev@test.ru','It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).','-','-','doc_contact_email','',0,0,0,'89111111111',1),
(242,'Василий Васильев','1995-05-05',0,'[{\'year\': \'2005\', \'university\': \'ФГУ\', \'faculty\': \'психологии\', \'degree\': \'психолог\'}]',NULL,'',NULL,NULL,'-','06 2008','5','','0','','5','5','yes','yes','-','5-10','-','0','vasili.vasilyev@test.ru','It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).','-','-','doc_contact_email','',0,0,0,'89111111111',1),
(243,'Анна Смирнова','1992-12-05',1,'[{\'year\': \'2005\', \'university\': \'СПбГУ\', \'faculty\': \'психологии\', \'degree\': \'психолог\'}]',NULL,'',NULL,NULL,'-','05 2010','5','','0','','5','5','yes','yes','-','5-15','-','0','anna.sidorova@test.ru','There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn\'t anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.','-','-','doc_contact_email','',0,0,0,'89111111111',1);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(169,1,0,0,0,1),
(170,1,0,0,0,1),
(172,1,1,0,0,0),
(173,0,0,1,0,0),
(174,0,0,1,0,0),
(175,0,0,1,0,0),
(176,0,0,1,0,0),
(177,0,0,1,0,0),
(179,0,0,1,0,0),
(180,0,0,1,0,0),
(181,0,0,1,0,0),
(190,1,0,1,0,0),
(191,1,0,1,0,0),
(192,1,0,1,0,0),
(193,1,0,1,0,0),
(194,1,0,1,0,0),
(195,1,0,1,0,0),
(196,1,0,1,0,0),
(197,1,0,1,0,0),
(198,1,0,1,0,0),
(199,1,0,1,0,0),
(200,1,0,1,0,0),
(201,1,0,1,0,0),
(202,1,0,1,0,0),
(203,1,0,1,0,0),
(204,1,0,1,0,0),
(205,1,0,1,0,0),
(206,1,0,1,0,0),
(207,1,0,1,0,0),
(216,0,1,0,0,0),
(220,0,0,0,1,0),
(222,0,0,0,1,0),
(223,0,0,0,1,0),
(225,0,0,0,1,0),
(227,0,0,0,0,0),
(231,1,1,1,0,0),
(239,1,1,0,0,0),
(240,1,0,0,1,0),
(241,0,0,0,0,1),
(242,1,0,0,1,0),
(243,1,0,0,0,0);
/*!40000 ALTER TABLE `educations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `educations_main`
--

DROP TABLE IF EXISTS `educations_main`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `educations_main` (
  `doc_id` int(11) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `university` text DEFAULT NULL,
  `faculty` text DEFAULT NULL,
  `degree` text DEFAULT NULL,
  KEY `ed_main_fc` (`doc_id`),
  CONSTRAINT `ed_main_fc` FOREIGN KEY (`doc_id`) REFERENCES `doctors` (`doc_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `educations_main`
--

LOCK TABLES `educations_main` WRITE;
/*!40000 ALTER TABLE `educations_main` DISABLE KEYS */;
INSERT INTO `educations_main` VALUES
(190,1990,'hoggwards','griffindor','B'),
(190,1995,'hoggwards','hoggwards','M'),
(191,1990,'hoggwards','griffindor','B'),
(191,1995,'hoggwards','hoggwards','M'),
(192,1990,'hoggwards','griffindor','B'),
(192,1995,'hoggwards','hoggwards','M'),
(193,1990,'hoggwards','griffindor','B'),
(193,1995,'hoggwards','hoggwards','M'),
(194,1990,'hoggwards','griffindor','B'),
(194,1995,'hoggwards','hoggwards','M'),
(195,1990,'hoggwards','griffindor','B'),
(195,1995,'hoggwards','hoggwards','M'),
(196,1990,'hoggwards','griffindor','B'),
(196,1995,'hoggwards','hoggwards','M'),
(197,1990,'hoggwards','griffindor','B'),
(197,1995,'hoggwards','hoggwards','M'),
(198,1990,'hoggwards','griffindor','B'),
(198,1995,'hoggwards','hoggwards','M'),
(199,1990,'hoggwards','griffindor','B'),
(199,1995,'hoggwards','hoggwards','M'),
(200,1990,'hoggwards','griffindor','B'),
(200,1995,'hoggwards','hoggwards','M'),
(201,1990,'hoggwards','griffindor','B'),
(201,1995,'hoggwards','hoggwards','M'),
(202,1990,'hoggwards','griffindor','B'),
(202,1995,'hoggwards','hoggwards','M'),
(203,1990,'hoggwards','griffindor','B'),
(203,1995,'hoggwards','hoggwards','M'),
(204,1990,'hoggwards','griffindor','B'),
(204,1995,'hoggwards','hoggwards','M'),
(205,1990,'hoggwards','griffindor','B'),
(205,1995,'hoggwards','hoggwards','M'),
(206,1990,'hoggwards','griffindor','B'),
(206,1995,'hoggwards','hoggwards','M'),
(207,1990,'hoggwards','griffindor','B'),
(207,1995,'hoggwards','hoggwards','M'),
(216,1999,'MUS','FUS','Bc'),
(220,1234,'a','b','c'),
(222,1234,'a','b','c'),
(223,0,'U','F','D'),
(225,0,'U','F','D'),
(227,2000,'ываыва','ываывавы','ываываыва'),
(231,2001,'лвдаоывадо','двалоыдваоад','двлаоывдао'),
(231,2002,'дывалоывад','ыдвлоадываод','дывлаоывдало'),
(239,2000,'МГУ','психологии','психолог'),
(239,2002,'СПбГУ','психологии',' психолог'),
(240,2001,'МГУ','психологии','бакалавр'),
(240,2003,'РГМУ','психиатрия','врач-психиатр'),
(241,2005,'ФГУ','психологии','психолог'),
(242,2005,'ФГУ','психологии','психолог'),
(243,2005,'СПбГУ','психологии','психолог'),
(243,2005,'A','B','C');
/*!40000 ALTER TABLE `educations_main` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(169,1,1,0),
(170,1,0,1),
(172,0,0,1),
(173,0,1,0),
(174,0,1,0),
(175,0,1,0),
(176,0,1,0),
(177,0,1,0),
(179,0,1,0),
(180,0,1,0),
(181,0,1,0),
(190,1,0,1),
(191,1,0,1),
(192,1,0,1),
(193,1,0,1),
(194,1,0,1),
(195,1,0,1),
(196,1,0,1),
(197,1,0,1),
(198,1,0,1),
(199,1,0,1),
(200,1,0,1),
(201,1,0,1),
(202,1,0,1),
(203,1,0,1),
(204,1,0,1),
(205,1,0,1),
(206,1,0,1),
(207,1,0,1),
(216,0,1,0),
(220,0,0,1),
(222,0,0,1),
(223,0,0,1),
(225,1,1,0),
(227,1,0,0),
(231,1,0,1),
(239,1,0,0),
(240,1,0,0),
(241,1,0,0),
(242,1,0,0),
(243,1,0,0);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(169,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0),
(170,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0),
(172,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(173,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0),
(174,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0),
(175,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0),
(176,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0),
(177,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0),
(179,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0),
(180,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0),
(181,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0),
(190,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(191,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(192,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(193,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(194,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(195,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(196,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(197,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(198,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(199,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(200,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(201,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(202,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(203,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(204,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(205,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(206,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(207,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(216,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(220,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(222,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(223,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(225,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(227,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0),
(231,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(239,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(240,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(241,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(242,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(243,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
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
  `accepted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`sh_id`),
  UNIQUE KEY `sh_id_UNIQUE` (`sh_id`)
) ENGINE=InnoDB AUTO_INCREMENT=224 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule`
--

LOCK TABLES `schedule` WRITE;
/*!40000 ALTER TABLE `schedule` DISABLE KEYS */;
INSERT INTO `schedule` VALUES
(95,'82','2024-09-15 01:00:00',NULL,NULL),
(96,'82','2024-09-15 03:00:00',NULL,NULL),
(97,'223','2024-09-15 03:00:00',NULL,NULL),
(107,'239','2024-10-22 00:00:00',NULL,NULL),
(108,'239','2024-10-22 01:00:00',NULL,NULL),
(109,'239','2024-10-22 02:00:00',NULL,NULL),
(110,'239','2024-10-24 00:00:00',NULL,NULL),
(111,'239','2024-10-24 01:00:00',NULL,NULL),
(112,'239','2024-10-24 02:00:00',NULL,NULL),
(113,'239','2024-10-26 00:00:00',NULL,NULL),
(114,'239','2024-10-26 01:00:00',NULL,NULL),
(115,'239','2024-10-26 02:00:00',NULL,NULL),
(116,'239','2024-10-29 00:00:00',NULL,NULL),
(117,'239','2024-10-29 01:00:00',NULL,NULL),
(118,'239','2024-10-29 02:00:00',NULL,NULL),
(119,'239','2024-10-31 00:00:00',NULL,NULL),
(120,'239','2024-10-31 01:00:00',NULL,NULL),
(121,'239','2024-10-31 02:00:00',NULL,NULL),
(122,'239','2024-11-02 00:00:00',NULL,NULL),
(123,'239','2024-11-02 01:00:00',NULL,NULL),
(124,'239','2024-11-02 02:00:00',NULL,NULL),
(142,'241','2024-10-23 00:00:00',NULL,NULL),
(143,'241','2024-10-23 01:00:00',NULL,NULL),
(144,'241','2024-10-23 02:00:00',NULL,NULL),
(145,'241','2024-10-23 03:00:00',NULL,NULL),
(146,'241','2024-10-23 04:00:00',NULL,NULL),
(147,'241','2024-10-25 00:00:00',NULL,NULL),
(148,'241','2024-10-25 01:00:00',NULL,NULL),
(149,'241','2024-10-25 02:00:00',NULL,NULL),
(150,'241','2024-10-25 03:00:00',NULL,NULL),
(151,'241','2024-10-25 04:00:00',NULL,NULL),
(152,'241','2024-10-27 00:00:00',NULL,NULL),
(153,'241','2024-10-27 01:00:00',NULL,NULL),
(154,'241','2024-10-27 02:00:00',NULL,NULL),
(155,'241','2024-10-27 03:00:00',NULL,NULL),
(156,'241','2024-10-27 04:00:00',NULL,NULL),
(157,'241','2024-10-29 03:00:00',NULL,NULL),
(158,'241','2024-10-29 04:00:00',NULL,NULL),
(159,'241','2024-10-29 05:00:00',NULL,NULL),
(160,'241','2024-10-29 06:00:00',NULL,NULL),
(161,'241','2024-11-01 03:00:00',NULL,NULL),
(162,'241','2024-11-01 04:00:00',NULL,NULL),
(163,'241','2024-11-01 05:00:00',NULL,NULL),
(164,'241','2024-11-01 06:00:00',NULL,NULL),
(165,'241','2024-11-07 03:00:00',NULL,NULL),
(166,'241','2024-11-07 04:00:00',NULL,NULL),
(167,'241','2024-11-07 05:00:00',NULL,NULL),
(168,'241','2024-11-07 06:00:00',NULL,NULL),
(169,'241','2024-11-10 03:00:00',NULL,NULL),
(170,'241','2024-11-10 04:00:00',NULL,NULL),
(171,'241','2024-11-10 05:00:00',NULL,NULL),
(172,'241','2024-11-10 06:00:00',NULL,NULL),
(173,'241','2024-11-12 04:00:00',NULL,NULL),
(174,'241','2024-11-12 05:00:00',NULL,NULL),
(175,'241','2024-11-12 06:00:00',NULL,NULL),
(176,'241','2024-11-12 07:00:00',NULL,NULL),
(177,'242','2024-10-23 03:00:00',NULL,NULL),
(178,'242','2024-10-27 01:00:00',NULL,NULL),
(179,'242','2024-10-29 04:00:00',NULL,NULL),
(180,'242','2024-10-29 05:00:00',NULL,NULL),
(181,'242','2024-11-01 04:00:00',NULL,NULL),
(182,'242','2024-11-01 05:00:00',NULL,NULL),
(183,'242','2024-11-01 06:00:00',NULL,NULL),
(184,'242','2024-11-10 03:00:00',NULL,NULL),
(185,'243','2024-10-22 04:00:00',NULL,NULL),
(186,'243','2024-10-22 05:00:00',NULL,NULL),
(187,'243','2024-10-22 06:00:00',NULL,NULL),
(188,'243','2024-10-22 08:00:00',NULL,NULL),
(189,'243','2024-10-22 10:00:00',NULL,NULL),
(190,'243','2024-10-25 04:00:00',NULL,NULL),
(191,'243','2024-10-25 05:00:00',NULL,NULL),
(192,'243','2024-10-25 07:00:00',NULL,NULL),
(193,'243','2024-10-25 09:00:00',NULL,NULL),
(194,'243','2024-10-27 04:00:00',NULL,NULL),
(195,'243','2024-10-27 05:00:00',NULL,NULL),
(196,'243','2024-10-27 07:00:00',NULL,NULL),
(197,'243','2024-10-27 09:00:00',NULL,NULL),
(198,'243','2024-11-06 02:00:00',NULL,NULL),
(199,'243','2024-11-06 03:00:00',NULL,NULL),
(200,'243','2024-11-06 05:00:00',NULL,NULL),
(201,'243','2024-11-09 05:00:00',NULL,NULL),
(202,'243','2024-11-09 06:00:00',NULL,NULL),
(203,'243','2024-11-09 08:00:00',NULL,NULL),
(204,'243','2024-11-04 07:00:00',NULL,NULL),
(205,'243','2024-11-04 08:00:00',NULL,NULL),
(206,'243','2024-11-04 09:00:00',NULL,NULL),
(207,'243','2024-11-10 01:00:00',NULL,NULL),
(208,'243','2024-11-10 02:00:00',NULL,NULL),
(209,'243','2024-11-15 02:00:00',NULL,NULL),
(210,'243','2024-11-15 03:00:00',NULL,NULL),
(211,'243','2024-11-15 05:00:00',NULL,NULL),
(212,'243','2024-11-12 09:00:00',NULL,NULL),
(213,'243','2024-11-12 10:00:00',NULL,NULL),
(214,'243','2024-11-17 09:00:00',NULL,NULL),
(215,'243','2024-11-17 10:00:00',NULL,NULL),
(216,'243','2024-11-11 04:00:00',NULL,NULL),
(217,'243','2024-11-11 03:00:00',NULL,NULL),
(218,'243','2024-10-30 04:00:00',NULL,NULL),
(219,'243','2024-10-30 05:00:00',NULL,NULL),
(220,'243','2024-10-30 07:00:00',NULL,NULL),
(221,'243','2024-11-02 06:00:00',NULL,NULL),
(222,'243','2024-11-02 09:00:00',NULL,NULL),
(223,'243','2024-11-02 10:00:00',245,NULL);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(170,'5c59b766-e283-4585-9a11-187d1d5d7792','2024-10-03 07:13:32'),
(171,'9502db13-704f-4777-a18e-4dde00a4bd7c','2024-10-03 08:00:41'),
(172,'efc81e41-e229-402f-b3b1-681bb0532d1f','2024-10-03 08:02:09'),
(173,'1ac9325c-c2c9-4a52-97bc-643c2f11465a','2024-10-03 08:28:40'),
(174,'c59ff36c-a142-4f6c-a587-e644bb8eb2ac','2024-10-03 08:31:36'),
(175,'926af1e2-e238-4427-b9b4-2cfa8647c9ca','2024-10-03 08:32:10'),
(176,'bdf4362f-4383-482e-a2d3-7842d8343ff4','2024-10-03 08:35:51'),
(177,'18811009-42e7-4cb7-bf5f-4eee9deb92d8','2024-10-03 08:38:32'),
(178,'3349c64d-5bc1-4429-84cc-0879333dc0fe','2024-10-03 08:39:35'),
(179,'4245eee8-536a-4751-843e-01bd4cf00978','2024-10-03 08:39:45'),
(180,'313e3fe8-6782-4ddb-8195-157e8e3d8e9b','2024-10-03 08:40:27'),
(181,'6c32c0ea-9970-4e62-aaa4-487d03e4e9cb','2024-10-03 08:44:14'),
(182,'9353d66f-d9e7-4418-a611-9157cdb562db','2024-10-04 16:15:47'),
(183,'c75ec6a6-c417-437e-8211-5eb2a467b160','2024-10-04 16:16:49'),
(184,'513d9f0e-fff0-417a-88b6-cb0c4d3ccada','2024-10-04 16:17:21'),
(185,'8898f485-222d-471e-b870-b6dba4e0c0cc','2024-10-04 16:18:27'),
(186,'16bfb0be-dcce-4603-8f1e-690a2a98769b','2024-10-04 16:19:08'),
(187,'ed88e6a5-4765-4273-9b21-ab2f03a1b0c9','2024-10-04 16:19:45'),
(188,'b2db4a3c-7ef2-478b-901c-5959d3b4a72f','2024-10-04 16:20:43'),
(189,'d14476e9-9a8f-46eb-9764-47946ee02688','2024-10-04 16:21:28'),
(190,'347f626b-e1ec-4283-afe5-108f58741966','2024-10-04 16:25:06'),
(191,'4ab9e034-f26a-4075-bf9d-90a718d86985','2024-10-04 16:26:32'),
(192,'8756cb28-93f2-4ed6-8201-ac5eea362cdf','2024-10-04 16:27:02'),
(193,'6d3dfb44-0145-4554-a9f7-40bc2017ef9a','2024-10-04 16:27:15'),
(194,'f28b6054-9375-4f40-9da4-60ed0ccb97a9','2024-10-04 16:29:53'),
(195,'c8afaab2-97fd-44a3-9b54-38179e7bdfd5','2024-10-04 16:30:53'),
(196,'f8caf976-e38f-4272-99e4-6d46d2b8d00b','2024-10-04 16:34:16'),
(197,'922acc52-c579-4011-905f-1316b66bf1fc','2024-10-04 16:35:47'),
(198,'6cd4c725-9c5b-4bdf-8edd-26355209078a','2024-10-04 16:37:59'),
(199,'1bcddc63-02e4-46ff-a5c1-79a235b8bac9','2024-10-04 16:38:25'),
(200,'c3075d35-005c-4a0f-8cdf-1cdbeedee68b','2024-10-04 16:39:01'),
(201,'832c8441-fb05-42fd-8ddd-f11a875d2f46','2024-10-04 16:40:30'),
(202,'1d3deebe-648f-4997-95ad-da132a5f3cd3','2024-10-04 16:40:48'),
(203,'fb57031a-d754-4807-ac4d-17e1c1b75a7f','2024-10-04 16:47:44'),
(204,'14af2254-7e42-41ed-adfa-f9cb8489c202','2024-10-04 16:48:20'),
(205,'f968dbf9-7a23-4c16-a0e5-c9ae1cd307f1','2024-10-04 16:49:30'),
(206,'4336a69f-07d1-477e-944c-37188277d732','2024-10-04 16:50:07'),
(207,'7ef4c468-687a-49db-8ddf-878b07b9b73c','2024-10-04 16:55:18'),
(212,'1d4a6779-abe6-42bd-9a25-0819d809e68d','2024-10-04 23:10:00'),
(213,'871533f1-bf9d-4029-a74b-c32a1a4cdc04','2024-10-04 23:13:07'),
(216,'49ec9944-5a2d-4aad-baad-b7fa4b5fd930','2024-10-04 23:17:01'),
(210,'f1bba50a-3547-46b4-9173-44948aedfeae','2024-10-05 12:52:01'),
(220,'c19f00f7-a09b-46cc-afe7-30b7f2d73832','2024-10-05 13:13:04'),
(222,'9fa55755-9fe1-4470-8e89-b2653ffa2145','2024-10-05 13:26:21'),
(223,'bb2dcec3-deb7-46b5-acc5-398f1cc739b8','2024-10-06 14:39:33'),
(225,'7bf51794-87ae-413c-a472-06d3fcb650bf','2024-10-06 15:31:11'),
(154,'25aee449-4e74-4e7b-b2cd-795274e1a1c1','2024-10-09 16:18:57'),
(227,'e298e963-c005-4c39-bc89-690bfbb526a9','2024-10-15 23:10:33'),
(228,'165a49f7-5fce-4610-8ed4-03f8b7feb0af','2024-10-21 09:15:17'),
(229,'95453d5f-42f4-48b8-8d60-da9ebee7f2c0','2024-10-21 09:28:11'),
(230,'6f8331ac-768e-4749-a104-5d794a681533','2024-10-21 10:15:17'),
(230,'ad33184a-9278-4faf-a9f4-5e312b21ad8b','2024-10-21 10:40:31'),
(230,'4c4ea05f-64ab-4cfd-a456-af3c47aa5de0','2024-10-21 10:58:02'),
(230,'02e7ba35-3976-4e48-9907-4c27c96b7cef','2024-10-21 10:58:23'),
(230,'badb49f2-9807-43ed-9172-ee07cac7840f','2024-10-21 10:58:40'),
(230,'0383d922-9088-453b-a770-35b2d5a88895','2024-10-21 11:04:49'),
(230,'0a11c6dd-317e-4822-9a83-d2d300bf6ca1','2024-10-21 11:05:17'),
(230,'c023ec66-cb34-4294-847a-83075d097c78','2024-10-21 11:05:58'),
(230,'688a1529-9e79-48da-8613-ad2aad03d781','2024-10-21 11:06:45'),
(230,'4017e3bc-cbb1-4dbb-a4e3-33db878e99d3','2024-10-21 11:07:08'),
(230,'f6aee144-9007-44f3-90e5-31bf5e202371','2024-10-21 11:09:01'),
(230,'12efa41b-f44d-4ed2-b4d1-e6358b2f2659','2024-10-21 11:18:41'),
(230,'4979988e-9939-4c0f-8cd3-dc6e8329d759','2024-10-21 11:25:07'),
(230,'324c62da-a651-4fea-aca3-e266406003a7','2024-10-21 11:26:27'),
(230,'76f8dc54-f677-423b-94fe-05838de4e53f','2024-10-21 11:29:34'),
(230,'dbbcc4e3-25c6-464f-84be-dc993e58e1c1','2024-10-21 11:30:59'),
(230,'9300375d-50ec-48b1-97b0-b0c110541e54','2024-10-21 11:31:29'),
(230,'007bbbf6-e5c4-4cae-b464-b541a0bfe14f','2024-10-21 11:31:54'),
(230,'07057348-199e-4d2f-bc6e-ef6110685a79','2024-10-21 11:34:44'),
(231,'960ba00f-dc8d-4da3-8f7c-9669061b8622','2024-10-21 11:58:42'),
(231,'79e136e7-3958-4597-a912-5e14430edd56','2024-10-21 12:08:57'),
(230,'f2bbfffb-7886-4181-9df1-fc70606c5eeb','2024-10-21 12:09:14'),
(230,'f745f0fd-c6da-4308-981f-6f349053a5ee','2024-10-21 12:10:27'),
(232,'ad119144-7184-47a7-9236-60bbd9e5ce1e','2024-10-21 12:11:43'),
(233,'8dd5e2e3-939b-48f1-90ad-e1ed1f9b2083','2024-10-21 12:13:29'),
(233,'fbb65d4d-3d15-4dd2-97df-25715d17d6a5','2024-10-21 12:14:43'),
(233,'a383e71f-fa5b-4c36-a13d-2eb2ed1b43eb','2024-10-21 12:15:14'),
(233,'c202856d-8b15-4586-86ef-4482395d8691','2024-10-21 12:15:24'),
(233,'4f0962df-50c8-4d69-afed-feb2ae78136a','2024-10-21 12:16:10'),
(233,'69b32dc5-43e1-4234-9a73-725755fe92a9','2024-10-21 12:17:14'),
(233,'69c0ca77-1519-4bf4-9d4e-1e8608b4cc25','2024-10-21 12:17:58'),
(233,'7dfb86c6-9ef8-4134-a533-4b9f548c65c8','2024-10-21 12:18:27'),
(233,'36c6f84a-e9a4-4e6c-b399-8a4df866ace0','2024-10-21 12:19:12'),
(230,'f394d6a1-2123-4bc5-b004-bb5410dfe740','2024-10-21 12:19:58'),
(233,'73f8a138-0aef-4f7a-8fb2-7badf51eb16f','2024-10-21 12:20:08'),
(233,'5048b8c1-dea4-4cfc-a0ab-0774bd50a9f9','2024-10-21 12:21:51'),
(230,'ac941e82-be32-4955-86a2-c10517cdf827','2024-10-21 12:24:17'),
(233,'eca44d1d-3cd2-495a-b876-11dcbce83d96','2024-10-21 12:24:29'),
(230,'4bc78534-4f91-47a8-81b6-cc824108d6e2','2024-10-21 12:27:07'),
(233,'24220317-5d12-4ce8-bdb7-7e20a4d68a9e','2024-10-21 12:27:15'),
(233,'d75f34e7-d1c0-41e9-8ae8-a0ab3d12f304','2024-10-21 12:27:34'),
(230,'a66fd3fb-bc67-4f09-a505-27af9bab2b3b','2024-10-21 12:29:29'),
(233,'75c847cf-5a20-4588-82b5-1e3cd833152a','2024-10-21 12:29:40'),
(233,'ea904b1b-9325-43b3-8dfd-984508fe7e83','2024-10-21 12:30:41'),
(230,'93ae8232-f02f-47ce-95f6-cde187a5885a','2024-10-21 12:32:11'),
(233,'0ad4a13c-27f5-41a6-8897-3aa4f6898eaf','2024-10-21 12:32:23'),
(230,'a28d70ad-9beb-49c1-a86a-d6a557431a54','2024-10-21 12:35:40'),
(233,'f7e0aa9a-aace-4cea-8ebb-cbe8935bc7ad','2024-10-21 12:35:51'),
(230,'ddda5df3-1f83-4a15-8d2c-b0ba8e10866a','2024-10-21 12:36:09'),
(233,'fe7db4ae-5594-42d7-9ad7-ac2c52f079f7','2024-10-21 12:36:17'),
(230,'4ef9b4b5-860a-4901-b613-23097f6f746f','2024-10-21 12:43:47'),
(234,'0ebfffeb-fcd6-4ab3-a510-1a890509d265','2024-10-21 12:44:52'),
(230,'9c245596-a707-403d-92e8-45d430dd0697','2024-10-21 12:50:29'),
(233,'4057655a-b39f-425d-a80f-1396c96c1019','2024-10-21 12:50:42'),
(235,'f594b402-abb6-457d-b203-2073558fc220','2024-10-21 12:51:41'),
(236,'2148372c-c024-4f72-92b3-df36bf19120c','2024-10-21 12:52:48'),
(237,'10f2546f-f500-4499-b107-7a80b19bf68f','2024-10-21 12:53:52'),
(230,'ff66535d-0fed-436c-83af-bbfe55da1cb3','2024-10-21 12:59:33'),
(233,'4fdb19e7-a705-4bd0-bedb-f7e8957759fd','2024-10-21 13:01:32'),
(233,'5036ec2a-89c6-47e0-944f-5a9124bcad44','2024-10-21 13:04:24'),
(238,'3b22874a-9379-4f54-ad0f-b663ea69b004','2024-10-21 13:05:47'),
(233,'febaa196-2af8-487d-a2d2-12b8ce1eefb3','2024-10-21 13:14:30'),
(239,'92651b8f-7626-4e68-9e03-8d4021abeb8b','2024-10-21 13:34:25'),
(240,'9a9111ff-d5d2-46c0-818d-909445ab9717','2024-10-21 13:37:50'),
(239,'442b9aa1-6d2d-40fd-ad12-1f7c5ad3e18a','2024-10-21 13:38:24'),
(241,'c043cae0-40aa-4aa9-8f25-af7c12e4c2e2','2024-10-21 13:40:21'),
(242,'16c1deee-a653-4f73-b208-413c29aa49cd','2024-10-21 13:40:21'),
(243,'3cf5f681-b4d5-4300-a3d2-9911dd42bd0f','2024-10-21 13:43:46'),
(244,'5a10aaf0-462c-4401-9ddf-e0990574b5cc','2024-10-21 13:47:39'),
(239,'22b636b6-e0b5-45c2-be1c-1fd9931265c2','2024-10-21 14:18:03'),
(242,'0b879f99-d6f8-46e2-8971-c1b27cdde4f2','2024-10-21 14:18:22'),
(243,'9ea00516-4ea9-4994-ae97-07fa5a2c0ee7','2024-10-21 14:18:40'),
(233,'957d17b4-229e-49e7-afbe-2ebccf9a2e23','2024-10-21 14:18:56'),
(244,'c7ec0d83-fc0c-4f8e-9fed-8a4b22cf8338','2024-10-21 14:19:15'),
(245,'119ffe5f-9657-442e-a284-143339e6171c','2024-10-21 14:19:47');
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
) ENGINE=InnoDB AUTO_INCREMENT=246 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(154,'test@test.ru','R9a0w0M3',0,1,'2024-09-30 00:00:00'),
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
(169,'test21@test.ts','t6h5k7z7',1,0,'2024-10-03 00:00:00'),
(170,'0-string112','U0X1c3j5',1,0,'2024-10-03 07:13:32'),
(171,'test-doc-222@test.ru','H2J8C2e2',1,0,'2024-10-03 08:00:41'),
(172,'test-doc-22@test.ru','x0U2m7F5',1,0,'2024-10-03 08:02:09'),
(173,'samuel@docs.com','E5o5u3R1',1,0,'2024-10-03 08:28:40'),
(174,'samuedl@docs.com','w9d9f9W9',1,0,'2024-10-03 08:31:36'),
(175,'sasmuedl@docs.com','m6l4M5Z5',1,0,'2024-10-03 08:32:10'),
(176,'sasmueыdl@docs.com','q7c4X3g7',1,0,'2024-10-03 08:35:51'),
(177,'sassmueыdl@docs.com','J1U6u4X5',1,0,'2024-10-03 08:38:32'),
(178,'sassmuseыdl@docs.com','B6U8Y1s6',1,0,'2024-10-03 08:39:35'),
(179,'sasssmuseыdl@docs.com','R7N9Z1b9',1,0,'2024-10-03 08:39:44'),
(180,'sassssmuseыdl@docs.com','X3K8q0D5',1,0,'2024-10-03 08:40:27'),
(181,'sasssdsmuseыdl@docs.com','P8b4H5c6',1,0,'2024-10-03 08:44:14'),
(182,'s1','j5g8l9k8',1,0,'2024-10-04 16:15:47'),
(183,'s2','J9q3O8k3',1,0,'2024-10-04 16:16:49'),
(184,'s3','T3q8b4I3',1,0,'2024-10-04 16:17:21'),
(185,'s4','p8L7m5M3',1,0,'2024-10-04 16:18:27'),
(186,'s5','X5R7U1P0',1,0,'2024-10-04 16:19:08'),
(187,'5s','m9b6E4q7',1,0,'2024-10-04 16:19:45'),
(188,'51s','W1d3X5a1',1,0,'2024-10-04 16:20:43'),
(189,'52s','S3n6P5O7',1,0,'2024-10-04 16:21:28'),
(190,'53s','j8s4u9c1',1,0,'2024-10-04 16:25:06'),
(191,'54s','y6O7X2a6',1,0,'2024-10-04 16:26:32'),
(192,'541s','L7Y8O4k6',1,0,'2024-10-04 16:27:02'),
(193,'5141s','J6P7H0a5',1,0,'2024-10-04 16:27:15'),
(194,'51411s','Y4a1I1d2',1,0,'2024-10-04 16:29:53'),
(195,'514s11s','j2k9o2X2',1,0,'2024-10-04 16:30:53'),
(196,'51s4s11s','G0b8G3a9',1,0,'2024-10-04 16:34:16'),
(197,'51s4ss11s','k8b3l2m9',1,0,'2024-10-04 16:35:47'),
(198,'51s4ss1s1s','a8z5B3g0',1,0,'2024-10-04 16:37:59'),
(199,'51s4sss1s1s','e2t8H2s7',1,0,'2024-10-04 16:38:25'),
(200,'51s4sss1ss1s','u8Z7e5t7',1,0,'2024-10-04 16:39:00'),
(201,'51s4ssss1ss1s','S3R0k0I7',1,0,'2024-10-04 16:40:30'),
(202,'51s4sssss1ss1s','F5I0T8k1',1,0,'2024-10-04 16:40:48'),
(203,'51s4ssssss1ss1s','j0P7U9A7',1,0,'2024-10-04 16:47:44'),
(204,'51s4sssssss1ss1s','o2M9O1b5',1,0,'2024-10-04 16:48:20'),
(205,'51s4sssssss1sfs1s','s3T7H6j1',1,0,'2024-10-04 16:49:30'),
(206,'51s4ssssssss1sfs1s','t4V3S3Z1',1,0,'2024-10-04 16:50:07'),
(207,'51s4sssыsssss1sfs1s','Z6c9P2i3',1,0,'2024-10-04 16:55:18'),
(208,'user@example.com','stringstr',0,0,'2024-10-04 17:33:07'),
(210,'user@enxam1ple.com','stringstr',0,0,'2024-10-04 17:40:15'),
(211,'a@a.a','*********',0,0,'2024-10-04 22:37:52'),
(212,'string','d3u9y1Q8',1,0,'2024-10-04 23:10:00'),
(213,'1','N1R6H8Y7',1,0,'2024-10-04 23:13:07'),
(216,'1f','R0I5L8A2',1,0,'2024-10-04 23:17:01'),
(220,'stddring','K4f2o9u9',1,0,'2024-10-05 13:13:04'),
(222,'stddrfаing','A6z9i0U5',1,0,'2024-10-05 13:26:21'),
(223,'stringgggg','M5t4X4o2',1,0,'2024-10-06 14:39:33'),
(225,'stringggggg','n0C6V1z0',1,0,'2024-10-06 15:31:11'),
(227,'kksdfnsffkjf@jskdjfsdf.fd','W8y4X0R5',1,0,'2024-10-15 23:10:33'),
(228,'test989@test.ru','1234567890',0,0,'2024-10-21 09:15:17'),
(229,'vasya11@test.ru','1234567890',0,0,'2024-10-21 09:28:11'),
(230,'vasyan123@test.ru','1234567890',0,0,'2024-10-21 10:15:17'),
(231,'test-doc@test111.ru','H0D4Z0C9',1,0,'2024-10-21 11:58:42'),
(232,'ivan@test111.ru','1234567890',0,0,'2024-10-21 12:11:43'),
(233,'ivan1@test111.ru','1234567890',0,0,'2024-10-21 12:13:29'),
(234,'mila123@test.ru','12345',0,0,'2024-10-21 12:44:52'),
(235,'mila55@test.ru','1234567890',0,0,'2024-10-21 12:51:41'),
(236,'mila545@test.ru','1234567890',0,0,'2024-10-21 12:52:48'),
(237,'mila1234@test.ru','1234567890',0,0,'2024-10-21 12:53:52'),
(238,'mila12346@test.ru','1234567890',0,0,'2024-10-21 13:05:47'),
(239,'ivanov.ivan@test.ru','e8r0Y2c4',1,0,'2024-10-21 13:34:25'),
(240,'','a3y0S2u0',1,0,'2024-10-21 13:37:50'),
(241,'vasili.vasilyev@test.ru','j5W9G1W1',1,0,'2024-10-21 13:40:21'),
(242,'vasili.vasilyev@test.ru','D2V4E7z9',1,0,'2024-10-21 13:40:21'),
(243,'anna.sidorova@test.ru','L5X0f9I1',1,0,'2024-10-21 13:43:46'),
(244,'ivan123@test.ru','12345',0,0,'2024-10-21 13:47:39'),
(245,'mila@test1234.ru','12345',0,0,'2024-10-21 14:19:47');
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

-- Dump completed on 2024-10-21 16:44:12
