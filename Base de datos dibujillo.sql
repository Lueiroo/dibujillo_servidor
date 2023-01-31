USE dibujillo;

CREATE TABLE usuario(
    token varchar(256) primary key not null,
    nombre varchar(20) not null,
    email varchar(50) null,
    contrasena varchar(20) null
);

CREATE TABLE partida(
    codigo int primary key not null,
    publica boolean not null,
    token_usuario varchar(100) not null
);

CREATE TABLE participa(
    id int primary key not null,
    token_usuario varchar(100) not null,
    codigo_partida int not null
);

CREATE TABLE dibujo(
    id int primary key not null,
    fecha date null, /*si tiene fecha ta publicao*/
    link varchar(100) not null,
    token_usuario varchar(100) not null
);

CREATE TABLE comentario(
    id int primary key not null,
    comentario varchar(1000) not null,
    token_usuario varchar(100) not null,
    id_dibujo int not null
);


CREATE TABLE valora(
    id int primary key not null,
    token_usuario varchar(100) not null,
    id_dibujo int not null,
    puntuacion int not null
);

CREATE TABLE contiene(
    id int primary key not null,
    id_dibujo int not null,
    codigo_partida int not null,
    historia varchar(100) not null
);

ALTER TABLE partida ADD CONSTRAINT fk_usuario_partida_crea FOREIGN KEY (token_usuario) REFERENCES usuario(token);
ALTER TABLE participa ADD CONSTRAINT fk_usuario_participa FOREIGN KEY (token_usuario) REFERENCES usuario(token);
ALTER TABLE participa ADD CONSTRAINT fk_partida_participa FOREIGN KEY (codigo_partida) REFERENCES partida(codigo);

ALTER TABLE dibujo ADD CONSTRAINT fk_usuario_dibujo_crea FOREIGN KEY (token_usuario) REFERENCES usuario(token);
ALTER TABLE valora ADD CONSTRAINT fk_usuario_valora FOREIGN KEY (token_usuario) REFERENCES usuario(token);
ALTER TABLE valora ADD CONSTRAINT fk_dibujo_valora FOREIGN KEY (id_dibujo) REFERENCES dibujo(id);

ALTER TABLE contiene ADD CONSTRAINT fk_contiene_dibujo FOREIGN KEY (id_dibujo) REFERENCES dibujo(id);
ALTER TABLE contiene ADD CONSTRAINT fk_partida_contiene FOREIGN KEY (codigo_partida) REFERENCES partida(codigo);

ALTER TABLE comentario ADD CONSTRAINT fk_usuario_comentario FOREIGN KEY (token_usuario) REFERENCES usuario(token);
ALTER TABLE comentario ADD CONSTRAINT fk_dibujo_comentario FOREIGN KEY (id_dibujo) REFERENCES dibujo(id);
