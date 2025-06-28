-- Scripts SQL:

CREATE TABLE ciudadano (
    ci varchar(8) PRIMARY KEY,
    nombre varchar(50) NOT NULL,
    apellido varchar(50) NOT NULL,
    fecha_nac date NOT NULL
);

CREATE TABLE departamento (
    id int AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(50) NOT NULL
);

CREATE TABLE comisaria (
    id int AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(50) NOT NULL
);

CREATE TABLE tipo_eleccion (
    id int AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(50) NOT NULL
);

CREATE TABLE partido (
    id int AUTO_INCREMENT PRIMARY KEY,
    direccion varchar(200) NOT NULL,
	nombre varchar(100) NOT NULL
);

CREATE TABLE zona (
    id int AUTO_INCREMENT NOT NULL,
    nombre varchar(50) NOT NULL,
    id_departamento int NOT NULL,
    PRIMARY KEY(id, id_departamento),
    FOREIGN KEY (id_departamento) REFERENCES departamento(id)
);

CREATE TABLE establecimiento (
   	id int AUTO_INCREMENT PRIMARY KEY,
    direccion varchar(200) NOT NULL,
    id_zona int NOT NULL,
	id_departamento int NOT NULL,
	FOREIGN KEY (id_zona , id_departamento ) REFERENCES zona(id, id_departamento)
);

CREATE TABLE candidato (
    ci_ciudadano varchar(8) NOT NULL PRIMARY KEY,
    FOREIGN KEY (ci_ciudadano) REFERENCES ciudadano(ci)
);

CREATE TABLE autoridad (
    ci_ciudadano varchar(8) NOT NULL PRIMARY KEY,
	id_partido int NOT NULL,
    FOREIGN KEY (id_partido ) REFERENCES partido(id),
    FOREIGN KEY (ci_ciudadano) REFERENCES ciudadano(ci)
);

CREATE TABLE credencial (
    serie varchar(5) NOT NULL,
    numero varchar(5) NOT NULL,
    ci_ciudadano varchar(8) NOT NULL,
    PRIMARY KEY (serie, numero),
    FOREIGN KEY (ci_ciudadano) REFERENCES ciudadano(ci)
);

CREATE TABLE eleccion (
    id int AUTO_INCREMENT PRIMARY KEY,
    fecha date NOT NULL,
    id_tipo_eleccion int NOT NULL,
    FOREIGN KEY (id_tipo_eleccion) REFERENCES tipo_eleccion(id)
);

CREATE TABLE agente_policia (
    ci_ciudadano varchar(8) NOT NULL PRIMARY KEY,
    id_comisaria int NOT NULL,
    FOREIGN KEY (ci_ciudadano) REFERENCES ciudadano(ci),
    FOREIGN KEY (id_comisaria) REFERENCES comisaria(id)
);

CREATE TABLE agente_establecimiento (
    ci_policia varchar(8) NOT NULL,
    id_establecimiento int NOT NULL,
    PRIMARY KEY (ci_policia, id_establecimiento),
    FOREIGN KEY (ci_policia) REFERENCES agente_policia(ci_ciudadano),
    FOREIGN KEY (id_establecimiento) REFERENCES establecimiento(id)
);

CREATE TABLE circuito (
    id int AUTO_INCREMENT NOT NULL,
    id_eleccion int NOT NULL,
    accesible tinyint(1) NOT NULL DEFAULT 0,
    id_establecimiento int NOT NULL,
    PRIMARY KEY (id, id_eleccion),
    FOREIGN KEY (id_eleccion) REFERENCES eleccion(id),
    FOREIGN KEY (id_establecimiento) REFERENCES establecimiento(id)
);

CREATE TABLE mesa (
    num INT NOT NULL,
    id_circuito INT NOT NULL,
    id_eleccion INT NOT NULL,
    PRIMARY KEY (num, id_circuito, id_eleccion),
    FOREIGN KEY (id_circuito, id_eleccion) REFERENCES circuito(id, id_eleccion)
);

CREATE TABLE tipo_empleado (
    id int AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(20) UNIQUE NOT NULL
);

CREATE TABLE empleado_publico (
    ci_ciudadano varchar(8) PRIMARY KEY,
    FOREIGN KEY (ci_ciudadano) REFERENCES ciudadano(ci)
);

CREATE TABLE participacion_en_mesa (
    ci_ciudadano VARCHAR(8) NOT NULL,
    num_mesa INT NOT NULL,
    id_circuito INT NOT NULL,
    id_eleccion INT NOT NULL,
    id_tipo INT NOT NULL,
    PRIMARY KEY (ci_ciudadano, num_mesa, id_circuito, id_eleccion, id_tipo),
    FOREIGN KEY (ci_ciudadano) REFERENCES empleado_publico(ci_ciudadano),
    FOREIGN KEY (num_mesa, id_circuito, id_eleccion) REFERENCES mesa(num, id_circuito, id_eleccion),
    FOREIGN KEY (id_tipo) REFERENCES tipo_empleado(id)
);
CREATE TABLE asignado (
    serie_credencial varchar(5) NOT NULL,
    numero_credencial varchar(5) NOT NULL,
    id_circuito int NOT NULL,
    id_eleccion int NOT NULL,
    PRIMARY KEY (serie_credencial, numero_credencial, id_circuito, id_eleccion),
    FOREIGN KEY (serie_credencial, numero_credencial) REFERENCES credencial(serie, numero),
    FOREIGN KEY (id_circuito, id_eleccion) REFERENCES circuito(id, id_eleccion)
);

CREATE TABLE vota_en (
    serie_credencial varchar(5) NOT NULL,
    numero_credencial varchar(5) NOT NULL,
    id_circuito int NOT NULL,
    id_eleccion int NOT NULL,
    observado tinyint(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (serie_credencial, numero_credencial, id_circuito, id_eleccion),
    FOREIGN KEY (serie_credencial, numero_credencial) REFERENCES credencial(serie, numero),
    FOREIGN KEY (id_circuito, id_eleccion) REFERENCES circuito(id, id_eleccion)
);

CREATE TABLE papeleta (
    id int AUTO_INCREMENT NOT NULL,
    id_eleccion int NOT NULL,
    PRIMARY KEY(id, id_eleccion),
    FOREIGN KEY (id_eleccion) REFERENCES eleccion(id)
);

CREATE TABLE lista (
    id_papeleta int NOT NULL,	
    id_eleccion int NOT NULL,
    id_partido int NOT NULL,
    organo varchar(50) NOT NULL,
    id_departamento int NOT NULL,
    PRIMARY KEY(id_papeleta, id_eleccion),
    FOREIGN KEY (id_papeleta, id_eleccion) REFERENCES papeleta(id, id_eleccion),
    FOREIGN KEY (id_partido) REFERENCES partido(id),
    FOREIGN KEY (id_departamento) REFERENCES departamento(id)
);

CREATE TABLE voto (
    id int AUTO_INCREMENT PRIMARY KEY,
    id_circuito int NOT NULL,
    id_eleccion int NOT NULL,
	observado tinyint(1) NOT NULL DEFAULT 0,
    FOREIGN KEY (id_circuito, id_eleccion) REFERENCES circuito(id, id_eleccion)
);

CREATE TABLE candidato_por_lista (
	id_papeleta int NOT NULL,
	id_eleccion int NOT NULL,
	id_candidato varchar(8) NOT NULL,
	PRIMARY KEY(id_papeleta, id_eleccion, id_candidato),
    FOREIGN KEY (id_papeleta, id_eleccion) REFERENCES lista(id_papeleta, id_eleccion),
    FOREIGN KEY (id_candidato) REFERENCES candidato(ci_ciudadano)
);

CREATE TABLE voto_anulado (
   	id_voto int PRIMARY KEY,
    FOREIGN KEY (id_voto) REFERENCES voto(id)
);

CREATE TABLE voto_blanco (
   	id_voto int PRIMARY KEY,
    FOREIGN KEY (id_voto) REFERENCES voto(id)
);

CREATE TABLE voto_normal (
  	id_voto int PRIMARY KEY,
	observado tinyint(1) NOT NULL DEFAULT 0,
    FOREIGN KEY (id_voto) REFERENCES voto(id)
);

CREATE TABLE voto_elige_papeleta (
    id_voto_normal int NOT NULL,
    id_papeleta int NOT NULL,
	id_eleccion int NOT NULL, 
    PRIMARY KEY(id_voto_normal, id_papeleta, id_eleccion),
    FOREIGN KEY (id_papeleta, id_eleccion) REFERENCES papeleta(id, id_eleccion),
    FOREIGN KEY (id_voto_normal) REFERENCES voto_normal(id_voto)
);

CREATE TABLE papeleta_plebiscito (
    id_papeleta int NOT NULL,	
    id_eleccion int NOT NULL,
	nombre varchar(30) NOT NULL,
	valor varchar(100) NOT NULL,
    PRIMARY KEY(id_papeleta, id_eleccion),
    FOREIGN KEY (id_papeleta, id_eleccion) REFERENCES papeleta(id, id_eleccion)
);

CREATE TABLE administrador (
   id INT AUTO_INCREMENT PRIMARY KEY,
   usuario VARCHAR(50) UNIQUE NOT NULL,
   password VARCHAR(255) NOT NULL
);


