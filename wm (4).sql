-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 01, 2025 at 06:39 AM
-- Server version: 8.0.31
-- PHP Version: 8.0.26

USE wm;
admindetails

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wm`
--

-- --------------------------------------------------------

--
-- Table structure for table `admindetails`
--

DROP TABLE IF EXISTS `admindetails`;
CREATE TABLE IF NOT EXISTS `admindetails` (
  `Admnid` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(30) NOT NULL,
  `Email` varchar(40) NOT NULL,
  `Password` varchar(20) NOT NULL,
  `Img` varchar(2000) NOT NULL,
  PRIMARY KEY (`Admnid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admindetails`
--

INSERT INTO `admindetails` (`Admnid`, `Name`, `Email`, `Password`, `Img`) VALUES
(2, 'RAHUL', 'shajicharuvilbenny@gmail.com', 'admin', '');

-- --------------------------------------------------------

--
-- Table structure for table `application`
--

DROP TABLE IF EXISTS `application`;
CREATE TABLE IF NOT EXISTS `application` (
  `Appno` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(20) NOT NULL,
  `Address` varchar(30) NOT NULL,
  `Area` varchar(30) NOT NULL,
  `Location` varchar(30) NOT NULL,
  `Houseno` int NOT NULL,
  `Phone` varchar(15) NOT NULL,
  `Uid` int NOT NULL,
  `Status` varchar(10) NOT NULL,
  `Date` varchar(100) CHARACTER SET latin1  NOT NULL,
  `type` varchar(50) NOT NULL,
  PRIMARY KEY (`Appno`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `application`
--

INSERT INTO `application` (`Appno`, `Name`, `Address`, `Area`, `Location`, `Houseno`, `Phone`, `Uid`, `Status`, `Date`, `type`) VALUES
(20, 'anju', 'fdgfg', 'dfdg', '11', 453, '44355555444', 12, 'approved', '2025-04-05', 'Rate'),
(21, 'Dia', 'dfd', 'xfds', '11', 576, '3333333333', 11, 'approved', '2025-04-04', 'Corate'),
(23, 'Sam', 'dfg', 'fghfh', '11', 434, '444444466666666', 13, 'approved', '2025-03-29', 'Corate'),
(24, 'sneha', 'dgfdg', 'dfgf', '10', 234, '444444444444444', 14, 'approved', '2025-03-29', 'Rate'),
(25, 'sree', 'fhgn', 'vcbghg', '10', 234, '56777776555', 23, 'approved', '2025-04-01', 'Rate');

-- --------------------------------------------------------

--
-- Table structure for table `assignloc`
--

DROP TABLE IF EXISTS `assignloc`;
CREATE TABLE IF NOT EXISTS `assignloc` (
  `Aid` int NOT NULL AUTO_INCREMENT,
  `Staffid` int NOT NULL,
  `Locationid` int NOT NULL,
  PRIMARY KEY (`Aid`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `assignloc`
--

INSERT INTO `assignloc` (`Aid`, `Staffid`, `Locationid`) VALUES
(12, 8, 10),
(13, 11, 11);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_23962d04_fk_auth_permission_id` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can add permission', 2, 'add_permission'),
(5, 'Can change permission', 2, 'change_permission'),
(6, 'Can delete permission', 2, 'delete_permission'),
(7, 'Can add group', 3, 'add_group'),
(8, 'Can change group', 3, 'change_group'),
(9, 'Can delete group', 3, 'delete_group'),
(10, 'Can add user', 4, 'add_user'),
(11, 'Can change user', 4, 'change_user'),
(12, 'Can delete user', 4, 'delete_user'),
(13, 'Can add content type', 5, 'add_contenttype'),
(14, 'Can change content type', 5, 'change_contenttype'),
(15, 'Can delete content type', 5, 'delete_contenttype'),
(16, 'Can add session', 6, 'add_session'),
(17, 'Can change session', 6, 'change_session'),
(18, 'Can delete session', 6, 'delete_session'),
(19, 'Can view log entry', 1, 'view_logentry'),
(20, 'Can view permission', 2, 'view_permission'),
(21, 'Can view group', 3, 'view_group'),
(22, 'Can view user', 4, 'view_user'),
(23, 'Can view content type', 5, 'view_contenttype'),
(24, 'Can view session', 6, 'view_session');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_30a071c9_fk_auth_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_3d7071f0_fk_auth_permission_id` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
CREATE TABLE IF NOT EXISTS `cart` (
  `Cartid` int NOT NULL AUTO_INCREMENT,
  `Pid` varchar(20) NOT NULL,
  `Uid` int NOT NULL,
  `Cqty` int NOT NULL,
  PRIMARY KEY (`Cartid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`Cartid`, `Pid`, `Uid`, `Cqty`) VALUES
(7, '11', 19, 1);

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
CREATE TABLE IF NOT EXISTS `category` (
  `Catid` int NOT NULL AUTO_INCREMENT,
  `Cname` varchar(30) NOT NULL,
  `Description` varchar(100) NOT NULL,
  PRIMARY KEY (`Catid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`Catid`, `Cname`, `Description`) VALUES
(6, 'Bat', 'bat is good'),
(7, 'Ball', 'Ball is good\r\n'),
(8, 'eeee   ', 'good ok');

-- --------------------------------------------------------

--
-- Table structure for table `cdetails`
--

DROP TABLE IF EXISTS `cdetails`;
CREATE TABLE IF NOT EXISTS `cdetails` (
  `Cardid` int NOT NULL AUTO_INCREMENT,
  `Cnumber` int NOT NULL,
  `Holdername` varchar(30) NOT NULL,
  `Date` varchar(15) NOT NULL,
  `Cvv` int NOT NULL,
  PRIMARY KEY (`Cardid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cdetails`
--

INSERT INTO `cdetails` (`Cardid`, `Cnumber`, `Holdername`, `Date`, `Cvv`) VALUES
(2, 2147483647, 'rocky', '12/27', 123);

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `Cid` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(35) NOT NULL,
  `Address` varchar(40) NOT NULL,
  `Phone` varchar(11) NOT NULL,
  `Gender` varchar(5) NOT NULL,
  `Email` varchar(40) NOT NULL,
  `Img` varchar(2000) NOT NULL,
  PRIMARY KEY (`Cid`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`Cid`, `Name`, `Address`, `Phone`, `Gender`, `Email`, `Img`) VALUES
(22, 'Mia', 'fgj', '55555555555', 'F', 'mia@gmail.com', ''),
(23, 'sree', 'gfh', '777777775', 'F', 'sree@gmail.com', 'customer_images/IMG_20221119_123505.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_5151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_1c5f563_fk_auth_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_3ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2022-02-28 06:39:32'),
(2, 'auth', '0001_initial', '2022-02-28 06:39:32'),
(3, 'admin', '0001_initial', '2022-02-28 06:39:32'),
(4, 'contenttypes', '0002_remove_content_type_name', '2022-02-28 06:39:32'),
(5, 'auth', '0002_alter_permission_name_max_length', '2022-02-28 06:39:32'),
(6, 'auth', '0003_alter_user_email_max_length', '2022-02-28 06:39:32'),
(7, 'auth', '0004_alter_user_username_opts', '2022-02-28 06:39:32'),
(8, 'auth', '0005_alter_user_last_login_null', '2022-02-28 06:39:32'),
(9, 'auth', '0006_require_contenttypes_0002', '2022-02-28 06:39:32'),
(10, 'sessions', '0001_initial', '2022-02-28 06:39:32'),
(11, 'admin', '0002_logentry_remove_auto_add', '2025-01-30 10:01:15'),
(12, 'admin', '0003_logentry_add_action_flag_choices', '2025-01-30 10:01:15'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2025-01-30 10:01:15'),
(14, 'auth', '0008_alter_user_username_max_length', '2025-01-30 10:01:15'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2025-01-30 10:01:15'),
(16, 'auth', '0010_alter_group_name_max_length', '2025-01-30 10:01:15'),
(17, 'auth', '0011_update_proxy_permissions', '2025-01-30 10:01:15'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2025-01-30 10:01:16');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('19737jvecwgoyrmlewxk9hovvihfpadt', 'N2ZmOTA1OGQzOWI0ZWY5NzcwYmE1NWQ5ODJjZTVhMTBmNDhmNWU4NTp7InR5cGUiOiJ1c2VyIiwiaWQiOjR9', '2022-11-21 07:34:17'),
('1kdj1ck9egtrjetgxej4rrsgpf6sfxgu', '.eJyrVgrNTFGyMjTUUQrNS8xNVbJSSslMdEjPTczM0UvOz1UCihckFhdDxEG8ksoCkKrk0uKS_NzUIqVaALsIFWM:1txhow:t_VXeFT91ji1kT0h6hm5ez_uoSzB1Vpn0x2LcT7mU9Y', '2025-04-10 07:38:34'),
('1syur7e4cr15o3r3qwt56o28hu50mn3l', '.eJyrVgrNTFGystBRCs1LzE1VslIqyc91SM9NzMzRS87PVQKKFyQWF0PEQbySygKQquKSxLQ0pVoAeEUUHw:1twebi:-yZCtAwfzTQkUI6NAfQaW7dKj5-m0nQDLMa-u5YQges', '2025-04-07 10:00:35'),
('28kotfuwgebuulldiu609ifo7rlfncmx', 'YWIyODYxYzExOWZkNDA2ODZiYWU2ODQ0ZWEyOTNlZmMxNjJkZWJiZTp7InR5cGUiOiJhZG1pbiIsImlkIjoxfQ==', '2022-11-20 20:05:59'),
('29if2eyu78fzjy6370bapwiuh98q7w7n', 'ZGI3ZjVkZmJiODBmZGFmYjJiZDhkYmE3NmNmNmE2ZjdiY2VkODU1ODp7InR5cGUiOiJ1c2VyIiwiaWQiOjF9', '2022-04-23 16:34:16'),
('2f15z5ob2fhllwc1fh6opw26y4k2qy2e', '.eJyrVgrNTFGyMtBRCs1LzE1VslJKTMnNzFMC8gsSi4uR-SWVBQj5WgD0ihHH:1tggqL:gRZgqK3rVppvuqcMhb4zIPMjfvsFsUM3arWbc0Des1o', '2025-02-22 09:09:41'),
('2ga2x0lgeul3f3jmq7y3o8j42hf3k6zz', 'ZGI3ZjVkZmJiODBmZGFmYjJiZDhkYmE3NmNmNmE2ZjdiY2VkODU1ODp7InR5cGUiOiJ1c2VyIiwiaWQiOjF9', '2022-04-24 15:08:28'),
('31vyi74mt1uldqag9h5ybg1wl6wemp27', 'NzM0MGNlNDEyMGMzODU0MzQzYjcxMWNlMTMzNmIwOTJkMWJjYmIxNDp7InR5cGUiOiJ1c2VyIiwiZW1haWwiOiJyZWV0aHVzaGFqaUBnbWFpbC5jb20iLCJpZCI6MX0=', '2022-04-23 05:42:43'),
('4mzpb876nyqm3wx3pqxnogaism5x94e1', '.eJyrVgrNTFGyMjTUUQrNS8xNVbJSKs7MynRIz03MzNFLzs9VAkoUJBYXQyVA3JLKArC6ksS0NKVaALAgFQc:1twcFw:EPh97QHwqJ37Whr9j-DpIPW3FlP7-GTkM_iaGSjrvA0', '2025-04-07 07:29:57'),
('50xeiq65meam6e6y64q7acq2r91e5c28', 'eyJ1aWQiOjEsInV0eXBlIjoidXNlciJ9:1ptsbt:6PJ0DECYWHLN0BzKFTM9hc8OYqaswDR4ePwqRAZE8Dg', '2023-05-16 16:12:13'),
('63emwbn31nqkxu5rass6le9tar832up5', 'eyJ1aWQiOjEsInV0eXBlIjoidXNlciJ9:1py7yC:6WUgfjx42iAORWpghkwhRjWxF3E7GRaDNyeyuI_nfFo', '2023-05-28 09:24:48'),
('6ufrpxfatkjwgfgwp1r4d47ta8qylgpd', 'eyJ1aWQiOjEsInV0eXBlIjoidXNlciJ9:1puPOW:Dz_wywXugm_7XlGcefJkpY1977GnKBDvJm4LM4nGUfM', '2023-05-18 03:12:36'),
('783hk250hu3ab54hhosk84us2ljmhtw5', 'YWIyODYxYzExOWZkNDA2ODZiYWU2ODQ0ZWEyOTNlZmMxNjJkZWJiZTp7InR5cGUiOiJhZG1pbiIsImlkIjoxfQ==', '2022-10-23 16:33:39'),
('88n0l97p5sb6doevqs1oliuc2m0kao0n', '.eJyrVgrNTFGyMtdRCs1LzE1VslIqyk_OrkzKSMw0NDJ2SM9NzMzRS87PVQIqKEgsLoYpAPFLKgtAGpJLi0vyc1OLlGoBv6sZVg:1tqv8r:FX2llQFI941keUyCaYcZEtz-T9XGkAfYxhZXglOnbhY', '2025-03-22 14:27:05'),
('9stcvahc0q61ala5q20558sshqby1m8i', 'Mjg2ZjFiZjJmZWJlMzhlNmZjOThlZWIzMmI3NDE3YjQyOGI2ZjU2YTp7InR5cGUiOiJidWlsZGVyIiwiZW1haWwiOjF9', '2022-03-30 14:45:03'),
('c1dwdyttjlpkby76tmb7ypduk972xx54', 'eyJ1aWQiOjEsInV0eXBlIjoidXNlciJ9:1pzhdq:Yu8FM4ARlQRHYEPFPZ9EGeR0B1DqT4CGB67qW6eIPOc', '2023-06-01 17:42:18'),
('c629696y9dmdnkck7dca8w3dhg3t7prv', 'N2ZmOTA1OGQzOWI0ZWY5NzcwYmE1NWQ5ODJjZTVhMTBmNDhmNWU4NTp7InR5cGUiOiJ1c2VyIiwiaWQiOjR9', '2022-11-14 12:53:43'),
('dpt6d9x9sy7y57wa97tp6jf29uctmc7q', '.eJyrVgrNTFGyMtBRCs1LzE1VslJKTMnNzFMC8gsSi4uR-SWVBQj5WgD0ihHH:1tliWo:7Rv0Cb3QHwY22HnRcOkHkL6C7rxsbKH8AJSmCikJOyY', '2025-03-08 05:58:18'),
('f6gimrujthidutxm9daado1zoa5kdnk7', '.eJyrVgrNTFGyMjTUUQrNS8xNVbJSSslMdEjPTczM0UvOz1UCihckFhdDxEG8ksoCkKrk0uKS_NzUIqVaALsIFWM:1txfeg:qlL2wtKMIj0f8OcQfJPNjxN0GTcFW-i_hBAmvXNzheA', '2025-04-10 05:19:50'),
('gglbtlrvmjcpeaou4dw2c5aw0dmo02fh', '.eJyrVgrNTFGyMjTUUQrNS8xNVbJSSslMdEjPTczM0UvOz1UCihckFhdDxEG8ksoCkKrk0uKS_NzUIqVaALsIFWM:1tv93R:ZldSM_rCI3rL7E1Ms0PP6mCK1-iaPcpzBO2Gez8WzJk', '2025-04-03 06:06:57'),
('iwwip14tbrilnngar18frgzzzl1fyjl3', '.eJyrVgrNTFGyMtBRCs1LzE1VslJKTMnNzFMC8gsSi4uR-SWVBQj5WgD0ihHH:1tu7Uj:oHH5i9wSf7OWPtom80ZbN47eXDiE0JWmd5ln0mkgQyw', '2025-03-31 10:14:53'),
('jgjqor5dm98gyzehe2y5hlfmwebqdwcu', '.eJyrVgrNTFGyMjLWUQrNS8xNVbJSKi5KTXVIz03MzNFLzs9VAkoUJBYXQyVA3JLKApC65NLikvzc1CKlWgDzxhZo:1tzV9o:oFojWm3ODuiU3CxNFsXyjRvotkbImcvg7D3lZcrdpT8', '2025-04-15 06:31:32'),
('k72j65ugbos62quugihotpcnau2rez64', '.eJyrVgrNTFGyMtBRCs1LzE1VslJKTMnNzFMC8gsSi4uR-SWVBQj5WgD0ihHH:1tyQVs:tG34GWnq17ycZjpLGAC7gdGbu26wKHMkYmE5qPtPbyM', '2025-04-12 07:21:52'),
('kixcuakh7cx0rqv8a68axg5sly58jl25', 'eyJ1aWQiOjEsInV0eXBlIjoidXNlciJ9:1ovXDS:o4rAr0tY62A4tKKJwl8HL4Y4besW9kdeUVP5WIdbYQs', '2022-12-01 05:13:34'),
('qupq6i83w1qgqgwcl7kmx1stvnkrql78', 'N2ZmOTA1OGQzOWI0ZWY5NzcwYmE1NWQ5ODJjZTVhMTBmNDhmNWU4NTp7InR5cGUiOiJ1c2VyIiwiaWQiOjR9', '2022-11-21 06:51:04'),
('rk113xdeway6zrqyij6d47tfbnmpg5s0', 'N2ZmOTA1OGQzOWI0ZWY5NzcwYmE1NWQ5ODJjZTVhMTBmNDhmNWU4NTp7InR5cGUiOiJ1c2VyIiwiaWQiOjR9', '2022-11-21 04:29:45'),
('ruda6ve46lm7trr9m2qty3vwygmms8sl', 'YWIyODYxYzExOWZkNDA2ODZiYWU2ODQ0ZWEyOTNlZmMxNjJkZWJiZTp7InR5cGUiOiJhZG1pbiIsImlkIjoxfQ==', '2022-11-21 07:47:30'),
('sceoazvlj29xsus3vvmxhzhpjp1v6zml', 'eyJ1aWQiOjEsInV0eXBlIjoidXNlciJ9:1pyrke:_v-eq0uskinEUe_k1FThRcCzkXySx2lvVedRlggmCNQ', '2023-05-30 10:17:52'),
('vq2j7k4x19liev73ljq28nt3piufxls8', '.eJyrVgrNTFGyMtBRCs1LzE1VslJKTMnNzFMC8gsSi4uR-SWVBQj5WgD0ihHH:1ty5w4:yUrlfNfdNzbRmFRlaNqhjHnsuu06M_venllwCuc55Zc', '2025-04-11 09:23:33'),
('wfmszz9pidle9htjx7u6dywphlan8h0t', 'eyJ1aWQiOjAsInV0eXBlIjoiYWRtaW4ifQ:1puQGy:cszh9adoFPOnEjnboayMEephhxzRjFYl4r8cAhD7BJ4', '2023-05-18 04:08:52'),
('zncj4alnj7ulrpdn1l8667ahnjuugsyo', 'YWIyODYxYzExOWZkNDA2ODZiYWU2ODQ0ZWEyOTNlZmMxNjJkZWJiZTp7InR5cGUiOiJhZG1pbiIsImlkIjoxfQ==', '2022-11-10 09:22:47');

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
CREATE TABLE IF NOT EXISTS `feedback` (
  `fid` int NOT NULL AUTO_INCREMENT,
  `feedback` varchar(5000) DEFAULT NULL,
  `uid` int DEFAULT NULL,
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`fid`, `feedback`, `uid`) VALUES
(1, 'dsfgdg', 3),
(2, 'good collection', 1),
(3, 'u', 1),
(4, 'nothing  to collect waste', 6),
(5, 'The networks are computer networks, both public and private, that are used every day to conduct transactions and communications among businesses, government agencies and individuals. The networks are comprised of nodes, which are client terminals and one or more servers and/or host computers. Network security involves the authorization of access to data in a network, which is controlled by the network administratormm.\r\nnetwork that is open to public access is the Internet, but many private networks also utilize publicly-accessible communications. Today, most companies host computers can be accessed by their employees whether in their offices over a private communications network, or from their homes or hotel rooms\r\nwhile on the road through normal telephone lines.All hosts should be on a private network that is invisible from the outsidemm. \r\nNetwork security consists of the provisions and policies adopted by a network administrator to prevent the unauthorized access, misuse, modification, or denial of a computer network and network-accessible resources.Host web servers in a DMZ, or a firewall from the outside and from the inside. Network security involves the authorization of access to data in a network, \r\nwhich is controlled by the network administrator. Users choose or are assigned an ID and password or other authenticating that allows them access and programs within their authority.These networks provide access control and data encryption between two different computers on a network. This allows remote workers to connect to the network without the risk of a hacker or thief intercepting datamm.\r\nSecurity management for networks is different for all kinds of situations. A home or small office may only require basic security while large businesses may require high-maintenance and advanced software and hardware to prevent malicious attacks from hacking and spamming.Today, most companies host computers can be accessed by their employees whether in their offices over a private communications network, or from their homes or hotel rooms while on the road through normal telephone linesmm.\r\nIn computer networking,hacking is an effort to manipulate the normal behavior of network connections. Historically, hacking referred to constructive, clever work that was not necessarily related to computermm.\r\nNetwork sniffers to impeding its flow. Sniffers are software tools commonly use by governments, corporations, hackers and studentsmm. ', 1),
(6, 'yjh', 11),
(7, 'fff', 11);

-- --------------------------------------------------------

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
CREATE TABLE IF NOT EXISTS `location` (
  `Locid` int NOT NULL AUTO_INCREMENT,
  `Location` varchar(30) NOT NULL,
  `Area` varchar(30) NOT NULL,
  `Rate` int NOT NULL,
  `Corate` int NOT NULL,
  PRIMARY KEY (`Locid`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `location`
--

INSERT INTO `location` (`Locid`, `Location`, `Area`, `Rate`, `Corate`) VALUES
(10, 'Municipality', 'adoor', 120, 135),
(11, 'Panchayath', 'kannamkode\r\n', 50, 100),
(12, 'Panchayath', 'kadambanadu', 56, 80);

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
CREATE TABLE IF NOT EXISTS `login` (
  `Lid` int NOT NULL AUTO_INCREMENT,
  `Uid` int NOT NULL,
  `Uname` varchar(30) NOT NULL,
  `Upass` varchar(10) NOT NULL,
  `Utype` varchar(10) NOT NULL,
  PRIMARY KEY (`Lid`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`Lid`, `Uid`, `Uname`, `Upass`, `Utype`) VALUES
(1, 0, 'admin', 'admin', 'admin'),
(24, 8, 'tom1@gmail.com', 'tom', 'staff'),
(25, 11, 'siji@gmail.com', 'siji', 'staff'),
(34, 22, 'mia@gmail.com', 'mia', 'customer'),
(35, 23, 'sree@gmail.com', 'sree', 'customer');

-- --------------------------------------------------------

--
-- Table structure for table `managerate`
--

DROP TABLE IF EXISTS `managerate`;
CREATE TABLE IF NOT EXISTS `managerate` (
  `Mrid` int NOT NULL AUTO_INCREMENT,
  `Mpc` varchar(20) NOT NULL,
  `Rate` int NOT NULL,
  `Type` varchar(25) NOT NULL,
  `District` varchar(25) NOT NULL,
  PRIMARY KEY (`Mrid`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `managerate`
--

INSERT INTO `managerate` (`Mrid`, `Mpc`, `Rate`, `Type`, `District`) VALUES
(18, 'Municipality', 788, 'Residential', 'Thiruvananthapuram'),
(27, 'Panchayath', 575, 'Commercial', 'Thrissur'),
(28, 'Corporation', 67, 'Residential', 'Idukki'),
(29, 'Panchayath', 35, 'Commercial', 'Ernakulam'),
(30, 'Corporation', 45, 'Residential', 'Palakkad'),
(31, 'Municipality', 788, 'Residential', 'Thiruvananthapuram'),
(32, 'Municipality', 67, 'Residential', 'Thiruvananthapuram'),
(33, 'Municipality', 67, 'Residential', 'Thiruvananthapuram');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
CREATE TABLE IF NOT EXISTS `orders` (
  `Oid` int NOT NULL AUTO_INCREMENT,
  `Odate` date NOT NULL,
  `Pid` int NOT NULL,
  `Uid` int NOT NULL,
  `Qnty` int NOT NULL,
  `Tamnt` int NOT NULL,
  `Status` varchar(10) NOT NULL,
  `Pstatus` varchar(30) NOT NULL,
  PRIMARY KEY (`Oid`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`Oid`, `Odate`, `Pid`, `Uid`, `Qnty`, `Tamnt`, `Status`, `Pstatus`) VALUES
(35, '2025-03-07', 11, 7, 2, 134, 'Delivered', 'paid'),
(36, '2025-03-28', 11, 11, 2, 134, 'Cancelled', 'paid'),
(37, '2025-03-28', 7, 11, 2, 466, 'Cancelled', 'paid'),
(38, '2025-03-28', 11, 11, 1, 67, 'Cancelled', 'paid'),
(39, '2025-03-28', 10, 11, 1, 67, 'Dispatched', 'paid'),
(40, '2025-03-28', 11, 12, 1, 67, 'Dispatched', 'COD'),
(41, '2025-04-01', 7, 23, 1, 233, 'ordered', 'paid');

-- --------------------------------------------------------

--
-- Table structure for table `pbill`
--

DROP TABLE IF EXISTS `pbill`;
CREATE TABLE IF NOT EXISTS `pbill` (
  `pid` int NOT NULL AUTO_INCREMENT,
  `apno` int NOT NULL,
  `uid` int NOT NULL,
  `date` varchar(100) NOT NULL,
  `amt` varchar(100) NOT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 ;

--
-- Dumping data for table `pbill`
--

INSERT INTO `pbill` (`pid`, `apno`, `uid`, `date`, `amt`) VALUES
(1, 20, 12, '2025-02-26', '50'),
(2, 20, 12, '2025-02-26', '50'),
(3, 21, 11, '2025-02-26', '100'),
(4, 23, 13, '2025-03-16', '100'),
(5, 23, 13, '2025-03-29', '100');

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `Pid` int NOT NULL AUTO_INCREMENT,
  `Item` varchar(20) NOT NULL,
  `Category` varchar(30) NOT NULL,
  `Subcategory` varchar(20) NOT NULL,
  `Des` varchar(200) NOT NULL,
  `Amnt` varchar(10) NOT NULL,
  `Stock` varchar(10) NOT NULL,
  `Img` varchar(2000) NOT NULL,
  PRIMARY KEY (`Pid`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`Pid`, `Item`, `Category`, `Subcategory`, `Des`, `Amnt`, `Stock`, `Img`) VALUES
(2, 'mouse', 'mouse', '4', '67', '678', '50', 'hgnjhtgj     '),
(3, 'rocky', 'nmg ghgg', '3', '56', '560', '0', 'nrmymnrmy'),
(4, 'fd bfbfd', 'fdbdfbd', '2', '34', '45', '0', 'fbdbd'),
(6, 'fd bfbfd', 'Bat', 'v f gf', 'hg,jh?', '45', '0', 'Comp Graphics.pdf'),
(7, 'dv', 'Bat', 'v f gf', 'vbb', '233', '93', 'Products/325_ROG-Prism.jpg'),
(10, ',nkbnnb,', 'Bat', 'v f gf', 'gntntt', '67', '97', '10'),
(11, 'blaaaaa', 'Bat', 'v f gf', 'mymttymtym', '67', '70', 'Products/OIP_1.jpeg');

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
CREATE TABLE IF NOT EXISTS `staff` (
  `Sid` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(30) NOT NULL,
  `Gender` varchar(5) NOT NULL,
  `Dob` varchar(20) NOT NULL,
  `Address` varchar(30) NOT NULL,
  `Place` varchar(30) NOT NULL,
  `Phone` int NOT NULL,
  `Adhaar` int NOT NULL,
  `Email` varchar(30) NOT NULL,
  `img` varchar(1000) CHARACTER SET latin1  NOT NULL,
  PRIMARY KEY (`Sid`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`Sid`, `Name`, `Gender`, `Dob`, `Address`, `Place`, `Phone`, `Adhaar`, `Email`, `img`) VALUES
(8, 'Tom', 'M', '1998-05-04', 'newwww', 'Adoorfff', 2147483647, 2147483647, 'tom1@gmail.com', 'staff_images/lindt.png'),
(9, 'fggf', 'M', '2025-02-25', 'ghgj', 'ghgh', 2147483647, 2147483647, 'tht@gmail.com', 'staff_images/aster_mims_kannur_5eOnmUw_Le6Mq7R.jpg'),
(11, 'Sijj', 'F', '2003-12-28', 'hhhhhh', 'jhhgggg', 2147483647, 2147483647, 'siji@gmail.com', 'staff_images/OIG_4.jpeg');

-- --------------------------------------------------------

--
-- Table structure for table `subcategory`
--

DROP TABLE IF EXISTS `subcategory`;
CREATE TABLE IF NOT EXISTS `subcategory` (
  `Subid` int NOT NULL AUTO_INCREMENT,
  `Subcategoryname` varchar(20) NOT NULL,
  `Category` varchar(20) NOT NULL,
  `Description` varchar(100) NOT NULL,
  PRIMARY KEY (`Subid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `subcategory`
--

INSERT INTO `subcategory` (`Subid`, `Subcategoryname`, `Category`, `Description`) VALUES
(1, 'v f gf', 'Bat', 'gf fg fg'),
(2, 'gf gf g', 'Bat', 'g g ng'),
(3, 'htmty,u7', 'Bat', 'uy,y,y,uy');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissions_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_group_permissions_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_ibfk_1` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permissions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `django_admin_log_ibfk_2` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
