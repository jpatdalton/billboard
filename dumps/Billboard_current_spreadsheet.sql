-- MySQL dump 10.13  Distrib 5.6.19, for osx10.7 (i386)
--
-- Host: billboard.cehafzitzdxd.us-west-2.rds.amazonaws.com    Database: Billboard
-- ------------------------------------------------------
-- Server version	5.6.22-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `current_spreadsheet`
--

DROP TABLE IF EXISTS `current_spreadsheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `current_spreadsheet` (
  `track_id` int(11) DEFAULT NULL,
  `indice` int(11) DEFAULT NULL,
  KEY `track_id` (`track_id`),
  CONSTRAINT `current_spreadsheet_ibfk_1` FOREIGN KEY (`track_id`) REFERENCES `track` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `current_spreadsheet`
--

LOCK TABLES `current_spreadsheet` WRITE;
/*!40000 ALTER TABLE `current_spreadsheet` DISABLE KEYS */;
INSERT INTO `current_spreadsheet` VALUES (401,0),(311,1),(456,2),(315,3),(322,4),(302,7),(325,9),(301,10),(303,12),(431,13),(321,15),(319,16),(416,19),(304,21),(318,22),(306,24),(424,26),(309,28),(342,29),(425,30),(457,31),(308,32),(316,36),(362,39),(305,41),(354,42),(310,43),(410,44),(330,46),(320,47),(385,48),(307,49),(324,50),(445,51),(449,52),(317,54),(341,55),(458,56),(312,60),(314,61),(367,63),(378,64),(419,65),(375,68),(335,69),(313,70),(418,71),(381,74),(327,75),(403,76),(364,77),(405,78),(394,79),(388,80),(345,82),(387,84),(426,85),(390,87),(406,88),(370,89),(399,90),(366,91),(350,92),(459,94),(436,96),(460,98),(441,99),(437,100),(446,101),(339,103),(429,104),(408,107),(336,108),(411,109),(383,111),(443,113),(442,114),(461,115),(452,116),(455,117),(439,118),(369,119),(421,120),(361,121),(438,122),(357,123),(451,124),(377,125),(447,129),(462,131),(463,133),(427,134),(323,135),(464,136),(465,137),(444,138),(379,141),(373,142),(466,144),(415,145);
/*!40000 ALTER TABLE `current_spreadsheet` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-09-02 22:46:13
