USE dibujillo;

CREATE TABLE usuario(
    token varchar(256) primary key not null,
    nombre varchar(20) not null,
    email varchar(50) null,
    contrasena varchar(256) null
);

CREATE TABLE partida(
    codigo varchar(3) primary key not null,
    historia varchar(500) null,
    createdAt datetime not null,
    token_usuario varchar(256) not null
);

CREATE TABLE participa(
    id int auto_increment primary key not null,
    token_usuario varchar(256) not null,
    codigo_partida varchar(3) not null
);

CREATE TABLE dibujo(
    id int auto_increment primary key not null,
    fecha date null, /*si tiene fecha ta publicao*/
    link varchar(400) not null,
    token_usuario varchar(256) not null,
    codigo_partida varchar(3) not null
);

CREATE TABLE comentario(
    id int auto_increment primary key not null,
    comentario varchar(1000) not null,
    token_usuario varchar(256) not null,
    id_dibujo int not null
);


CREATE TABLE valora(
    id int auto_increment primary key not null,
    token_usuario varchar(256) not null,
    id_dibujo int not null,
    puntuacion int not null
);


ALTER TABLE partida ADD CONSTRAINT fk_usuario_partida_crea FOREIGN KEY (token_usuario) REFERENCES usuario(token);
ALTER TABLE participa ADD CONSTRAINT fk_usuario_participa FOREIGN KEY (token_usuario) REFERENCES usuario(token);
ALTER TABLE participa ADD CONSTRAINT fk_partida_participa FOREIGN KEY (codigo_partida) REFERENCES partida(codigo);

ALTER TABLE dibujo ADD CONSTRAINT fk_usuario_dibujo_crea FOREIGN KEY (token_usuario) REFERENCES usuario(token);
ALTER TABLE valora ADD CONSTRAINT fk_usuario_valora FOREIGN KEY (token_usuario) REFERENCES usuario(token);
ALTER TABLE valora ADD CONSTRAINT fk_dibujo_valora FOREIGN KEY (id_dibujo) REFERENCES dibujo(id);

ALTER TABLE comentario ADD CONSTRAINT fk_usuario_comentario FOREIGN KEY (token_usuario) REFERENCES usuario(token);
ALTER TABLE comentario ADD CONSTRAINT fk_dibujo_comentario FOREIGN KEY (id_dibujo) REFERENCES dibujo(id);

ALTER TABLE dibujo ADD CONSTRAINT fk_dibujo_partida FOREIGN KEY (codigo_partida) REFERENCES partida(codigo);
