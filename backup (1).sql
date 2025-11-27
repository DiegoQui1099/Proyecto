-- MySQL dump 10.13  Distrib 8.0.29, for Linux (x86_64)
--
-- Host: Diego10.mysql.pythonanywhere-services.com    Database: Diego10$default
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `idAdmin` int unsigned NOT NULL AUTO_INCREMENT,
  `nomAdmin` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `idUsuario` int unsigned NOT NULL,
  PRIMARY KEY (`idAdmin`),
  UNIQUE KEY `nomAdmin` (`nomAdmin`,`idUsuario`),
  KEY `idUsuario` (`idUsuario`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idUsuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'Juan Mendoza',1);
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cargo`
--

DROP TABLE IF EXISTS `cargo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cargo` (
  `idCargo` int unsigned NOT NULL AUTO_INCREMENT,
  `nomCargo` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`idCargo`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cargo`
--

LOCK TABLES `cargo` WRITE;
/*!40000 ALTER TABLE `cargo` DISABLE KEYS */;
INSERT INTO `cargo` VALUES (1,'Constructor'),(2,'Topografo Principal'),(3,'Topógrafo de Campo'),(4,'Asistente de Topografía'),(5,'Dibujante Topográfico'),(6,'Ingeniero Topográfico'),(7,'Supervisor de Campo');
/*!40000 ALTER TABLE `cargo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certificados`
--

DROP TABLE IF EXISTS `certificados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certificados` (
  `idCertificados` int unsigned NOT NULL AUTO_INCREMENT,
  `idEmpleado` int unsigned NOT NULL,
  `estado_cert` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `num_certificado` int DEFAULT NULL,
  PRIMARY KEY (`idCertificados`),
  KEY `idEmpleado` (`idEmpleado`),
  CONSTRAINT `certificados_ibfk_1` FOREIGN KEY (`idEmpleado`) REFERENCES `empleados` (`idEmpleado`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificados`
--

LOCK TABLES `certificados` WRITE;
/*!40000 ALTER TABLE `certificados` DISABLE KEYS */;
INSERT INTO `certificados` VALUES (7,2,'Inactivo',2);
/*!40000 ALTER TABLE `certificados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ciudad`
--

DROP TABLE IF EXISTS `ciudad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ciudad` (
  `idCiudad` int unsigned NOT NULL AUTO_INCREMENT,
  `nomCiudad` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`idCiudad`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ciudad`
--

LOCK TABLES `ciudad` WRITE;
/*!40000 ALTER TABLE `ciudad` DISABLE KEYS */;
INSERT INTO `ciudad` VALUES (1,'Bogotá'),(2,'Medellín'),(3,'Cali'),(4,'Barranquilla'),(5,'Cartagena'),(6,'Bucaramanga'),(7,'Pereira'),(8,'Manizales'),(9,'Armenia'),(10,'Santa Marta'),(11,'Cúcuta'),(12,'Ibagué'),(13,'Villavicencio'),(14,'Pasto'),(15,'Montería');
/*!40000 ALTER TABLE `ciudad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `idCliente` int unsigned NOT NULL AUTO_INCREMENT,
  `nombreCliente` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `apeCliente` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `telefono` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `idUsuario` int unsigned DEFAULT NULL,
  PRIMARY KEY (`idCliente`),
  KEY `idUsuario` (`idUsuario`),
  CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idUsuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (8,'Diego Alexander ','Quiñones Sanabria','3016636500',5),(9,'Edwin Santiago ','Fajardo Baron','1234567898',6),(10,'Natalia','Avila Avila','3194406753',41),(11,'Pedro ','Quiñones','3213246546',43);
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contempleado`
--

DROP TABLE IF EXISTS `contempleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contempleado` (
  `idContratoE` int unsigned NOT NULL AUTO_INCREMENT,
  `banco` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fechaI` date DEFAULT NULL,
  `fechaF` date DEFAULT NULL,
  `salario` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tipoContrato` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tipoCuenta` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `idAdmin` int unsigned NOT NULL,
  `idEmpleado` int unsigned NOT NULL,
  PRIMARY KEY (`idContratoE`),
  KEY `idEmpleado` (`idEmpleado`),
  KEY `idAdmin` (`idAdmin`),
  CONSTRAINT `contempleado_ibfk_1` FOREIGN KEY (`idAdmin`) REFERENCES `admin` (`idAdmin`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `contempleado_ibfk_2` FOREIGN KEY (`idEmpleado`) REFERENCES `empleados` (`idEmpleado`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contempleado`
--

LOCK TABLES `contempleado` WRITE;
/*!40000 ALTER TABLE `contempleado` DISABLE KEYS */;
INSERT INTO `contempleado` VALUES (5,'BBVA','2024-06-11','2025-06-11','2.000.000','Termino indefinido','Ahorros',1,2),(6,'Bancolombiaa','2024-06-26','2024-07-01','1.800.000','Termino indefinido','Ahorros',1,11);
/*!40000 ALTER TABLE `contempleado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contproyecto`
--

DROP TABLE IF EXISTS `contproyecto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contproyecto` (
  `idContratoP` int unsigned NOT NULL AUTO_INCREMENT,
  `fechaI` date DEFAULT NULL,
  `fechaF` date DEFAULT NULL,
  `precio` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `idAdmin` int unsigned NOT NULL,
  `idCliente` int unsigned NOT NULL,
  `idEmpleado` int unsigned NOT NULL,
  `idCiudad` int unsigned NOT NULL,
  `idProyecto` int unsigned NOT NULL,
  PRIMARY KEY (`idContratoP`),
  KEY `idAdmin` (`idAdmin`),
  KEY `idCliente` (`idCliente`),
  KEY `idEmpleado` (`idEmpleado`),
  KEY `idCiudad` (`idCiudad`),
  KEY `idProyecto` (`idProyecto`),
  CONSTRAINT `contproyecto_ibfk_1` FOREIGN KEY (`idEmpleado`) REFERENCES `empleados` (`idEmpleado`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `contproyecto_ibfk_3` FOREIGN KEY (`idCiudad`) REFERENCES `ciudad` (`idCiudad`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `contproyecto_ibfk_4` FOREIGN KEY (`idCliente`) REFERENCES `clientes` (`idCliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `contproyecto_ibfk_5` FOREIGN KEY (`idAdmin`) REFERENCES `admin` (`idAdmin`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `contproyecto_ibfk_6` FOREIGN KEY (`idProyecto`) REFERENCES `proyectos` (`idProyecto`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contproyecto`
--

LOCK TABLES `contproyecto` WRITE;
/*!40000 ALTER TABLE `contproyecto` DISABLE KEYS */;
INSERT INTO `contproyecto` VALUES (6,'2024-06-23','2024-06-24','20000',1,11,2,1,5),(7,'2024-06-23','2024-06-30','50000',1,11,11,4,1),(8,'2024-06-24','2024-07-05','60000',1,8,13,6,9);
/*!40000 ALTER TABLE `contproyecto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleados`
--

DROP TABLE IF EXISTS `empleados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleados` (
  `idEmpleado` int unsigned NOT NULL AUTO_INCREMENT,
  `idUsuario` int unsigned NOT NULL,
  `nomEmpleado` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `apeEmpleado` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `edad` int DEFAULT NULL,
  `documento` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `telefono` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `idEps` int unsigned NOT NULL,
  `idCargo` int unsigned NOT NULL,
  PRIMARY KEY (`idEmpleado`),
  UNIQUE KEY `documento` (`documento`),
  KEY `idUsuario` (`idUsuario`),
  KEY `idEps` (`idEps`),
  KEY `idCargo` (`idCargo`),
  CONSTRAINT `empleados_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idUsuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `empleados_ibfk_2` FOREIGN KEY (`idCargo`) REFERENCES `cargo` (`idCargo`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `empleados_ibfk_3` FOREIGN KEY (`idEps`) REFERENCES `eps` (`idEps`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleados`
--

LOCK TABLES `empleados` WRITE;
/*!40000 ALTER TABLE `empleados` DISABLE KEYS */;
INSERT INTO `empleados` VALUES (2,2,'Alexander','Quiñones',21,'1012654823','3222354944',1,1),(6,3,'Loren Mariana','Zualaga Romboy',19,'12321445','3105321468',1,2),(11,42,'patricia','cuervo',40,'56784269','3106548213',3,1),(12,44,'asadfadsf','jejejejeje',19,'1234445226','1252452625365',3,3),(13,45,'Diego Alexander','Quiñones Sanabria',60,'1013691636','013016636500',1,7);
/*!40000 ALTER TABLE `empleados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eps`
--

DROP TABLE IF EXISTS `eps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eps` (
  `idEps` int unsigned NOT NULL AUTO_INCREMENT,
  `nomEps` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`idEps`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eps`
--

LOCK TABLES `eps` WRITE;
/*!40000 ALTER TABLE `eps` DISABLE KEYS */;
INSERT INTO `eps` VALUES (1,'Famisanar'),(2,'Sura'),(3,'Sanitas '),(4,'Nueva EPS'),(5,'Compensar '),(6,'Coomeva '),(7,'Salud Total'),(8,'EPS Medimás'),(9,'EPS Mutual Ser'),(10,'Salud Total'),(11,'Aliansalud');
/*!40000 ALTER TABLE `eps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incapacidades`
--

DROP TABLE IF EXISTS `incapacidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `incapacidades` (
  `idIncapacidad` int unsigned NOT NULL AUTO_INCREMENT,
  `idEmpleado` int unsigned NOT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `numIncapacidad` int DEFAULT NULL,
  `duracion` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`idIncapacidad`),
  KEY `idEmpleado` (`idEmpleado`),
  CONSTRAINT `incapacidades_ibfk_1` FOREIGN KEY (`idEmpleado`) REFERENCES `empleados` (`idEmpleado`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incapacidades`
--

LOCK TABLES `incapacidades` WRITE;
/*!40000 ALTER TABLE `incapacidades` DISABLE KEYS */;
INSERT INTO `incapacidades` VALUES (3,2,'2024-06-11','2024-06-30',1,'19 dias');
/*!40000 ALTER TABLE `incapacidades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permisos`
--

DROP TABLE IF EXISTS `permisos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permisos` (
  `idPermisos` int unsigned NOT NULL AUTO_INCREMENT,
  `idEmpleado` int unsigned NOT NULL,
  `duracion` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `numPermiso` int DEFAULT NULL,
  `fechaInicio` date DEFAULT NULL,
  `fechaFin` date DEFAULT NULL,
  PRIMARY KEY (`idPermisos`),
  KEY `idEmpleado` (`idEmpleado`),
  CONSTRAINT `permisos_ibfk_1` FOREIGN KEY (`idEmpleado`) REFERENCES `empleados` (`idEmpleado`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permisos`
--

LOCK TABLES `permisos` WRITE;
/*!40000 ALTER TABLE `permisos` DISABLE KEYS */;
INSERT INTO `permisos` VALUES (3,2,'5 días',1,'2024-06-01','2024-06-05');
/*!40000 ALTER TABLE `permisos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proyectos`
--

DROP TABLE IF EXISTS `proyectos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proyectos` (
  `idProyecto` int unsigned NOT NULL AUTO_INCREMENT,
  `nomProyecto` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`idProyecto`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proyectos`
--

LOCK TABLES `proyectos` WRITE;
/*!40000 ALTER TABLE `proyectos` DISABLE KEYS */;
INSERT INTO `proyectos` VALUES (1,'Placa Huella'),(2,'Tunel'),(3,'Cartografía y GIS'),(4,'Estudios Geodésicos'),(5,'Estudios de Infraestructura y Vías'),(6,'Proyectos Mineros y de Exploración'),(7,'Proyectos de Energía'),(8,'Levantamientos Agrícolas y Forestale'),(9,'Estudios de Impacto Ambiental'),(10,'Proyectos de Desarrollo Inmobiliario'),(11,'Proyectos de Conservación y Restauración');
/*!40000 ALTER TABLE `proyectos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `idRol` int unsigned NOT NULL AUTO_INCREMENT,
  `Nombre_rol` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`idRol`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Empleado'),(2,'Cliente');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solicitudese`
--

DROP TABLE IF EXISTS `solicitudese`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solicitudese` (
  `idSolicitud` int unsigned NOT NULL AUTO_INCREMENT,
  `tipoSolicitud` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `motivo` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `fechaSolicitud` date NOT NULL,
  `estado` enum('pendiente','aceptado','rechazado') COLLATE utf8mb4_general_ci DEFAULT 'pendiente',
  `fechaRespuesta` date DEFAULT NULL,
  `respuesta` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `idEmpleado` int unsigned NOT NULL,
  PRIMARY KEY (`idSolicitud`),
  KEY `idEmpleado` (`idEmpleado`),
  CONSTRAINT `solicitudese_ibfk_1` FOREIGN KEY (`idEmpleado`) REFERENCES `empleados` (`idEmpleado`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitudese`
--

LOCK TABLES `solicitudese` WRITE;
/*!40000 ALTER TABLE `solicitudese` DISABLE KEYS */;
INSERT INTO `solicitudese` VALUES (9,'Incapacidad','dasgdfgfadhadf','2024-06-23','aceptado','2024-06-23','Su solicitud A sido aceptada y se registrara su incapacidad, gracias te quiero',2),(10,'Permiso','lele pancha','2024-06-24','rechazado','2024-06-23','Sea seria',11),(11,'Permiso','lele pancha','2024-06-24','aceptado','2024-06-24','si',11),(12,'Incapacidad','Cita Medica','2024-06-24','pendiente',NULL,NULL,11),(13,'Incapacidad','motivo por el cual se solicita \r\n\r\nde tal fecha a tal fecha','2024-06-26','pendiente',NULL,NULL,11);
/*!40000 ALTER TABLE `solicitudese` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solicitudesp`
--

DROP TABLE IF EXISTS `solicitudesp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solicitudesp` (
  `idSolicitud` int unsigned NOT NULL AUTO_INCREMENT,
  `desc_solicitud` text COLLATE utf8mb4_general_ci,
  `Estado` enum('pendiente','aceptado') COLLATE utf8mb4_general_ci DEFAULT 'pendiente',
  `idCliente` int unsigned NOT NULL,
  `idProyecto` int unsigned NOT NULL,
  PRIMARY KEY (`idSolicitud`),
  KEY `idCliente` (`idCliente`),
  KEY `idProyecto` (`idProyecto`),
  CONSTRAINT `solicitudesp_ibfk_1` FOREIGN KEY (`idCliente`) REFERENCES `clientes` (`idCliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `solicitudesp_ibfk_2` FOREIGN KEY (`idProyecto`) REFERENCES `proyectos` (`idProyecto`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitudesp`
--

LOCK TABLES `solicitudesp` WRITE;
/*!40000 ALTER TABLE `solicitudesp` DISABLE KEYS */;
INSERT INTO `solicitudesp` VALUES (53,'que vsj ','aceptado',8,2),(54,'safdadsgasd','aceptado',8,1),(55,'ayudasdasf','pendiente',9,1),(56,'hola jeje','pendiente',10,10),(57,'hola mundo jeje ','pendiente',8,11),(58,'quiero uno jeje ','aceptado',11,5),(59,'ayuda que paso ','aceptado',11,1),(60,'si pude','aceptado',8,9);
/*!40000 ALTER TABLE `solicitudesp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `idUsuario` int unsigned NOT NULL AUTO_INCREMENT,
  `correo` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `contraseña` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Nombre_Usuario` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `idRol` int unsigned DEFAULT NULL,
  PRIMARY KEY (`idUsuario`),
  UNIQUE KEY `Nombre_Usuario` (`Nombre_Usuario`),
  UNIQUE KEY `correo` (`correo`),
  KEY `idRol` (`idRol`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`idRol`) REFERENCES `roles` (`idRol`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Jp_mendoza17@gmail.com','JuanPmendoza1*','Admin',NULL),(2,'diegosantafe1999@hotmail.com','diego123.','diegoQuiñones10 ',1),(3,'mm6542597@gmail.com','LoremZuluaga','LoremZ1',1),(4,'MairaRechtp1@gmail.com','Maria01.@','MariaRH1',NULL),(5,'diegodarkar123@hotmail.com','Diego2501.@','DiegoQui10',2),(6,'esantifb11@gmail.com','Batman2121*','Fafas21',2),(41,'avilaavilanatalia5@gmail.com','natalia123*','Natis12',2),(42,'patriciacc2074@gmail.com','patricia321*','Patricia10',1),(43,'pedropquinones@gmail.com','salo1211*','PedroP1',2),(44,'asdasda@gmail.com','Diego123*','afadsf12',1),(45,'diegosantafe1501@gmail.com','Samorgap123*','DiegoQui20',1);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-27 17:08:35
