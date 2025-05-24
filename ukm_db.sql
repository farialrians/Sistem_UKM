-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.30 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping structure for table ukm_portal.admin_ukm_anggota
DROP TABLE IF EXISTS `admin_ukm_anggota`;
CREATE TABLE IF NOT EXISTS `admin_ukm_anggota` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status_aktif` tinyint(1) NOT NULL,
  `tanggal_bergabung` date NOT NULL,
  `pendaftaran_id` bigint NOT NULL,
  `ukm_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_ukm_anggota_pendaftaran_id_b0f3ef29_fk_admin_ukm` (`pendaftaran_id`),
  KEY `admin_ukm_anggota_ukm_id_5f696aa5_fk_admin_ukm_ukm_id` (`ukm_id`),
  CONSTRAINT `admin_ukm_anggota_pendaftaran_id_b0f3ef29_fk_admin_ukm` FOREIGN KEY (`pendaftaran_id`) REFERENCES `admin_ukm_pendaftaranukm` (`id`),
  CONSTRAINT `admin_ukm_anggota_ukm_id_5f696aa5_fk_admin_ukm_ukm_id` FOREIGN KEY (`ukm_id`) REFERENCES `admin_ukm_ukm` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table ukm_portal.admin_ukm_anggota: ~0 rows (approximately)

-- Dumping structure for table ukm_portal.admin_ukm_mahasiswa
DROP TABLE IF EXISTS `admin_ukm_mahasiswa`;
CREATE TABLE IF NOT EXISTS `admin_ukm_mahasiswa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nim` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fakultas` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `angkatan` int NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nim` (`nim`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `admin_ukm_mahasiswa_user_id_ec0a65f3_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table ukm_portal.admin_ukm_mahasiswa: ~0 rows (approximately)
REPLACE INTO `admin_ukm_mahasiswa` (`id`, `nama`, `nim`, `fakultas`, `angkatan`, `email`, `user_id`) VALUES
	(1, 'Jesika', '2271020999', 'SAINTEK', 2022, 'jesika@gmail.com', 3);

-- Dumping structure for table ukm_portal.admin_ukm_pendaftaranukm
DROP TABLE IF EXISTS `admin_ukm_pendaftaranukm`;
CREATE TABLE IF NOT EXISTS `admin_ukm_pendaftaranukm` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nomor_telepon` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `foto_profil` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dokumen_ktm` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dokumen_cv` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dokumen_surat_minat` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dokumen_lainnya` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `mahasiswa_id` bigint NOT NULL,
  `ukm_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_ukm_pendaftara_mahasiswa_id_3a9766b6_fk_admin_ukm` (`mahasiswa_id`),
  KEY `admin_ukm_pendaftaranukm_ukm_id_72f56160_fk_admin_ukm_ukm_id` (`ukm_id`),
  CONSTRAINT `admin_ukm_pendaftara_mahasiswa_id_3a9766b6_fk_admin_ukm` FOREIGN KEY (`mahasiswa_id`) REFERENCES `admin_ukm_mahasiswa` (`id`),
  CONSTRAINT `admin_ukm_pendaftaranukm_ukm_id_72f56160_fk_admin_ukm_ukm_id` FOREIGN KEY (`ukm_id`) REFERENCES `admin_ukm_ukm` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table ukm_portal.admin_ukm_pendaftaranukm: ~0 rows (approximately)

-- Dumping structure for table ukm_portal.admin_ukm_pesan
DROP TABLE IF EXISTS `admin_ukm_pesan`;
CREATE TABLE IF NOT EXISTS `admin_ukm_pesan` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `isi` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `tanggal_kirim` datetime(6) NOT NULL,
  `dibaca` tinyint(1) NOT NULL,
  `parent_id` bigint DEFAULT NULL,
  `penerima_id` int NOT NULL,
  `pengirim_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_ukm_pesan_parent_id_75665f29_fk_admin_ukm_pesan_id` (`parent_id`),
  KEY `admin_ukm_pesan_penerima_id_8fd82518_fk_auth_user_id` (`penerima_id`),
  KEY `admin_ukm_pesan_pengirim_id_5ba305b9_fk_auth_user_id` (`pengirim_id`),
  CONSTRAINT `admin_ukm_pesan_parent_id_75665f29_fk_admin_ukm_pesan_id` FOREIGN KEY (`parent_id`) REFERENCES `admin_ukm_pesan` (`id`),
  CONSTRAINT `admin_ukm_pesan_penerima_id_8fd82518_fk_auth_user_id` FOREIGN KEY (`penerima_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `admin_ukm_pesan_pengirim_id_5ba305b9_fk_auth_user_id` FOREIGN KEY (`pengirim_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table ukm_portal.admin_ukm_pesan: ~0 rows (approximately)

-- Dumping structure for table ukm_portal.admin_ukm_ukm
DROP TABLE IF EXISTS `admin_ukm_ukm`;
CREATE TABLE IF NOT EXISTS `admin_ukm_ukm` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `logo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `deskripsi_singkat` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `visi` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `misi` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `jenis_kegiatan` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hari_mulai` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hari_selesai` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `waktu_mulai` time(6) NOT NULL,
  `waktu_selesai` time(6) NOT NULL,
  `ketua_ukm` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pengurus_pendaftaran` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `persyaratan_umum` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `berkas_dibutuhkan_json` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `alur_pendaftaran_json` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `periode_pendaftaran_mulai` date DEFAULT NULL,
  `periode_pendaftaran_selesai` date DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `admin_ukm_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_ukm_ukm_admin_ukm_id_a61ea06d_fk_auth_user_id` (`admin_ukm_id`),
  CONSTRAINT `admin_ukm_ukm_admin_ukm_id_a61ea06d_fk_auth_user_id` FOREIGN KEY (`admin_ukm_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table ukm_portal.admin_ukm_ukm: ~0 rows (approximately)
REPLACE INTO `admin_ukm_ukm` (`id`, `nama`, `logo`, `deskripsi_singkat`, `visi`, `misi`, `jenis_kegiatan`, `hari_mulai`, `hari_selesai`, `waktu_mulai`, `waktu_selesai`, `ketua_ukm`, `pengurus_pendaftaran`, `persyaratan_umum`, `berkas_dibutuhkan_json`, `alur_pendaftaran_json`, `periode_pendaftaran_mulai`, `periode_pendaftaran_selesai`, `created_at`, `admin_ukm_id`) VALUES
	(1, 'Menwa', 'ukm_logos/menwa.webp', '<p>test</p>', '<p>test</p>', '<p>test</p>', 'lainnya', 'senin', 'jumat', '08:00:00.000000', '16:00:00.000000', 'test', 'test', '<p>test</p>', '["ktm", "pas_foto", "cv", "surat_minat"]', '["online", "seleksi", "wawancara", "pengumuman"]', '2025-05-05', '2025-05-14', '2025-05-05 01:01:03.896672', 2);

-- Dumping structure for table ukm_portal.auth_group
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table ukm_portal.auth_group: ~0 rows (approximately)

-- Dumping structure for table ukm_portal.auth_group_permissions
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table ukm_portal.auth_group_permissions: ~0 rows (approximately)

-- Dumping structure for table ukm_portal.auth_permission
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table ukm_portal.auth_permission: ~44 rows (approximately)
REPLACE INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 2, 'add_permission'),
	(6, 'Can change permission', 2, 'change_permission'),
	(7, 'Can delete permission', 2, 'delete_permission'),
	(8, 'Can view permission', 2, 'view_permission'),
	(9, 'Can add group', 3, 'add_group'),
	(10, 'Can change group', 3, 'change_group'),
	(11, 'Can delete group', 3, 'delete_group'),
	(12, 'Can view group', 3, 'view_group'),
	(13, 'Can add user', 4, 'add_user'),
	(14, 'Can change user', 4, 'change_user'),
	(15, 'Can delete user', 4, 'delete_user'),
	(16, 'Can view user', 4, 'view_user'),
	(17, 'Can add content type', 5, 'add_contenttype'),
	(18, 'Can change content type', 5, 'change_contenttype'),
	(19, 'Can delete content type', 5, 'delete_contenttype'),
	(20, 'Can view content type', 5, 'view_contenttype'),
	(21, 'Can add session', 6, 'add_session'),
	(22, 'Can change session', 6, 'change_session'),
	(23, 'Can delete session', 6, 'delete_session'),
	(24, 'Can view session', 6, 'view_session'),
	(25, 'Can add mahasiswa', 7, 'add_mahasiswa'),
	(26, 'Can change mahasiswa', 7, 'change_mahasiswa'),
	(27, 'Can delete mahasiswa', 7, 'delete_mahasiswa'),
	(28, 'Can view mahasiswa', 7, 'view_mahasiswa'),
	(29, 'Can add pesan', 8, 'add_pesan'),
	(30, 'Can change pesan', 8, 'change_pesan'),
	(31, 'Can delete pesan', 8, 'delete_pesan'),
	(32, 'Can view pesan', 8, 'view_pesan'),
	(33, 'Can add ukm', 9, 'add_ukm'),
	(34, 'Can change ukm', 9, 'change_ukm'),
	(35, 'Can delete ukm', 9, 'delete_ukm'),
	(36, 'Can view ukm', 9, 'view_ukm'),
	(37, 'Can add pendaftaran ukm', 10, 'add_pendaftaranukm'),
	(38, 'Can change pendaftaran ukm', 10, 'change_pendaftaranukm'),
	(39, 'Can delete pendaftaran ukm', 10, 'delete_pendaftaranukm'),
	(40, 'Can view pendaftaran ukm', 10, 'view_pendaftaranukm'),
	(41, 'Can add anggota', 11, 'add_anggota'),
	(42, 'Can change anggota', 11, 'change_anggota'),
	(43, 'Can delete anggota', 11, 'delete_anggota'),
	(44, 'Can view anggota', 11, 'view_anggota');

-- Dumping structure for table ukm_portal.auth_user
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table ukm_portal.auth_user: ~2 rows (approximately)
REPLACE INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(1, 'pbkdf2_sha256$870000$WuxmdwbhvH3msNGKLDRIUS$3U5AvipwyFg+dHh2ZEHzaC+Vbt0DhTAy+Ex3wEssbxQ=', '2025-05-05 01:51:32.399717', 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2025-05-05 00:51:30.232685'),
	(2, 'pbkdf2_sha256$870000$yqtA6XLDyNgKKpYL3Nyw5x$li0dl+7XTpqtk0qUnzqvHevBYuCJ2tjwQ5JUi3lE5+E=', '2025-05-05 01:51:59.572433', 0, 'admin_menwa', 'UKM', 'Menwa', 'menwa@raden.ac.id', 1, 1, '2025-05-05 00:57:19.000000'),
	(3, 'pbkdf2_sha256$870000$yYB73W26h4vXLck3sfu0fw$GyUuDf+EX8VsaSUd5WHqTvrVGQbah38siidOC1aQhoY=', '2025-05-16 08:38:46.482132', 0, 'Jesika', '', '', 'jesika@gmail.com', 0, 1, '2025-05-05 01:02:36.844149');

-- Dumping structure for table ukm_portal.auth_user_groups
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table ukm_portal.auth_user_groups: ~0 rows (approximately)

-- Dumping structure for table ukm_portal.auth_user_user_permissions
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table ukm_portal.auth_user_user_permissions: ~0 rows (approximately)

-- Dumping structure for table ukm_portal.django_admin_log
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table ukm_portal.django_admin_log: ~2 rows (approximately)
REPLACE INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(1, '2025-05-05 00:57:19.981284', '2', 'admin_menwa', 1, '[{"added": {}}]', 4, 1),
	(2, '2025-05-05 00:58:21.073454', '2', 'admin_menwa', 2, '[{"changed": {"fields": ["First name", "Last name", "Email address", "Staff status"]}}]', 4, 1);

-- Dumping structure for table ukm_portal.django_content_type
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table ukm_portal.django_content_type: ~11 rows (approximately)
REPLACE INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(11, 'admin_ukm', 'anggota'),
	(7, 'admin_ukm', 'mahasiswa'),
	(10, 'admin_ukm', 'pendaftaranukm'),
	(8, 'admin_ukm', 'pesan'),
	(9, 'admin_ukm', 'ukm'),
	(3, 'auth', 'group'),
	(2, 'auth', 'permission'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(6, 'sessions', 'session');

-- Dumping structure for table ukm_portal.django_migrations
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table ukm_portal.django_migrations: ~19 rows (approximately)
REPLACE INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2025-05-05 00:50:10.448759'),
	(2, 'auth', '0001_initial', '2025-05-05 00:50:11.157479'),
	(3, 'admin', '0001_initial', '2025-05-05 00:50:11.395048'),
	(4, 'admin', '0002_logentry_remove_auto_add', '2025-05-05 00:50:11.395048'),
	(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-05-05 00:50:11.427726'),
	(6, 'admin_ukm', '0001_initial', '2025-05-05 00:50:12.188574'),
	(7, 'contenttypes', '0002_remove_content_type_name', '2025-05-05 00:50:12.325937'),
	(8, 'auth', '0002_alter_permission_name_max_length', '2025-05-05 00:50:12.429720'),
	(9, 'auth', '0003_alter_user_email_max_length', '2025-05-05 00:50:12.493679'),
	(10, 'auth', '0004_alter_user_username_opts', '2025-05-05 00:50:12.510362'),
	(11, 'auth', '0005_alter_user_last_login_null', '2025-05-05 00:50:12.627232'),
	(12, 'auth', '0006_require_contenttypes_0002', '2025-05-05 00:50:12.627232'),
	(13, 'auth', '0007_alter_validators_add_error_messages', '2025-05-05 00:50:12.647932'),
	(14, 'auth', '0008_alter_user_username_max_length', '2025-05-05 00:50:12.760575'),
	(15, 'auth', '0009_alter_user_last_name_max_length', '2025-05-05 00:50:12.875272'),
	(16, 'auth', '0010_alter_group_name_max_length', '2025-05-05 00:50:12.916547'),
	(17, 'auth', '0011_update_proxy_permissions', '2025-05-05 00:50:12.943486'),
	(18, 'auth', '0012_alter_user_first_name_max_length', '2025-05-05 00:50:13.044689'),
	(19, 'sessions', '0001_initial', '2025-05-05 00:50:13.099542');

-- Dumping structure for table ukm_portal.django_session
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table ukm_portal.django_session: ~1 rows (approximately)
REPLACE INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('urx08j1dk14bn83nwb9fws2oej42kowv', '.eJxVjDsOwjAQBe_iGlm215vNUtJzBstfHECOFCcV4u4QKQW0b2beSzi_rdVtPS9uSuIsQJx-t-DjI7cdpLtvt1nGua3LFOSuyIN2eZ1Tfl4O9--g-l6_tS4G0YBhooGsVjYzYUSAxBChEA_KQNE265HjGFKyirxBQ544YGTx_gCdHjZs:1uFqac:6VKRjo_Y5EGlPJjAeuEnyJZEjrp3i94pj-7aT3iWhAE', '2025-05-30 08:38:46.486829');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

////update
