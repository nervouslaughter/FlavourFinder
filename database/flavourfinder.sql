CREATE TABLE `restaurants` (
  `restaurant_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `category` VARCHAR(255) NOT NULL,
  `address` TEXT NOT NULL,
  `tags` VARCHAR(255) DEFAULT NULL,
  `rating` FLOAT DEFAULT NULL,
  `website` VARCHAR(255) DEFAULT NULL,
  `contact_number` VARCHAR(255) DEFAULT NULL,
  `latitude` FLOAT NOT NULL,
  `longitude` FLOAT NOT NULL,
  `pricing_for_two` INT(11) DEFAULT NULL,
  PRIMARY KEY (`restaurant_id`)
);

CREATE TABLE `users` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
);

CREATE TABLE `reviews` (
  `review_id` INT(11) NOT NULL AUTO_INCREMENT,
  `restaurant_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  `rating` FLOAT NOT NULL,
  `comment` TEXT NOT NULL,
  `upvote_count` INT(11) DEFAULT NULL,
  PRIMARY KEY (`review_id`),
  CONSTRAINT `fk_reviews_restaurants` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`restaurant_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_reviews_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `images` (
  `image_id` INT(11) NOT NULL AUTO_INCREMENT,
  `restaurant_id` INT(11) NOT NULL,
  `image_url` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`image_id`),
  CONSTRAINT `fk_images_restaurants` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`restaurant_id`) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE `reviewstoimages` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(255) NOT NULL,
  `review_ied` INT(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
);