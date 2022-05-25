"""
Universidad Nacional Autónoma de México
Tarea 4. Uso del coordinador de transacciones.

Integrantes del equipo.
    -Calzada Martinez Jonathan
    -Chávez García Jesús Ángel
    -Casillas Toledo Mauricio Enrique
"""
import datetime
import pyodbc as db
import socket as sck

conexion = ''

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
    
    def consulta(self,ID):
        global conexion
        consulta = 'SELECT Saldo FROM Cliente WHERE (NoCuenta = ?)'
        cursor = conexion.cursor()
        cursor.execute(consulta,ID)
        saldo = cursor.fetchone()
        print('\nMonto total: $'+str(saldo[0])+'\n')
    
    def retiroDB(self,ID):
        global conexion
        bandera = 0
        monto = int(input('\nMonto a retirar: \n'))
        consulta = 'SELECT Saldo FROM Cliente WHERE (NoCuenta = ?)'
        cursor = conexion.cursor()
        cursor.execute(consulta,ID)
        saldo = cursor.fetchone()
        
        if(monto > int(saldo[0])):
            print('\nNo se puede retirar el monto solicitado, esto debido a que es mayor al saldo de la cuenta.\n')
            return int(saldo[0]), bandera
        else:
            res = int(input('Continuar con la transacción?: \n1.- sí\n2.- no\n\n'))
            if(res==1):
                bandera = 1
                saldoFinal=int(saldo[0])-monto
                #men.añade(cantidadTotal, tran.creaTransaccion())
                retiro = 'UPDATE Cliente SET SALDO = ? WHERE NoCuenta = ?'
                cursor.execute(retiro,[saldoFinal,ID])
                cursor.commit()
                return saldoFinal, bandera
            else:
                return int(saldo[0]), bandera
    
    def depositoDB(self,ID):
        global conexion
        monto = int(input('\nMonto a depositar: \n'))
        consulta = 'SELECT Saldo FROM Cliente WHERE (NoCuenta = ?)'
        cursor = conexion.cursor()
        cursor.execute(consulta,ID)
        saldo = cursor.fetchone()
        saldoFinal=int(saldo[0])+monto
        res = int(input('Continuar con la transacción?: \n1.- sí\n2.- no\n\n'))
        if(res==1):
            retiro = 'UPDATE Cliente SET SALDO = ? WHERE NoCuenta = ?'
            cursor.execute(retiro,[saldoFinal,ID])
            cursor.commit()
            return saldoFinal
        else:
            return int(saldo[0])

class principal:
    def __init__(self):
        global conexion
        bandera = 0
        salida = 0
        insTran = transaccion()
        condb = database()
        condb.conexionSQL()
        cursor = conexion.cursor()
        while(bandera == 0):
            try:
                ID = int(input('Introduce el numero de cuenta: '))
                consulta = 'SELECT NoCuenta FROM Cliente WHERE NoCuenta = ?'
                if(cursor.execute(consulta,ID)):
                    bandera = 1
                else:
                    print('\nDatos incorrectos, intenta otra vez\n')
            except:
                print('\nDatos incorrectos, intenta otra vez\n')
            
        consulta = 'SELECT Saldo FROM Cliente WHERE NoCuenta = ?'
        cursor.execute(consulta,ID)
        monto = cursor.fetchone()
        
        consulta = 'SELECT Nombre FROM Cliente WHERE NoCuenta = ?'
        cursor.execute(consulta,ID)
        usuario = cursor.fetchone()
        
        print('\nIdentificador: '+str(ID)+'\nUsuario: '+str(usuario[0])+'\n')
        """El siguiente ciclo corresponde al menu de la cuenta bancaria"""
        while(salida == 0):
            aceptar = 0
            print('1. Realizar deposito\n2. Realizar retiro\n3. Consultar saldo\n4. Salir')
            """El try-except sirve para tratar el error que pueda surgir si se 
            introduce alguna letra en vez de un número"""
            while(aceptar == 0):
                try:
                    opcion = int(input('Selecciona una opción: '))
                    aceptar = 1
                except (ValueError):
                    print('\nDato incorrecto, introduce otro\n')
            
            if(opcion == 1):
                """Esta primera opción realizará el deposito"""
                monto = condb.depositoDB(ID)
                print('Monto total: $'+str(monto)+'\n')
                insTran.creaTransaccion('Deposito', ID)
                print('\nDeposito Realizado con exito\n')
            elif(opcion == 2):
                """Esta segunda opción realizará el retiro"""
                monto, bandera=condb.retiroDB(ID)
                if(bandera == 0):
                    print('No se pudo realizar la transacción\n')
                elif(bandera == 1):
                    print('Monto total: $'+str(monto)+'\n')
                    insTran.creaTransaccion('Retiro', ID)
                    print('\nRetiro Realizado con exito\n')
            elif (opcion == 3):
                """Esta tercera opción mostrará el saldo total"""
                condb.consulta(ID)
                insTran.creaTransaccion('Consulta de saldo', ID)
            elif(opcion == 4):
                """Esta cuarta opción terminará el programa"""
                salida = 1
            else:
                print('\nSelecciona una opción valida\n')
                
        print('\nSaliendo de la cuenta')
    

        
obj=principal()