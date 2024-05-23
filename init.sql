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
    agenda_id BIGINT NOT NULL ,
    dia DATE NOT NULL,
    horario VARCHAR(45) NOT NULL,
    telefone VARCHAR(12) NOT NULL,
    PRIMARY KEY (agenda_id)
    );

INSERT INTO tbl_cliente (nome, idade, username, email, endereco, telefone, senha)
VALUES ("admin", 00, "admin", "admin@admin.com", "admin", "admin", "admin");

INSERT INTO tbl_horas (horarios)
VALUES ("09h"), ("10h"), ("11h"), ("13h"), ("14h"), ("15h"), ("16h"), ("17h");

INSERT INTO tbl_agenda (agenda_id, dia, horario, telefone)
VALUES (1, "2024-05-01", "11h", "111111");