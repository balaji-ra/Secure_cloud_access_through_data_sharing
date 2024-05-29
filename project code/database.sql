/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.1.13-MariaDB : Database - verifiableandfair
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`verifiableandfair` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `verifiableandfair`;

/*Table structure for table `dataowner` */

DROP TABLE IF EXISTS `dataowner`;

CREATE TABLE `dataowner` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `doname` varchar(200) DEFAULT NULL,
  `doemail` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `contact` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `profile` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `dataowner` */

insert  into `dataowner`(`id`,`doname`,`doemail`,`password`,`contact`,`address`,`profile`,`status`) values (1,'preeti','preeti@gmail.com','Preeti@123','9652145698','tpt','static/profiles/istockphoto-1035399856-612x612.jpg','accepted');

/*Table structure for table `filesupload` */

DROP TABLE IF EXISTS `filesupload`;

CREATE TABLE `filesupload` (
  `id` int(200) NOT NULL AUTO_INCREMENT,
  `doemail` varchar(200) DEFAULT NULL,
  `FileName` varchar(200) DEFAULT NULL,
  `Keywords` varchar(200) DEFAULT NULL,
  `Files` varchar(200) DEFAULT NULL,
  `AccessPilicy` varchar(200) DEFAULT NULL,
  `Date` varchar(200) DEFAULT NULL,
  `Time` varchar(200) DEFAULT NULL,
  `Attack` varchar(200) DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `filesupload` */

insert  into `filesupload`(`id`,`doemail`,`FileName`,`Keywords`,`Files`,`AccessPilicy`,`Date`,`Time`,`Attack`) values (1,'preeti@gmail.com','file','key123','òX1üK(¯?àÆéW–ëSóÉØ.A–G»Ñyþº›½>_|Å|LÏáôºÏŸ$¾','Download','2024-03-04','17:15:55','pending');

/*Table structure for table `recipients` */

DROP TABLE IF EXISTS `recipients`;

CREATE TABLE `recipients` (
  `ID` int(20) NOT NULL AUTO_INCREMENT,
  `rename` varchar(200) DEFAULT NULL,
  `reemail` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `contact` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `profile` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT 'pending',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `recipients` */

insert  into `recipients`(`ID`,`rename`,`reemail`,`password`,`contact`,`address`,`profile`,`status`) values (1,'nakku','nakku@gmail.com','Nakku@123','6363379953','tpt','static/profiles/istockphoto-1035399856-612x612.jpg','accepted'),(2,'ram','ram@gmail.com','Ram@1234','6363379953','tpt','static/profiles/istockphoto-1015350750-612x612.jpg','accepted');

/*Table structure for table `recipientsharefile` */

DROP TABLE IF EXISTS `recipientsharefile`;

CREATE TABLE `recipientsharefile` (
  `ID` int(20) NOT NULL AUTO_INCREMENT,
  `doemail` varchar(200) DEFAULT NULL,
  `FileName` varchar(200) DEFAULT NULL,
  `reemail` varchar(200) DEFAULT NULL,
  `sharedrecipient` varchar(200) DEFAULT NULL,
  `Files` varchar(200) DEFAULT NULL,
  `otp` varchar(200) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `recipientsharefile` */

/*Table structure for table `sharefile` */

DROP TABLE IF EXISTS `sharefile`;

CREATE TABLE `sharefile` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `doemail` varchar(200) DEFAULT NULL,
  `RecipintId` varchar(200) DEFAULT NULL,
  `FileName` varchar(200) DEFAULT NULL,
  `AccessPilicy` varchar(200) DEFAULT NULL,
  `reemail` varchar(200) DEFAULT NULL,
  `Files` varchar(200) DEFAULT NULL,
  `otp` varchar(200) DEFAULT NULL,
  `Date` varchar(200) DEFAULT NULL,
  `Time` varchar(200) DEFAULT NULL,
  `Status` varchar(200) DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `sharefile` */

insert  into `sharefile`(`id`,`doemail`,`RecipintId`,`FileName`,`AccessPilicy`,`reemail`,`Files`,`otp`,`Date`,`Time`,`Status`) values (1,'preeti@gmail.com','1','file','Download','nakku@gmail.com','òX1üK(¯?àÆéW–ëSóÉØ.A–G»Ñyþº›½>_|Å|LÏáôºÏŸ$¾','355202','2024-03-04','17:15:55','pending');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
