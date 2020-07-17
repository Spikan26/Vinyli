CREATE TABLE IF NOT EXISTS `vinyliDB`.`Genre` (
  `idGenre` INT NOT NULL,
  `nom` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idGenre`));


CREATE TABLE IF NOT EXISTS `vinyliDB`.`Produit` (
  `idProduit` INT NOT NULL,
  `titre` VARCHAR(255) NOT NULL,
  `annee_sortie` DATE NULL,
  `prix` DECIMAL(2) NOT NULL,
  `quantite` INT NOT NULL,
  `description` VARCHAR(255) NULL,
  `extrait` VARCHAR(255) NULL,
  `image` VARCHAR(255) NULL,
  `fk_genre` INT NULL,
  PRIMARY KEY (`idProduit`),
  INDEX `idGenre_idx` (`fk_genre` ASC),
  CONSTRAINT `idGenre`
    FOREIGN KEY (`fk_genre`)
    REFERENCES `vinyliDB`.`Genre` (`idGenre`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


CREATE TABLE IF NOT EXISTS `vinyliDB`.`Artiste` (
  `idArtiste` INT NOT NULL,
  `nom` VARCHAR(45) NOT NULL,
  `bio` VARCHAR(255) NULL,
  `image` VARCHAR(255) NULL,
  PRIMARY KEY (`idArtiste`));


CREATE TABLE IF NOT EXISTS `vinyliDB`.`Client` (
  `idClient` INT NOT NULL,
  `nom` VARCHAR(45) NOT NULL,
  `prenom` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `mdp` VARCHAR(255) NOT NULL,
  `adresse` VARCHAR(255) NULL,
  `code_postal` INT NULL,
  `ville` VARCHAR(45) NULL,
  PRIMARY KEY (`idClient`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC));


CREATE TABLE IF NOT EXISTS `vinyliDB`.`ProduitArtiste` (
  `idMusiqueArtiste` INT NOT NULL,
  `fk_produit` INT NULL,
  `fk_artiste` INT NULL,
  PRIMARY KEY (`idMusiqueArtiste`),
  INDEX `fk_musique_idx` (`fk_produit` ASC),
  INDEX `fk_artiste_idx` (`fk_artiste` ASC),
  CONSTRAINT `fk_musique`
    FOREIGN KEY (`fk_produit`)
    REFERENCES `vinyliDB`.`Produit` (`idProduit`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_artiste`
    FOREIGN KEY (`fk_artiste`)
    REFERENCES `vinyliDB`.`Artiste` (`idArtiste`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


CREATE TABLE IF NOT EXISTS `vinyliDB`.`Panier` (
  `idPanier` INT NOT NULL,
  `fk_produit` INT NULL,
  `fk_client` INT NULL,
  `valide` TINYINT NULL,
  PRIMARY KEY (`idPanier`),
  INDEX `idProduit_idx` (`fk_produit` ASC),
  INDEX `idClient_idx` (`fk_client` ASC),
  CONSTRAINT `idProduit`
    FOREIGN KEY (`fk_produit`)
    REFERENCES `vinyliDB`.`Produit` (`idProduit`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `idClient`
    FOREIGN KEY (`fk_client`)
    REFERENCES `vinyliDB`.`Client` (`idClient`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


CREATE TABLE IF NOT EXISTS `vinyliDB`.`Facturation` (
  `idFacturation` INT NOT NULL,
  `fk_panier` INT NULL,
  `date` DATETIME NOT NULL,
  `prix_total` DECIMAL(2) NOT NULL,
  PRIMARY KEY (`idFacturation`),
  INDEX `idPanier_idx` (`fk_panier` ASC),
  CONSTRAINT `idPanier`
    FOREIGN KEY (`fk_panier`)
    REFERENCES `vinyliDB`.`Panier` (`idPanier`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
