"""
Universidad Nacional Autónoma de México
Tarea 5. Uso del coordinador de transacciones.

Integrantes del equipo.
    -Calzada Martinez Jonathan
    -Chávez García Jesús Ángel
    -Casillas Toledo Mauricio Enrique
"""
import datetime
import pyodbc as db
import socket as sck
import logging
import concurrent.futures
import random


conexion = ''
condb = ''
disponibilidadEscritura = True
disponibilidadLectura = True

class transaccion:
    """ Genera el id de una transacción usando el tiempo unix """
    def creaTransaccion(self,transaccion,ID):
        identificador = int(datetime.datetime.timestamp(datetime.datetime.now())*1000)
        insertar = 'INSERT INTO Operacion VALUES (?,?,?,?)'
        cursor = conexion.cursor()
        current_date = datetime.datetime.now()
        date = int(current_date.strftime("%Y%m%d"))
        cursor.execute(insertar,[identificador,transaccion,int(date),ID])
        cursor.commit()

    def terminarTransaccion(self,ID):
        cursor = conexion.cursor()
        cursor.commit()
        cursor.close

    def abortarTransaccion(self, cursor, ID):
        cursor.close

    # 0 -> consulta
    # 1 -> deposito
    # 2 -> retiro
    def Coordinador(self, cursor, database, operacion, ID): 
        global disponibilidadEscritura
        global disponibilidadLectura
        if(operacion == 0):
            if(disponibilidadLectura):
                condb.consultaDB(ID)
                self.terminarTransaccion(ID)
                return True
            else: 
                self.abortarTransaccion(cursor, ID)
                return True
        elif(operacion == 1):
            if(disponibilidadEscritura):
                disponibilidadEscritura = False
                disponibilidadLectura = False
                database.depositoDB(ID)
                self.terminarTransaccion(ID)
                disponibilidadEscritura = True
                disponibilidadLectura = True
                return True
            else: 
                self.abortarTransaccion(cursor, ID)
                return True
        elif(operacion == 2):
            if(disponibilidadEscritura):
                disponibilidadEscritura = False
                disponibilidadLectura = False
                database.retiroDB(ID)
                self.terminarTransaccion(ID)
                disponibilidadEscritura = True
                disponibilidadLectura = True
                return True
            else: 
                self.abortarTransaccion(cursor, ID)

class database:
    """
    Va a conectar el programa a la base de datos. Ademas, va a realizar 
    las operaciones necesarias que el usuario necesite
    """
    def conexionSQL(self):
        global conexion
        server = sck.gethostname()
        print('\nConectando a la base de datos\n')
        try:
            conexion = db.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE=CoordinadorTransacciones')
            print('\nConexión a la base de datos establecida\n')
        except:
            print('\nNo se pudo conectar a la base de datos\n')
    
    def consultaDB(self,ID):
        global conexion
        consulta = 'SELECT Saldo FROM Cliente WHERE (NoCuenta = ?)'
        cursor = conexion.cursor()
        cursor.execute(consulta,ID)
        saldo = cursor.fetchone()
        print('\nMonto total: $'+str(saldo[0])+'\n')
    
    def retiroDB(self,ID):
        global conexion
        bandera = 0
        monto = random.randrange(100,500,100)
        consulta = 'SELECT Saldo FROM Cliente WHERE (NoCuenta = ?)'
        cursor = conexion.cursor()
        cursor.execute(consulta,ID)
        saldo = cursor.fetchone()
        
        if(monto > int(saldo[0]) or monto == 0):
            print('\nNo se puede retirar el monto solicitado, esto debido a que es mayor al saldo de la cuenta.\n')
            return int(saldo[0]), bandera
        else:
            res = random.randint(1, 2)
            if(res==1):
                bandera = 1
                saldoFinal=int(saldo[0])-monto
                retiro = 'UPDATE Cliente SET SALDO = ? WHERE NoCuenta = ?'
                cursor.execute(retiro,[saldoFinal,ID])
                cursor.commit()
                return saldoFinal, bandera
            else:
                return int(saldo[0]), bandera
    
    def depositoDB(self,ID):
        global conexion
        monto = random.randrange(100,500,100)
        consulta = 'SELECT Saldo FROM Cliente WHERE (NoCuenta = ?)'
        cursor = conexion.cursor()
        cursor.execute(consulta,ID)
        saldo = cursor.fetchone()
        saldoFinal=int(saldo[0])+monto
        res = random.randint(1, 2)
        if(res==1):
            retiro = 'UPDATE Cliente SET SALDO = ? WHERE NoCuenta = ?'
            cursor.execute(retiro,[saldoFinal,ID])
            cursor.commit()
            return saldoFinal
        else:
            return int(saldo[0])

class principal:
    def banco(self):
        global conexion
        global condb
        bandera = 0
        salida = 0
        insTran = transaccion()
        condb = database()
        condb.conexionSQL()
        cursor = conexion.cursor()
        ID = random.randint(314, 316)
        consulta = 'SELECT NoCuenta FROM Cliente WHERE NoCuenta = ?'
            
        consulta = 'SELECT Saldo FROM Cliente WHERE NoCuenta = ?'
        cursor.execute(consulta,ID)
        monto = cursor.fetchone()
        
        consulta = 'SELECT Nombre FROM Cliente WHERE NoCuenta = ?'
        cursor.execute(consulta,ID)
        usuario = cursor.fetchone()
        
        print('\nIdentificador: '+str(ID)+'\nUsuario: '+str(usuario[0])+'\n')
        """El siguiente ciclo corresponde al menu de la cuenta bancaria"""
        while(salida == 0):
            print('1. Realizar deposito\n2. Realizar retiro\n3. Consultar saldo\n4. Salir')
            """El try-except sirve para tratar el error que pueda surgir si se 
            introduce alguna letra en vez de un número"""
            opcion = random.randint(1, 4)
            
            if(opcion == 1):
                """Esta primera opción realizará el deposito"""
                """
                monto = condb.depositoDB(ID)
                print('Monto total: $'+str(monto)+'\n')
                insTran.creaTransaccion('Deposito', ID)
                print('\nDeposito Realizado con exito\n')
                """
                print('Monto total: $'+str(monto)+'\n')
                insTran.Coordinador(cursor, conexion, 1, ID)
                print('\nDeposito Realizado con exito\n')

            elif(opcion == 2):
                """Esta segunda opción realizará el retiro"""
                monto, bandera=condb.retiroDB(ID)
                if(bandera == 0):
                    print('No se pudo realizar la transacción\n')
                elif(bandera == 1):
                    """
                    print('Monto total: $'+str(monto)+'\n')
                    insTran.creaTransaccion('Retiro', ID)
                    print('\nRetiro Realizado con exito\n')
                    """
                    print('Monto total: $'+str(monto)+'\n')
                    insTran.Coordinador(cursor, conexion, 2, ID)
                    print('\nRetiro Realizado con exito\n')

            elif (opcion == 3):
                """Esta tercera opción mostrará el saldo total"""
                """
                condb.consulta(ID)
                insTran.creaTransaccion('Consulta de saldo', ID)
                """
                insTran.Coordinador(cursor, conexion, 0, ID)
                
            elif(opcion == 4):
                """Esta cuarta opción terminará el programa"""
                salida = 1
            else:
                print('\nSelecciona una opción valida\n')
                
        print('\nSaliendo de la cuenta')
    

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(principal.banco, range(5))