SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


CREATE SCHEMA IF NOT EXISTS `academia` DEFAULT CHARACTER SET utf8 ;
USE `academia` ;

CREATE TABLE IF NOT EXISTS `academia`.`Aluno` (
  `CPF` INT NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `senha` VARCHAR(45) NOT NULL,
  `data_nascimento` DATE NOT NULL,
  `foto` LONGBLOB NULL,
  PRIMARY KEY (`CPF`))
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `academia`.`Instrutor` (
  `CPF` INT NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `senha` VARCHAR(45) NOT NULL,
  `data_nascimento` DATE NOT NULL,
  `foto` LONGBLOB NULL,
  PRIMARY KEY (`CPF`))
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `academia`.`Funcionario` (
  `CPF` INT NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `senha` VARCHAR(45) NOT NULL,
  `data_nascimento` DATE NOT NULL,
  `foto` LONGBLOB NULL,
  PRIMARY KEY (`CPF`))
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `academia`.`Aula` (
  `Codigo` INT NOT NULL AUTO_INCREMENT,
  `Nome` VARCHAR(45) NOT NULL,
  `Duracao` TIME NOT NULL,
  `Instrutor_CPF` INT NOT NULL,
  PRIMARY KEY (`Codigo`),
  INDEX `fk_Aula_Instrutor_idx` (`Instrutor_CPF` ASC) VISIBLE,
  CONSTRAINT `fk_Aula_Instrutor`
    FOREIGN KEY (`Instrutor_CPF`)
    REFERENCES `academia`.`Instrutor` (`CPF`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `academia`.`Sessao` (
  `Aula_Codigo` INT NOT NULL,
  `Data` DATE NOT NULL,
  `Hora` TIME NOT NULL,
  PRIMARY KEY (`Aula_Codigo`),
  CONSTRAINT `fk_Sessao_Aula1`
    FOREIGN KEY (`Aula_Codigo`)
    REFERENCES `academia`.`Aula` (`Codigo`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `academia`.`Treino` (
  `Aluno_CPF` INT NOT NULL,
  `Tipo` VARCHAR(100) NOT NULL,
  `Instrutor_CPF` INT NOT NULL,
  PRIMARY KEY (`Aluno_CPF`, `Tipo`),
  INDEX `fk_Treino_Instrutor1_idx` (`Instrutor_CPF` ASC) VISIBLE,
  INDEX `fk_Treino_Aluno1_idx` (`Aluno_CPF` ASC) VISIBLE,
  CONSTRAINT `fk_Treino_Instrutor1`
    FOREIGN KEY (`Instrutor_CPF`)
    REFERENCES `academia`.`Instrutor` (`CPF`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Treino_Aluno1`
    FOREIGN KEY (`Aluno_CPF`)
    REFERENCES `academia`.`Aluno` (`CPF`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `academia`.`Exercicio` (
  `Nome` VARCHAR(50) NOT NULL,
  `Series` INT NOT NULL,
  `Repeticoes` INT NOT NULL,
  `Carga` INT NULL,
  `Treino_Aluno_CPF` INT NOT NULL,
  `Treino_Tipo` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`Treino_Aluno_CPF`, `Treino_Tipo`),
  CONSTRAINT `fk_Exercicio_Treino1`
    FOREIGN KEY (`Treino_Aluno_CPF` , `Treino_Tipo`)
    REFERENCES `academia`.`Treino` (`Aluno_CPF` , `Tipo`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `academia`.`Exame_fisico` (
  `data` DATE NOT NULL,
  `Funcionario_CPF` INT NOT NULL,
  `Aluno_CPF` INT NOT NULL,
  `Altura` FLOAT NOT NULL,
  `Peso_atual` FLOAT NOT NULL,
  `Peso_usual` FLOAT NOT NULL,
  PRIMARY KEY (`data`, `Aluno_CPF`),
  INDEX `fk_Exame_fisico_Funcionario1_idx` (`Funcionario_CPF` ASC) VISIBLE,
  INDEX `fk_Exame_fisico_Aluno1_idx` (`Aluno_CPF` ASC) VISIBLE,
  CONSTRAINT `fk_Exame_fisico_Funcionario1`
    FOREIGN KEY (`Funcionario_CPF`)
    REFERENCES `academia`.`Funcionario` (`CPF`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Exame_fisico_Aluno1`
    FOREIGN KEY (`Aluno_CPF`)
    REFERENCES `academia`.`Aluno` (`CPF`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `academia`.`Bioimpedancia` (
  `Condicionamento` VARCHAR(30) NOT NULL,
  `Gordura_corporal` INT NOT NULL,
  `Peso_gordura` FLOAT NOT NULL,
  `Gordura_alvo` INT NOT NULL,
  `IMC` FLOAT NOT NULL,
  `TMB` FLOAT NOT NULL,
  `Peso_ideal` FLOAT NOT NULL,
  `Massa_magra` INT NOT NULL,
  `Peso_massa_magra` INT NOT NULL,
  `Agua` INT NOT NULL,
  `Agua_L` FLOAT NOT NULL,
  `Agua_ideal` FLOAT NOT NULL,
  `Exame_fisico_data` DATE NOT NULL,
  `Exame_fisico_Aluno_CPF` INT NOT NULL,
  PRIMARY KEY (`Exame_fisico_data`, `Exame_fisico_Aluno_CPF`),
  CONSTRAINT `fk_Bioimpedancia_Exame_fisico1`
    FOREIGN KEY (`Exame_fisico_data` , `Exame_fisico_Aluno_CPF`)
    REFERENCES `academia`.`Exame_fisico` (`data` , `Aluno_CPF`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `academia`.`DobrasCutaneas_Circuferencias` (
  `Dobra_subescapular` FLOAT NOT NULL,
  `Dobra_triceptal` FLOAT NOT NULL,
  `Dobra_axilar_media` FLOAT NOT NULL,
  `Dobra_toracica` FLOAT NOT NULL,
  `Dobra_abdominal` FLOAT NOT NULL,
  `Dobra_medial_coxa` FLOAT NOT NULL,
  `Dobra_panturrilha` FLOAT NOT NULL,
  `Circu_braco` FLOAT NOT NULL,
  `Circu_cintura` FLOAT NOT NULL,
  `Circu_abdomen` FLOAT NOT NULL,
  `Circu_quadril` FLOAT NOT NULL,
  `Circu_panturrilha` FLOAT NOT NULL,
  `Exame_fisico_data` DATE NOT NULL,
  `Exame_fisico_Aluno_CPF` INT NOT NULL,
  PRIMARY KEY (`Exame_fisico_data`, `Exame_fisico_Aluno_CPF`),
  CONSTRAINT `fk_DobrasCutaneas_Circuferencias_Exame_fisico1`
    FOREIGN KEY (`Exame_fisico_data` , `Exame_fisico_Aluno_CPF`)
    REFERENCES `academia`.`Exame_fisico` (`data` , `Aluno_CPF`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
