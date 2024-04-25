CREATE schema tatoo_shop;
USE tatoo_shop;
CREATE TABLE tbl_cliente(
    usuario_id BIGINT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(45) NOT NULL, idade INT NOT NULL,
    username VARCHAR(45) NULL,
    email VARCHAR(45) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    telefone VARCHAR(12) NOT NULL,
    senha VARCHAR(45) NULL,
    CONSTRAINT UC UNIQUE (email,telefone),
    PRIMARY KEY (usuario_id)
    );

USE tatoo_shop;
CREATE TABLE tbl_produtos(
    produto_id BIGINT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(45) NOT NULL, marca VARCHAR(45) NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    quantidade INT NOT NULL,
    PRIMARY KEY (produto_id)
    );

USE tatoo_shop;
CREATE TABLE tbl_agendamento(
    horarios VARCHAR(5) NOT NULL
);

USE tatoo_shop;
INSERT INTO tbl_cliente (nome, idade, username, email, endereco, telefone, senha)
VALUES ("admin", 00, "admin", "admin@admin.com", "admin", "admin", "admin");

USE tatoo_shop;
INSERT INTO tbl_agendamento (horarios)
VALUES ("09h"), ("10h"), ("11h"), ("12h"), ("13h"), ("14h"), ("15h"), ("16h"), ("17h"), ("18h");