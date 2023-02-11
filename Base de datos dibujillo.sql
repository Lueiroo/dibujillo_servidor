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

INSERT INTO usuario VALUES ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkNyaXN0aW5hIn0.zSuPSNULqSYojIuuRyy8MpNBAQ1wgT3mnkLINi9u5VY","Cristina",NULL,NULL),
("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21icmUiOiJEaWVnbyIsImVtYWlsIjoiZGllZ29AZGllZ28uY29tIn0.Uw9SnAmZPpRjzl4gPt_1NxE2RH-mQCOXDhnPMK13QA4","Diego","diego@diego.com","bcrypt_sha256$$2b$12$JLZYU28HErqLyWjzoMJNvus0.VWkTgLZbm.yg3impUkAY9ZLP/UXG"),
("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21icmUiOiJNYXJpYSIsImVtYWlsIjoibWFyaWFAbWFyaWEuY29tIn0.bEv0JCfGie_IMwh4riCxmvl1s8k1KikBChpK3L8K2I4","Maria","maria@maria.com","bcrypt_sha256$$2b$12$KK4fwfKnaCN8EPoF1eY.sOdO7zBR3YdZeTa17UImYzGOpBpNqZIHi");

INSERT INTO partida VALUES ("QWE","Dragon jugando al ajedrez con un humano","2023-02-11 18:10:13","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21icmUiOiJNYXJpYSIsImVtYWlsIjoibWFyaWFAbWFyaWEuY29tIn0.bEv0JCfGie_IMwh4riCxmvl1s8k1KikBChpK3L8K2I4"),
("XJW","Perro sobre un caballo","2023-02-11 18:00:13","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21icmUiOiJEaWVnbyIsImVtYWlsIjoiZGllZ29AZGllZ28uY29tIn0.Uw9SnAmZPpRjzl4gPt_1NxE2RH-mQCOXDhnPMK13QA4");

INSERT INTO participa VALUES (1,"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21icmUiOiJEaWVnbyIsImVtYWlsIjoiZGllZ29AZGllZ28uY29tIn0.Uw9SnAmZPpRjzl4gPt_1NxE2RH-mQCOXDhnPMK13QA4","XJW"),
(2,"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkNyaXN0aW5hIn0.zSuPSNULqSYojIuuRyy8MpNBAQ1wgT3mnkLINi9u5VY","XJW"),
(3,"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21icmUiOiJNYXJpYSIsImVtYWlsIjoibWFyaWFAbWFyaWEuY29tIn0.bEv0JCfGie_IMwh4riCxmvl1s8k1KikBChpK3L8K2I4","QWE"),
(4,"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21icmUiOiJEaWVnbyIsImVtYWlsIjoiZGllZ29AZGllZ28uY29tIn0.Uw9SnAmZPpRjzl4gPt_1NxE2RH-mQCOXDhnPMK13QA4","QWE"),
(5,"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkNyaXN0aW5hIn0.zSuPSNULqSYojIuuRyy8MpNBAQ1wgT3mnkLINi9u5VY","QWE");

INSERT INTO dibujo VALUES (1,"2022-02-11","https://s1.eestatic.com/2020/10/09/ciencia/nutricion/patatas-adelgazar-dieta_526958892_162156492_1024x576.jpg","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21icmUiOiJEaWVnbyIsImVtYWlsIjoiZGllZ29AZGllZ28uY29tIn0.Uw9SnAmZPpRjzl4gPt_1NxE2RH-mQCOXDhnPMK13QA4","XJW"),
(2,"2022-02-11","https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/cherries-royalty-free-image-1656341880.jpg?crop=0.668xw:1.00xh;0.111xw,0&resize=640:*","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkNyaXN0aW5hIn0.zSuPSNULqSYojIuuRyy8MpNBAQ1wgT3mnkLINi9u5VY","XJW"),
(3,"2022-02-11","https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/NCI_Visuals_Food_Hamburger.jpg/640px-NCI_Visuals_Food_Hamburger.jpg","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21icmUiOiJNYXJpYSIsImVtYWlsIjoibWFyaWFAbWFyaWEuY29tIn0.bEv0JCfGie_IMwh4riCxmvl1s8k1KikBChpK3L8K2I4","QWE"),
(4,"2022-02-11","https://cdn.shopify.com/s/files/1/0536/4514/8323/products/lonbali-shopping-bag-born-b_w-black-back_800x.jpg?v=1669656693","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21icmUiOiJEaWVnbyIsImVtYWlsIjoiZGllZ29AZGllZ28uY29tIn0.Uw9SnAmZPpRjzl4gPt_1NxE2RH-mQCOXDhnPMK13QA4","QWE"),
(5,"2022-02-11","https://www.webmenaje.com/18502-large_default/vaso-de-agua-de-tritan-de-lacor-set-de-6.jpg","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkNyaXN0aW5hIn0.zSuPSNULqSYojIuuRyy8MpNBAQ1wgT3mnkLINi9u5VY","QWE");

INSERT INTO comentario VALUES (1,"Que bonito","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkNyaXN0aW5hIn0.zSuPSNULqSYojIuuRyy8MpNBAQ1wgT3mnkLINi9u5VY",1),
(2,"Precioso","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21icmUiOiJEaWVnbyIsImVtYWlsIjoiZGllZ29AZGllZ28uY29tIn0.Uw9SnAmZPpRjzl4gPt_1NxE2RH-mQCOXDhnPMK13QA4",5),
(3,"No me gusta","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21icmUiOiJNYXJpYSIsImVtYWlsIjoibWFyaWFAbWFyaWEuY29tIn0.bEv0JCfGie_IMwh4riCxmvl1s8k1KikBChpK3L8K2I4",2);

INSERT INTO valora VALUES (1,"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkNyaXN0aW5hIn0.zSuPSNULqSYojIuuRyy8MpNBAQ1wgT3mnkLINi9u5VY",2,5),
(2,"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21icmUiOiJEaWVnbyIsImVtYWlsIjoiZGllZ29AZGllZ28uY29tIn0.Uw9SnAmZPpRjzl4gPt_1NxE2RH-mQCOXDhnPMK13QA4",2,10),
(3,"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub21icmUiOiJEaWVnbyIsImVtYWlsIjoiZGllZ29AZGllZ28uY29tIn0.Uw9SnAmZPpRjzl4gPt_1NxE2RH-mQCOXDhnPMK13QA4",1,10),
(4,"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkNyaXN0aW5hIn0.zSuPSNULqSYojIuuRyy8MpNBAQ1wgT3mnkLINi9u5VY",1,5);
