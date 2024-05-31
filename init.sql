CREATE schema tatoo_shop;
USE tatoo_shop;

CREATE TABLE tbl_cliente(
    usuario_id BIGINT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(45) NOT NULL, 
    idade INT NOT NULL,
    username VARCHAR(45) NULL,
    email VARCHAR(45) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    telefone VARCHAR(12) NOT NULL,
    senha VARCHAR(45) NULL,
    CONSTRAINT UC UNIQUE (email,telefone),
    PRIMARY KEY (usuario_id)
    );

CREATE TABLE tbl_produtos(
    produto_id BIGINT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(45) NOT NULL, marca VARCHAR(45) NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    quantidade INT NOT NULL,
    PRIMARY KEY (produto_id)
    );

CREATE TABLE tbl_horas(
    horarios VARCHAR(45) NOT NULL
);

CREATE TABLE tbl_agenda(
    agenda_id BIGINT NOT NULL AUTO_INCREMENT,
    dia DATE NOT NULL,
    horario VARCHAR(45) NOT NULL,
    telefone VARCHAR(12) NOT NULL,
    tipo_pagamento VARCHAR(25) NOT NULL,
    valor_total INT NOT NULL,
    situacao VARCHAR(25) NOT NULL,
    PRIMARY KEY (agenda_id)
    );

INSERT INTO tbl_cliente (nome, idade, username, email, endereco, telefone, senha)
VALUES ("admin", 20, "admin", "admin@admin.com", "admin", "999999", "admin");

INSERT INTO tbl_horas (horarios)
VALUES ("09h"), ("10h"), ("11h"), ("13h"), ("14h"), ("15h"), ("16h"), ("17h");

INSERT INTO tbl_agenda (dia, horario, telefone, tipo_pagamento, valor_total, situacao)
VALUES ("2024-06-06", "11h", "999999", "escolher", 0, "Ok");

INSERT INTO tbl_cliente (nome, idade, username, email, endereco, telefone, senha)
VALUES ("isaac", 20, "isaac", "email@mail.com", "Rua teste", "333333", "isaac");