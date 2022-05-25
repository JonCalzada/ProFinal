USE CoordinadorTransacciones
GO

--Insertar datos de los bancos a usar
INSERT INTO Banco
VALUES (110,'Bancomer','Av. del Iman')

INSERT INTO Banco
VALUES (111,'Banamex','Reforma')

INSERT INTO Banco
VALUES (112,'Santander','Centro Historico')

--Insertar datos de los usuarios
INSERT INTO Cliente
VALUES (314,'Angel Chavez','Gustavo A. Madero',111,1000)

INSERT INTO Cliente
VALUES (315,'Jonathan Calzada','Texcoco',112,1000)

INSERT INTO Cliente
VALUES (316,'Mauricio Casillas','Toluca',111,1000)


SELECT * FROM Banco

SELECT * FROM Cliente

SELECT * FROM Operacion


DROP TABLE Operacion
DROP TABLE Cliente
DROP TABLE Banco
