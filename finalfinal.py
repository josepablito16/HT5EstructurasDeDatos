# FECHA: 04/03/2018
# SIMULACION DE UN PROCESADOR CON LA AYUDA DE SIMPY
# ALGORITMOS Y ESTRUCTURA DE DATOS
# SERGIO MARCEHNA 16387
# JOSE CIFUNETS 17509

#IMPORTACION DE LIBRERIAS
import simpy
import random

#valores iniciales
memoria=50#CANTIDAD DE MEMORIA
tTotal=0#TIEMPO TOTAL DE LA CORRIDA DE PROCESOS
cantidad=200 #PROCESOS
intervalo=10#INTERCALO
numeroCPU=1#NUMMERO DE PROCESADORES
random.seed(0)#SE FIJA DE DONDE COMENZAR EL PSEUDORANDOM PARA QUE SIEMPRE COMIENCE DESDE 0

#solo necesitamos definir ready. Porque en ready es donde pasa todo. 
def ready(nombre, env, itotales,irestantes):

    global memoria # :( mala practica, pero ni modo
    global tTotal # :( mala practica, pero ni modo

    if(memoria<90)or(itotales!=irestantes): # si la memoria se encuentra llena o se agrega a la cola un proceso
        memoria=memoria+itotales
        tiempo=env.now
        #READY
        print('El proceso #%d se esta listo para ser procesado con %d instrucciones' % (nombre, irestantes))
        yield env.timeout(5)
        #RUNNING
        with cpu.request() as hola:
            yield hola
            yield env.timeout(10)
            if(irestantes>3): #si hay mas de tres instrucciones restantes
                print('El proceso #%d se esta procesando en el tiempo %d' % (nombre, env.now))
                # WAITING O READY
                flag=random.randint(0,1) #random 1 o 2
                if(flag==1):
                    print('El proceso #%d esta esperando entrada/salida en el tiempo %d' % (nombre, env.now))
                    yield env.timeout(20)
                    env.process(ready(nombre, env, itotales,irestantes-3))#ready
                else:
                    env.process(ready(nombre, env, itotales,irestantes-3))#ready
            else:
                #TERMINATED
                print('El proceso #%d finalizo en el tiempo %d'%(nombre,env.now))
                print('Se esta liberando memoria utilizada por el proceso #%d' % nombre)
                memoria=memoria-itotales #liberar memoria
                tTotal = tTotal + env.now - tiempo
    else:
        print('La memoria esta llena en el tiempo %d'% env.now)


# ------------------------------ ENVIRONMENT ----------------------------- #

env=simpy.Environment()
cpu=simpy.Resource(env,capacity = numeroCPU) #cantidad de procesadores


def procesos(env, memoria, cpu, intervalo):
    for i in range(cantidad):
        instrucciones = random.randint(1,10) #instrucciones por proceso
        timepo2 = random.expovariate(1.0/intervalo)
        print ('El proceso #%d se ha creado en el tiempo %d, con %d instrucciones' % (i, timepo2, instrucciones))
        env.process(ready(i,env,instrucciones,instrucciones))
        yield env.timeout(timepo2)
env.process(procesos(env, cpu, memoria, intervalo))
env.run(until = 999999999)

tfinal = tTotal/200.0
print "El tiempo promedio es de: ", tfinal



