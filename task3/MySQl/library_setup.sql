-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 07-05-2023 a las 10:10:10
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `library_users`
--
CREATE DATABASE IF NOT EXISTS `library_users` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `library_users`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `books`
--

INSERT INTO `books` (`id`, `title`, `author`) VALUES
(11, 'Don Quijote de La Mancha', 'Miguel de Cervantes'),
(12, 'To Kill a Mockingbird', 'Harper Lee'),
(13, 'The Catcher in the Rye', 'J.D. Salinger'),
(14, 'The Great Gatsby', 'F. Scott Fitzgerald'),
(15, '1984', 'George Orwell'),
(16, 'Animal Farm', 'George Orwell'),
(17, 'Pride and Prejudice', 'Jane Austen'),
(18, 'Wuthering Heights', 'Emily Bronte'),
(19, 'Jane Eyre', 'Charlotte Bronte'),
(20, 'The Lord of the Rings', 'J.R.R. Tolkien'),
(21, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `loans`
--

CREATE TABLE `loans` (
  `id` int(11) NOT NULL,
  `id_users` int(11) NOT NULL,
  `id_books` int(11) NOT NULL,
  `state` varchar(255) NOT NULL,
  `borrower` varchar(255) NOT NULL,
  `due_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('Admin','User','Library','') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `name`, `password`, `role`) VALUES
(18, 'b', 'pbkdf2:sha256:260000$MhsCW3qvUKebpZbJ$5a61910f429c5f0fad5f203d8cb5329fbdaec4c0e7ca1c7e328ec2b36283543f', 'User'),
(19, 'c', 'pbkdf2:sha256:260000$cbKkgHC81aoEt6hM$00b6040d5b9b432b1e75de5ac016fbbb9a44e01fdade7a5d4aabc0ead7f8f985', 'Library'),
(20, 'pepe', 'pbkdf2:sha256:260000$GpmVJgsokwsQlfad$c13e8a9398b6750c10cb14b81606d8b1f938c308737787aa41f5d3fdca70c69f', 'Library'),
(21, 'juan', 'pbkdf2:sha256:260000$s90HUmHbNX0mBBJh$1ba1079390146942f41e89b7fccfe59fb8934f2ae50ed8c7a6927e3ade7c012e', 'User');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `loans`
--
ALTER TABLE `loans`
  ADD PRIMARY KEY (`id`),
  ADD KEY `books` (`id_books`),
  ADD KEY `users` (`id_users`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user` (`name`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `loans`
--
ALTER TABLE `loans`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `loans`
--
ALTER TABLE `loans`
  ADD CONSTRAINT `books` FOREIGN KEY (`id_books`) REFERENCES `books` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `users` FOREIGN KEY (`id_users`) REFERENCES `users` (`id`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
