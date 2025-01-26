SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- 

CREATE SCHEMA IF NOT EXISTS `auto_service` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `auto_service` ;

-- -----------------------------------------------------
-- Table `auto_service`.`cars`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `auto_service`.`cars` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `registration_number` VARCHAR(20) NOT NULL,
  `brand` VARCHAR(50) NOT NULL,
  `model` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `registration_number` (`registration_number` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `auto_service`.`masters`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `auto_service`.`masters` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `specialization` VARCHAR(100) NOT NULL,
  `experience_years` INT NOT NULL,
  `phone_number` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `auto_service`.`works`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `auto_service`.`works` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `car_id` INT NOT NULL,
  `master_id` INT NOT NULL,
  `problem_description` TEXT NOT NULL,
  `work_description` TEXT NOT NULL,
  `hours_worked` INT NOT NULL,
  `hourly_rate` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `car_id` (`car_id` ASC) VISIBLE,
  INDEX `master_id` (`master_id` ASC) VISIBLE,
  CONSTRAINT `works_ibfk_1`
    FOREIGN KEY (`car_id`)
    REFERENCES `auto_service`.`cars` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `works_ibfk_2`
    FOREIGN KEY (`master_id`)
    REFERENCES `auto_service`.`masters` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
