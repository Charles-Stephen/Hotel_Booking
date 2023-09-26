-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 26, 2023 at 07:45 AM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 7.4.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hotel_booking_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `amount`
--

CREATE TABLE `amount` (
  `id` bigint(20) NOT NULL,
  `total_capital` bigint(20) NOT NULL,
  `returned_capital` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `amount`
--

INSERT INTO `amount` (`id`, `total_capital`, `returned_capital`) VALUES
(1, 10000, 0),
(30, 36700, 0),
(31, 10000, 26700),
(32, 36700, 0),
(33, -33800, 0),
(34, -94900, 0),
(35, -156000, 0),
(36, -221800, 0),
(37, -213400, 0);

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `message` longtext NOT NULL,
  `status` varchar(255) NOT NULL DEFAULT 'unread'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contact`
--

INSERT INTO `contact` (`id`, `name`, `email`, `message`, `status`) VALUES
(1, 'Charles Stephen', 'charlesadwin99@gmail.com', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 'read'),
(2, 'Haari Raaj', 'haariraaj23456789@gmail.com', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 'read'),
(3, 'Social Media Marketing', 'technicalshahzaib093@gmail.com', 'fghjkl;', 'read'),
(4, 'Ali', 'ali@gmail.com', 'kkkkl', 'read'),
(5, 'Joshua', 'colinchristopher2001@gmail.com', 'jkl', 'read'),
(6, 'Colin', 'colinchristopher2001@gmail.com', 'demo', 'read');

-- --------------------------------------------------------

--
-- Table structure for table `facilities`
--

CREATE TABLE `facilities` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `facilities`
--

INSERT INTO `facilities` (`id`, `name`) VALUES
(1, 'Single Bed'),
(2, 'Double Bed'),
(3, 'Breakfast'),
(4, 'Lunch'),
(5, 'Dinner'),
(6, '1 Bedroom'),
(7, '2 Bedrooms'),
(8, 'Play Area'),
(9, 'Shower'),
(10, 'Swimming Pool'),
(11, 'King Bed'),
(12, 'Kitchen'),
(13, 'Lounge'),
(14, 'gym'),
(15, 'Volleyball Court'),
(16, 'Basketball Court'),
(17, 'Tennis Court');

-- --------------------------------------------------------

--
-- Table structure for table `package`
--

CREATE TABLE `package` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `price` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `package`
--

INSERT INTO `package` (`id`, `name`, `price`) VALUES
(2, 'Standard', '4700'),
(3, 'Premium', '8900'),
(8, 'Basic', '2800');

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `id` bigint(20) NOT NULL,
  `cover_img` varchar(255) NOT NULL,
  `img_1` varchar(255) NOT NULL,
  `img_2` varchar(255) NOT NULL,
  `img_3` varchar(255) NOT NULL,
  `img_4` varchar(255) NOT NULL,
  `room_number` bigint(20) NOT NULL,
  `facilities_1` int(11) NOT NULL,
  `facilities_2` int(11) NOT NULL,
  `facilities_3` int(11) NOT NULL,
  `facilities_4` int(11) NOT NULL,
  `facilities_5` int(11) NOT NULL,
  `facilities_6` int(11) NOT NULL,
  `package_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`id`, `cover_img`, `img_1`, `img_2`, `img_3`, `img_4`, `room_number`, `facilities_1`, `facilities_2`, `facilities_3`, `facilities_4`, `facilities_5`, `facilities_6`, `package_id`) VALUES
(1, '1256855604958328181288929081246502coverimage.jpg', '9053747960288760006011694043814499image1.jpg', '6292646130242501644739541682896205image2.jpg', '2834704654845561032098545647546832image3.jpg', '', 1000, 3, 5, 1, 2, 7, 0, 2),
(5, '1256855604958328181288929081246502coverimage.jpg', '1859033269840587347995245050776476image1.jpg', '1356871377695013150879046617501620image2.jpg', '', '', 1001, 7, 1, 11, 10, 5, 3, 3),
(6, '4300089404202824476784709664494861coverimage.jpg', '8250534142065102099606243580865995image1.jpg', '7132012427654965709110429591511069image2.jpg', '', '', 1003, 4, 2, 6, 0, 0, 0, 8);

-- --------------------------------------------------------

--
-- Table structure for table `room_booking`
--

CREATE TABLE `room_booking` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `room_id` bigint(20) NOT NULL,
  `booking_date` varchar(255) NOT NULL,
  `starting_date` varchar(255) NOT NULL,
  `ending_date` varchar(255) NOT NULL,
  `room_cost` bigint(20) NOT NULL,
  `total_cost` bigint(20) NOT NULL,
  `credit_card_number` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `room_booking`
--

INSERT INTO `room_booking` (`id`, `user_id`, `room_id`, `booking_date`, `starting_date`, `ending_date`, `room_cost`, `total_cost`, `credit_card_number`, `status`) VALUES
(26, 2, 5, '2023-09-23', '2023-09-23', '2023-09-25', 8900, 26700, '5678', 'booked'),
(27, 2, 5, '2023-09-23', '2023-09-27', '2023-09-29', 8900, 26700, '56789', 'booked'),
(32, 1, 6, '2023-09-23', '2023-09-23', '2023-09-25', 2800, 8400, '56789', 'booked');

-- --------------------------------------------------------

--
-- Table structure for table `slider`
--

CREATE TABLE `slider` (
  `id` bigint(20) NOT NULL,
  `img` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL DEFAULT 'show'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `slider`
--

INSERT INTO `slider` (`id`, `img`, `status`) VALUES
(1, '2067852176391520440203584871287175image.jpg', 'show'),
(2, '7445369225279062366915261559387984image.jpg', 'show'),
(3, '9865587380193910725325598474489919image.jpg', 'show'),
(4, '8305230653229043065549511212525955image.jpg', 'hide');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `created_on` varchar(255) NOT NULL,
  `updated_on` varchar(255) NOT NULL,
  `role` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `phone`, `created_on`, `updated_on`, `role`) VALUES
(1, 'Charles Stephen', 'admin@gmail.com', '202cb962ac59075b964b07152d234b70', '+923343427289', '12-08-2023 - 08:42', '21-08-2023 - 07:10', 0),
(2, 'Ahmer', 'ahmer@gmail.com', 'caf1a3dfb505ffed0d024130f58c5cfa', '+923318343144', '12-08-2023 - 08:48', '23-09-2023 - 09:59', 1),
(4, 'Hayyan', 'hayyan@gmail.com', '202cb962ac59075b964b07152d234b70', '33333', '12-08-2023 - 08:50', '', 1),
(5, 'Idrees', 'idrees@gmail.com', '202cb962ac59075b964b07152d234b70', '+92 342 7118882', '12-08-2023 - 09:03', '', 1),
(6, 'Joshua', 'joshua@gmail.com', '202cb962ac59075b964b07152d234b70', '+447456440988', '12-08-2023 - 09:07', '', 1),
(7, 'Haroon', 'haroon@gmail.com', '202cb962ac59075b964b07152d234b70', '123456', '12-08-2023 - 09:09', '27-08-2023 - 05:42', 1),
(11, 'Ahmed', 'ahmed@gmail.com', '202cb962ac59075b964b07152d234b70', '+9237118882', '01-09-2023 - 06:49', '', 1),
(12, 'hamza', 'humza123@gma', '698d51a19d8a121ce581499d7b701668', '00000000000000000000', '23-09-2023 - 12:08', '', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `amount`
--
ALTER TABLE `amount`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `facilities`
--
ALTER TABLE `facilities`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `package`
--
ALTER TABLE `package`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `room_booking`
--
ALTER TABLE `room_booking`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `slider`
--
ALTER TABLE `slider`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `amount`
--
ALTER TABLE `amount`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `contact`
--
ALTER TABLE `contact`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `facilities`
--
ALTER TABLE `facilities`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `package`
--
ALTER TABLE `package`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `room_booking`
--
ALTER TABLE `room_booking`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `slider`
--
ALTER TABLE `slider`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
