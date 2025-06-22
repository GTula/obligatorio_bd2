INSERT INTO ciudadano (ci, nombre, apellido, fecha_nac) VALUES
(50825394, 'ALBERTO', 'JOTA', '2002-10-20'),
(43456123, 'MARIA', 'LOPEZ', '1989-05-15'),
(39001234, 'JUAN', 'PEREZ', '1995-12-01'),
(12345678, 'Juan', 'Pérez', '2000-09-03'),
(23456789, 'Ana', 'Gómez', '2004-07-08');



INSERT INTO tipo_eleccion (id, nombre) VALUES
(1, 'Presidencial'),
(2, 'Ballotage'),
(3, 'Plebiscito'),
(4, 'Municipal');



INSERT INTO eleccion ( id, fecha, id_tipo_eleccion) VALUES
(1, '2025-10-20', 1),
( 2, '2025-10-20', 3),
( 3,'2025-11-30', 2),
( 4,'2025-10-31', 1);



INSERT INTO papeleta(id_eleccion) VALUES
( 1 ),
( 2 ),
( 2 ),
( 2 ),
( 2),
( 3 ),
( 3);
INSERT INTO partido(id, nombre, direccion) VALUES
(1, 'Partido A', 'Bv España 3232'),
(2, 'Partido B', 'Bv España 3232');

INSERT INTO comisaria(id, nombre) VALUES
(1, 'Comisaría 1ª');

INSERT INTO departamento(id, nombre) VALUES
(1, 'Montevideo');

INSERT INTO zona( nombre, id_departamento) VALUES
( 'Zona Centro', 1);

INSERT INTO establecimiento(direccion, id_zona, id_departamento) VALUES
('Av. Uruguay 1234', 1, 1);


INSERT INTO credencial(serie, numero, ci_ciudadano) VALUES
('A', 1001, 12345678),
('B', 1002, 23456789);

INSERT INTO candidato(ci_ciudadano, id_partido) VALUES
(12345678, 1);

INSERT INTO autoridad(ci_ciudadano, id_partido) VALUES
(23456789, 2);

INSERT INTO agente_policia(ci_ciudadano, id_comisaria) VALUES
(12345678, 1);

INSERT INTO agente_establecimiento(ci_policia, id_establecimiento) VALUES
(12345678, '1');

INSERT INTO circuito(id_eleccion, accesible, id_establecimiento) VALUES
( 1, true, 1),
( 2, true, 1);

INSERT INTO tipo_empleado( nombre) VALUES
('Presidente'),
('Vocal'),
('Secretario');

INSERT INTO mesa (num, id_circuito, id_eleccion) VALUES
(1, 1, 1);

INSERT INTO empleado_publico (ci_ciudadano, num_mesa, id_tipo) VALUES
(23456789, 1, 1);

INSERT INTO asignado (serie_credencial, numero_credencial, id_circuito, id_eleccion) VALUES
('A', 1001, 1, 1);

INSERT INTO vota_en (serie_credencial, numero_credencial, id_circuito, id_eleccion, observado) VALUES
('A', 1001, 1, 1, false);



INSERT INTO lista (id_papeleta, id_eleccion, id_partido, organo, id_departamento) VALUES
(1, 1, 1, 'Senado', 1);

INSERT INTO candidato_por_lista (id_papeleta, id_eleccion, id_candidato) VALUES
(1, 1, 12345678);

INSERT INTO voto ( id_circuito, id_eleccion) VALUES
( 1, 1),
( 1, 1),
( 2, 2),
( 2, 2),
( 2, 2),
( 1, 1),
( 1, 1);


INSERT INTO voto_anulado (id_voto) VALUES
(1);

INSERT INTO voto_blanco (id_voto) VALUES
(2);

INSERT INTO voto_normal (id_voto) VALUES
(3),
(4),
(5),
(6),
(7);

INSERT INTO voto_elige_papeleta (id_voto_normal, id_papeleta, id_eleccion) VALUES
(3, 1, 1),
(4, 2, 2),
(5, 3, 2);

INSERT INTO papeleta_plebiscito (id_papeleta, id_eleccion, nombre, valor) VALUES
(2, 2, 'Reforma Constitucional', 'SI'),
(3, 2, 'Reforma Constitucional', 'NO');
