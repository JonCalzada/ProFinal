"""
Por el momento, el programa sólo hará la parte del 
depósito. Al final se juntará todo
"""

class memoria:
    """En el método añade se planea que reciba la información
    que se genere al realizar un deposito o un retiro"""
    def añade(self,cantidadTotal):
        transaccion = open("Transacciones.txt","a")
        transaccion.write("El monto final es $"+str(cantidadTotal)+" \n")
        transaccion.close()
        print('\t\tHolaaaaa \n')

class deposito:
    """El método añade la cantidad que se ha introducido
    al monto inicial"""
    def realizarDeposito(self, monto):
        men=memoria()
        cantidad=int(input('Monto a depositar: $'))
        cantidadTotal=cantidad+monto
        men.añade(cantidadTotal)
        return cantidadTotal
class retiro: 
    """ El metodo realiza un retiro de la memoria """
    def retirar (self, monto): 
        men=memoria()
        cantidad=int (input('Monto a retirar: $'))
        cantidadTotal=monto-cantidad
        men.añade(cantidadTotal)
        return cantidadTotal
        
        
class principal:
    def __init__(self):
        salida = 0
        monto = 200
        usuario = 'Angel'
        dep=deposito()
        ret=retiro()
        print('Usuario: '+usuario+'\nMonto: $'+str(monto)+'\n')
        """El siguiente ciclo corresponde al menu de la cuenta bancaria"""
        while(salida == 0):
            aceptar = 0
            print('1. Realizar deposito\n2. Realizar retiro\n3.Consultar saldo\n4. Salir')
            """El try-except sirve para tratar el error que pueda surgir si se 
            introduce alguna letra en vez de un número"""
            while(aceptar == 0):
                try:
                    opcion = int(input('Selecciona una opción: '))
                    aceptar = 1
                except (ValueError):
                    print('\nDato incorrecto, introduce otro\n')
            
            if(opcion == 1 and isinstance(opcion,int)):
                monto=dep.realizarDeposito(monto)
                print('Monto total: $'+str(monto)+'\n')
                print('\nDeposito1 Realizado con exito\n')
            elif(opcion == 2 and isinstance(opcion,int)):
               
                monto=ret.retirar(monto)
                print('Monto total: $'+str(monto)+'\n')
                print('\nRetiro Realizado con exito\n')
            elif (opcion == 3 and isinstance(opcion, int)):
                print('Monto total: $'+str(monto)+'\n')
            elif(opcion == 4 and isinstance(opcion,int)):
                salida = 1
            else:
                print('\nSelecciona una opción valida\n')
                
        print('\nSaliendo de la cuenta')
        
obj=principal()
