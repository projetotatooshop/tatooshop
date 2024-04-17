CREATE schema tatoo_shop;
USE tatoo_shop;
CREATE TABLE tbl_cliente(
    usuario_id BIGINT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(45) NOT NULL, idade INT NOT NULL,
    email VARCHAR(45) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    telefone VARCHAR(12) NOT NULL,
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
