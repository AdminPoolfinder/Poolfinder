-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 17 Bulan Mei 2026 pada 14.34
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `poolfinder_db`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`) VALUES
(1, 'admin_pool', 'scrypt:32768:8:1$imBd5OztnxaM4x3k$e0a1e3f7036598394223766964dbe703d21cebf67d871e409e4f25570cbbdcb50c682da112ef167e7e300bb2cc4f3bdfebcebc85d22bcae8add1739025c23499');

-- --------------------------------------------------------

--
-- Struktur dari tabel `kolam`
--

CREATE TABLE `kolam` (
  `id` int(11) NOT NULL,
  `nama` varchar(255) DEFAULT NULL,
  `jenis` varchar(100) DEFAULT NULL,
  `harga` float DEFAULT NULL,
  `kebersihan` varchar(100) DEFAULT NULL,
  `fasilitas` varchar(255) DEFAULT NULL,
  `kedalaman` varchar(50) DEFAULT NULL,
  `skor_harga` float DEFAULT NULL,
  `skor_rating` float DEFAULT NULL,
  `alamat_lengkap` text DEFAULT NULL,
  `kecamatan` varchar(100) DEFAULT NULL,
  `panjang` varchar(50) DEFAULT NULL,
  `jalur` varchar(50) DEFAULT NULL,
  `papan_start` varchar(50) DEFAULT NULL,
  `pace_clock` varchar(50) DEFAULT NULL,
  `lokasi` varchar(100) DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `air_hangat` varchar(20) DEFAULT NULL,
  `link_google_maps` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `kolam`
--

INSERT INTO `kolam` (`id`, `nama`, `jenis`, `harga`, `kebersihan`, `fasilitas`, `kedalaman`, `skor_harga`, `skor_rating`, `alamat_lengkap`, `kecamatan`, `panjang`, `jalur`, `papan_start`, `pace_clock`, `lokasi`, `rating`, `air_hangat`, `link_google_maps`) VALUES
(114, 'Kolam Renang Zwembad Stadion Gajayana', 'Umum', 12500, 'Cukup', 'Loker, ruang ganti, kolam anak, tribun', '1.7-2.2m', 0, 0, 'Jl. Tangkuban Perahu No.18 Kauman', 'Klojen', '50m', '8', 'Ada', 'Ada', 'Sangat Mudah', 4, 'Tidak', 'https://maps.app.goo.gl/LV48RrCNWZ1BpXjd8'),
(115, 'Kolam Renang Tirta Marabunta', 'Umum', 15000, 'Bersih', 'Loker, ruang ganti, kamar bilas, kolam anak', '1.45-2m', 0, 0, 'Jl. Kesatrian Lapangan Rampal', 'Blimbing', '50m', '10', 'Ada', 'Ada', 'Mudah', 4.3, 'Tidak', 'https://maps.app.goo.gl/7fa2BzWeLm5DhRru7'),
(116, 'Taman Rekreasi Tlogomas', 'Umum', 20000, 'Cukup', 'Kolam dewasa, kolam anak, seluncuran', '1-3m', 0, 0, 'Jl. Baiduri Pandan No.17 Tlogomas', 'Lowokwaru', '50m', '6', 'Ada', 'Tidak', 'Mudah', 4.4, 'Tidak', 'https://maps.app.goo.gl/ro4zNj3WhFjmAdkH8'),
(117, 'UM Swimming Pool', 'Umum', 15000, 'Cukup', 'Ruang ganti, loker, kamar bilas', '1.4-2m', 0, 0, 'Jl. Graha Cakrawala No.17 Sumbersari', 'Lowokwaru', '50m', '10', 'Ada', 'Ada', 'Sangat Mudah', 4.2, 'Tidak', 'https://maps.app.goo.gl/mgUh4iQ836LCmoz9A'),
(118, 'Kolam Renang Universitas Brawijaya', 'Umum', 15000, 'Cukup', 'Ruang ganti, loker', '1-2m', 0, 0, 'Jl. Veteran No.1 Kampus UB', 'Lowokwaru', '50m', '8', 'Ada', 'Ada', 'Sangat Mudah', 4.1, 'Tidak', 'https://maps.app.goo.gl/EZpyPPgsaWdzBbpn6'),
(119, 'Permata Jingga Swimming Pool', 'Umum', 42500, 'Bersih', 'Ruang ganti, loker, mushalla, cafe', '1.2-1.5m', 0, 0, 'Jl. Raya Permata Jingga I Tunggulwulung', 'Lowokwaru', '25m', '4', 'Tidak', 'Tidak', 'Mudah', 4.3, 'Tidak', 'https://maps.app.goo.gl/Sn1u3SCu1TUssEKu8'),
(120, 'Araya Family Club House', 'Umum', 70000, 'Sangat Bersih', 'Fitness center, tennis, basket, cafe', '1-2m', 0, 0, 'Jl. Raya Golf Utama No.1 Kedungkandang', 'Kedungkandang', '25m', '4', 'Ada', 'Tidak', 'Sulit', 4.4, 'Tidak', 'https://maps.app.goo.gl/7sEWFAz5Xc9pLpMJ9'),
(121, 'Kolam Renang Tarekot', 'Umum', 10000, 'Cukup', 'Wahana permainan, jogging track', '1.1-1.5m', 0, 0, 'Jl. Simpang Mojopahit No.1', 'Klojen', '20m', '4', 'Tidak', 'Tidak', 'Mudah', 3.9, 'Tidak', 'https://maps.app.goo.gl/DSXKhvJ7KNncRj977'),
(122, 'Warna Swimming Pool', 'Umum', 15000, 'Bersih', 'Kamar bilas', '1.2-1.5m', 0, 0, 'Jl. Ikhwan Ridwan Rais Gg. IX No.309', 'Sukun', '15m', '2', 'Tidak', 'Tidak', 'Mudah', 4.3, 'Tidak', 'https://maps.app.goo.gl/FHHzxAqEm1RWYVLW7'),
(123, 'Eco Club Citra Garden City', 'Umum', 35000, 'Cukup', '2 kolam, snack area', '1.7m', 0, 0, 'Jl. The Hill Boulevard Buring', 'Kedungkandang', '25m', '4', 'Tidak', 'Tidak', 'Sulit', 4.2, 'Tidak', 'https://maps.app.goo.gl/csA2PwzJxQXrsv3w7'),
(124, 'NK Swimming Pool', 'Umum', 40000, 'Bersih', 'Kolam anak, seluncuran, air mancur', '1.2-1.5m', 0, 0, 'Jl. Candi Panggung No.12 Merjosari', 'Lowokwaru', '25m', '4', 'Tidak', 'Tidak', 'Cukup', 4, 'Tidak', 'https://maps.app.goo.gl/Xx2vYSu26pF9jxvx8'),
(125, 'Omah Bamboo Java', 'Umum', 12500, 'Bersih', '4 kolam, suasana teduh bambu', '1.2-1.5m', 0, 0, 'Jl. Batu Amaril No.80 Pandanwangi', 'Blimbing', '20m', '4', 'Tidak', 'Tidak', 'Mudah', 4.5, 'Tidak', 'https://maps.app.goo.gl/bU2GHTaSBij3RNnn8'),
(126, 'Kolam Renang Sulfat', 'Umum', 10000, 'Cukup', 'Kamar bilas', '1.2-1.5m', 0, 0, 'Jl. Simpang Sulfat Selatan Gg. Kolam No.1', 'Blimbing', '15m', '2', 'Tidak', 'Tidak', 'Mudah', 3.8, 'Tidak', 'https://maps.app.goo.gl/XHHnenrv2yHC6nxK7'),
(127, 'Kolam Renang Lanal Malang', 'Umum', 11000, 'Cukup', 'Kamar mandi, kantin, area teduh', '0.85-1.65m', 0, 0, 'Jl. Yos Sudarso Kasin', 'Klojen', '15m', '6', 'Ada', 'Ada', 'Mudah', 4.1, 'Tidak', 'https://maps.app.goo.gl/VFfe1a7CHz7Ep2Hy5'),
(128, 'Maxone Ascent Hotel Malang', 'Hotel', 42500, 'Bersih', 'Rooftop pool, welcome drink, nasi goreng', '1.2-1.5m', 0, 0, 'Jl. Jaksa Agung Suprapto No.75A', 'Klojen', '15m', '2', 'Tidak', 'Tidak', 'Sangat Mudah', 4.4, 'Tidak', 'https://maps.app.goo.gl/YLQ4Bm7cQ87XBLYB6'),
(129, 'Swiss-Belinn Malang', 'Hotel', 40000, 'Bersih', 'Kolam dewasa, handuk, welcome drink', '1.2-1.5m', 0, 0, 'Jl. Veteran No.8A', 'Klojen', '15m', '2', 'Tidak', 'Tidak', 'Sangat Mudah', 4.3, 'Tidak', 'https://maps.app.goo.gl/xNTKPiA6Joph3xBR9'),
(130, 'Ubud Cottages Malang', 'Hotel', 50000, 'Bersih', 'Nuansa Bali, gazebo, 2 kolam, handuk', '1.2-1.5m', 0, 0, 'Jl. Bendungan Sigura-gura Barat No.6', 'Sukun', '15m', '2', 'Tidak', 'Tidak', 'Cukup', 4.2, 'Tidak', 'https://maps.app.goo.gl/gHXaBDrzAdNKQXMQ9'),
(131, 'Ibis Style Malang', 'Hotel', 62500, 'Sangat Bersih', 'Kolam air hangat semi-indoor, mini gym', '1.2-1.5m', 0, 0, 'Jl. Letjen S. Parman No.45', 'Blimbing', '15m', '2', 'Tidak', 'Tidak', 'Mudah', 4.2, 'Ya', 'https://maps.app.goo.gl/GEUTezYFXAGPdUKCA'),
(132, 'Ijen Suites & Convention Malang', 'Hotel', 42500, 'Bersih', 'Kolam rindang, jacuzzi, sauna, fitness center', '1.35m', 0, 0, 'Jl. Ijen Nirwana Raya Blok A No.16', 'Klojen', '15m', '2', 'Tidak', 'Tidak', 'Mudah', 4.5, 'Ya', 'https://maps.app.goo.gl/ZEghMwLRYzfsCxSo7'),
(133, 'Grand Mercure Malang', 'Hotel', 70000, 'Sangat Bersih', 'Kolam outdoor modern, lounge tepi kolam, spa', '1.2-1.5m', 0, 0, 'Jl. Raden Panji Suroso No.7', 'Blimbing', '15m', '2', 'Tidak', 'Tidak', 'Mudah', 4.6, 'Ya', 'https://maps.app.goo.gl/74QXTLvVs7T6Dquc6'),
(134, 'The Alana Hotel Malang', 'Hotel', 70000, 'Bersih', 'Kolam renang pilihan air hangat/dingin, gym, spa', '1.2-1.5m', 0, 0, 'Jl. Ahmad Yani No.12', 'Blimbing', '15m', '2', 'Tidak', 'Tidak', 'Mudah', 4.3, 'Ya', 'https://maps.app.goo.gl/tGzWE9uuXGwmFSTi7'),
(135, 'Atria Hotel Malang', 'Hotel', 62500, 'Bersih', 'Kolam renang outdoor lantai 3, gym, spa, restoran', '1.2-1.5m', 0, 0, 'Jl. Letjen S. Parman No.87-89 Purwantoro', 'Blimbing', '15m', '2', 'Tidak', 'Tidak', 'Mudah', 4.4, 'Tidak', 'https://maps.app.goo.gl/LGWn6sLNFLNBD8MZ7');

-- --------------------------------------------------------

--
-- Struktur dari tabel `review`
--

CREATE TABLE `review` (
  `id` int(11) NOT NULL,
  `kolam_id` int(11) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `komentar` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`) VALUES
(1, 'user', 'user@poolfinder.com', 'scrypt:32768:8:1$d1XK6rSj2nwZwje0$12809663a6a976fa8baeba1816b24f1a2af2dc36d01803113314119f065c1fe135471153f61e36b502f3a7670c3adb9988d1d3f708c418f5b24e612bd1e0796f');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indeks untuk tabel `kolam`
--
ALTER TABLE `kolam`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `review`
--
ALTER TABLE `review`
  ADD PRIMARY KEY (`id`),
  ADD KEY `kolam_id` (`kolam_id`);

--
-- Indeks untuk tabel `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `kolam`
--
ALTER TABLE `kolam`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=136;

--
-- AUTO_INCREMENT untuk tabel `review`
--
ALTER TABLE `review`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT untuk tabel `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`kolam_id`) REFERENCES `kolam` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
